import os
import shutil
import socket

import toml
from loguru import logger

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
config_file = f"{root_dir}/config.toml"
_CONTAINER_CGROUP_MARKERS = ("docker", "containerd", "kubepods", "libpod", "podman")
_DOCKER_HOST_GATEWAY_NAME = "host.docker.internal"


def is_running_in_container(
    dockerenv_path: str = "/.dockerenv",
    containerenv_path: str = "/run/.containerenv",
    cgroup_path: str = "/proc/1/cgroup",
) -> bool:
    """
    Kiểm tra xem chương trình hiện tại có đang chạy bên trong Docker/container hay không.

    Mục đích chính của việc kiểm tra này là để xác định địa chỉ mặc định khi kết nối
    đến Ollama:

    - Nếu chương trình chạy trực tiếp trên máy tính:
        + localhost sẽ trỏ đến chính máy tính của người dùng.
        + Có thể sử dụng: http://localhost:12345/v1

    - Nếu chương trình chạy trong Docker:
        + localhost chỉ trỏ đến chính container, không phải máy chủ (host).
        + Muốn truy cập Ollama đang chạy trên máy chủ thường phải dùng:
        http://host.docker.internal:12345/v1

    Không thể chỉ kiểm tra sự tồn tại của file /proc/1/cgroup vì hầu hết các hệ điều
    hành Linux đều có file này. Thay vào đó, hàm sẽ tìm các dấu hiệu đặc trưng của
    Docker hoặc các nền tảng container khác (docker, containerd, kubepods, podman...)
    để xác định chính xác môi trường đang chạy.

    Các đường dẫn được khai báo dưới dạng tham số để có thể thay thế bằng dữ liệu giả
    (mock) khi viết Unit Test, giúp kiểm thử hàm trong nhiều môi trường khác nhau mà
    không cần chạy Docker thật.
    """
    if os.path.isfile(dockerenv_path) or os.path.isfile(containerenv_path):
        return True

    try:
        with open(cgroup_path, mode="r", encoding="utf-8") as fp:
            cgroup_content = fp.read().lower()
    except OSError:
        return False

    return any(marker in cgroup_content for marker in _CONTAINER_CGROUP_MARKERS)


def _can_resolve_hostname(hostname: str) -> bool:
    try:
        socket.gethostbyname(hostname)
    except OSError:
        return False
    return True


def _decode_linux_route_gateway(hex_gateway: str) -> str:
    # Gateway trong /proc/net/route là dạng hex little-endian, ví dụ 010011AC là
    # 172.17.0.1. Phân tích riêng ở đây để khi Docker trên Linux gốc không có
    # bản ghi DNS host.docker.internal, vẫn có thể thử truy cập máy chủ host qua gateway mặc định của container.
    if len(hex_gateway) != 8:
        raise ValueError("invalid gateway length")

    octets = [
        str(int(hex_gateway[index : index + 2], 16))
        for index in range(6, -1, -2)
    ]
    return ".".join(octets)


def get_container_default_gateway_ip(route_path: str = "/proc/net/route") -> str:
    """
    Đọc địa chỉ IP gateway mặc định trong container Linux.

    Docker Desktop thường cung cấp `host.docker.internal`, nhưng Docker trên Linux gốc
    mặc định không chắc có tên DNS này. Gateway mặc định thường có thể được dùng
    làm địa chỉ dự phòng để truy cập các dịch vụ trên máy chủ host; nếu Ollama của người dùng
    chỉ lắng nghe trên 127.0.0.1, họ vẫn cần cấu hình Ollama để lắng nghe trên card mạng của host
    hoặc cấu hình thủ công `ollama_base_url`.
    """
    try:
        with open(route_path, mode="r", encoding="utf-8") as fp:
            route_lines = fp.readlines()
    except OSError:
        return ""

    for line in route_lines[1:]:
        fields = line.strip().split()
        if len(fields) < 3:
            continue

        destination = fields[1]
        gateway = fields[2]
        if destination != "00000000" or gateway == "00000000":
            continue

        try:
            return _decode_linux_route_gateway(gateway)
        except ValueError:
            logger.warning(f"invalid container gateway route entry: {line.strip()}")
            return ""

    return ""


def get_default_ollama_base_url() -> str:
    """
    Trả về base_url mặc định tương thích với OpenAI cho Ollama.

    Hàm này sẽ không được gọi nếu người dùng đã cấu hình `ollama_base_url` một cách tường minh;
    nó chỉ xử lý "giá trị mặc định tốt nhất khi chưa được cấu hình".
    Trong container, nó sẽ mặc định trỏ đến máy chủ host, còn khi chạy bình thường trên máy, nó sẽ trỏ đến localhost.
    """
    if not is_running_in_container():
        return "http://localhost:11434/v1"

    if _can_resolve_hostname(_DOCKER_HOST_GATEWAY_NAME):
        return f"http://{_DOCKER_HOST_GATEWAY_NAME}:11434/v1"

    gateway_ip = get_container_default_gateway_ip()
    if gateway_ip:
        logger.info(
            "host.docker.internal is not resolvable, fallback to container "
            f"default gateway for Ollama: {gateway_ip}"
        )
        return f"http://{gateway_ip}:11434/v1"

    logger.warning(
        "failed to resolve host.docker.internal and container default gateway; "
        "fallback to host.docker.internal for Ollama"
    )
    return f"http://{_DOCKER_HOST_GATEWAY_NAME}:11434/v1"


def load_config():
    # Sửa lỗi: IsADirectoryError: [Errno 21] Is a directory: '/MoneyPrinterTurbo/config.toml'
    if os.path.isdir(config_file):
        shutil.rmtree(config_file)

    if not os.path.isfile(config_file):
        example_file = f"{root_dir}/config.example.toml"
        if os.path.isfile(example_file):
            shutil.copyfile(example_file, config_file)
            logger.info("copy config.example.toml to config.toml")

    logger.info(f"load config from file: {config_file}")

    try:
        _config_ = toml.load(config_file)
    except Exception as e:
        logger.warning(f"load config failed: {str(e)}, try to load as utf-8-sig")
        with open(config_file, mode="r", encoding="utf-8-sig") as fp:
            _cfg_content = fp.read()
            _config_ = toml.loads(_cfg_content)
    return _config_


def save_config():
    with open(config_file, "w", encoding="utf-8") as f:
        _cfg["app"] = app
        _cfg["azure"] = azure
        _cfg["siliconflow"] = siliconflow
        _cfg["elevenlabs"] = elevenlabs
        _cfg["chatterbox"] = chatterbox
        _cfg["ui"] = ui
        f.write(toml.dumps(_cfg))


_cfg = load_config()
app = _cfg.get("app", {})
whisper = _cfg.get("whisper", {})
proxy = _cfg.get("proxy", {})
azure = _cfg.get("azure", {})
siliconflow = _cfg.get("siliconflow", {})
elevenlabs = _cfg.get("elevenlabs", {})
chatterbox = _cfg.get("chatterbox", {})
ui = _cfg.get(
    "ui",
    {
        "hide_log": False,
    },
)

vnpay = _cfg.get("vnpay", {})

hostname = socket.gethostname()

log_level = _cfg.get("log_level", "DEBUG")
listen_host = _cfg.get("listen_host", "0.0.0.0")
listen_port = _cfg.get("listen_port", 8080)
project_name = _cfg.get("project_name", "MoneyPrinterTurbo")
project_description = _cfg.get(
    "project_description",
    "<a href='https://github.com/harry0703/MoneyPrinterTurbo'>https://github.com/harry0703/MoneyPrinterTurbo</a>"
    "<br><small>Supported by <a href='https://aihubmix.com/?aff=CEve'>AIHubMix</a></small>",
)
project_version = _cfg.get("project_version", "1.3.0")

VNP_TMN_CODE = vnpay.get("tmn_code", "")
VNP_HASH_SECRET = vnpay.get("hash_secret", "")
VNP_URL = vnpay.get(
    "url",
    "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html",
)
VNP_RETURN_URL = vnpay.get("return_url", "")

reload_debug = False

app["redis_host"] = os.getenv(
    "MPT_APP_REDIS_HOST",
    os.getenv("REDIS_HOST", app.get("redis_host", "localhost")),
)

imagemagick_path = app.get("imagemagick_path", "")
if imagemagick_path and os.path.isfile(imagemagick_path):
    os.environ["IMAGEMAGICK_BINARY"] = imagemagick_path

ffmpeg_path = app.get("ffmpeg_path", "")
if ffmpeg_path and os.path.isfile(ffmpeg_path):
    os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

logger.info(f"{project_name} v{project_version}")
