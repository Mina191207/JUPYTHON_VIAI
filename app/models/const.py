PUNCTUATIONS = [
    "?",
    ",",
    ".",
    "、",
    ";",
    ":",
    "!",
    "…",
    "？",
    "，",
    "。",
    "、",
    "；",
    "：",
    "！",
    "...",
    # Các dấu câu thường dùng trong tiếng Ả Rập cũng nên được coi là điểm ngắt câu tự nhiên,
    # để tránh sự không nhất quán về ranh giới dừng của phụ đề trả về từ văn bản kịch bản và edge-tts, dẫn đến việc khớp từng dòng sau đó không thành công.
    "،",
    "؛",
    "؟",
]

TASK_STATE_FAILED = -1
TASK_STATE_COMPLETE = 1
TASK_STATE_PROCESSING = 4

FILE_TYPE_VIDEOS = ["mp4", "mov", "mkv", "webm"]
FILE_TYPE_IMAGES = ["jpg", "jpeg", "png", "bmp"]
