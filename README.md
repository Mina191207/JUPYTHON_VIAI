# 🎬 VIAI

**Nền tảng AI tạo video ngắn (TikTok / Reels / Shorts) hoàn toàn bằng tiếng Việt** — từ ý tưởng đến video hoàn chỉnh chỉ trong vài phút, không cần kỹ năng dựng phim, không cần tự cấu hình kỹ thuật phức tạp.

> Dự án thuộc nhóm **JuPython**.

---

## ✨ Tính năng chính

- 🧠 **AI viết kịch bản tiếng Việt** — hook 3 giây đầu, nội dung chính, CTA cuối; hỗ trợ giọng điệu Bắc / Trung / Nam
- 🔥 **Gợi ý trend đang hot** trên TikTok Việt Nam theo thời gian thực
- 🎙️ **Giọng đọc TTS tiếng Việt tự nhiên** — tích hợp sẵn, không cần tự đăng ký API nước ngoài
- 🎞️ **Tự động ghép video, phụ đề, nhạc nền** và xuất file MP4 hoàn chỉnh
- 📦 **SaaS sẵn dùng** — đăng ký, trả phí, tạo video ngay, không cần cài đặt kỹ thuật

---

## 🛠️ Tech Stack

| Layer | Công nghệ |
|---|---|
| Backend | Python 3.11 + FastAPI |
| Frontend | Streamlit |
| AI / LLM | Google Gemini Flash 2.0 API |
| Text-to-Speech | Edge TTS (`vi-VN-HoaiMyNeural`, `vi-VN-NamMinhNeural`) |
| Video render | FFmpeg + MoviePy |
| Stock video | Pexels API |
| Database | SQLite |
| Base codebase | [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (MIT License) |

---

## 📦 Cài đặt & Chạy thử (Development)

### Yêu cầu hệ thống

- Python **3.11+**
- [FFmpeg](https://ffmpeg.org/download.html) — bắt buộc để render video
- [ImageMagick](https://imagemagick.org/script/download.php) — bắt buộc để render phụ đề
- Git

### Bước 1 — Clone repo

```bash
git clone https://github.com/Mina191207/JUPYTHON_VIAI.git
cd JUPYTHON_VIAI
git checkout dev
```

### Bước 2 — Tạo môi trường ảo và cài dependencies

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (macOS / Linux)
source venv/bin/activate

# Cài packages
pip install -r requirements.txt
```

### Bước 3 — Cấu hình API keys

```bash
# Copy file mẫu
cp .env.example .env
```

Mở file `.env` và điền thông tin:

```env
# === LLM ===
GEMINI_API_KEY=your_gemini_api_key_here
# Backup (tuỳ chọn)
OPENAI_API_KEY=your_openai_api_key_here

# === Stock Video ===
PEXELS_API_KEY=your_pexels_api_key_here

# === TTS (Edge TTS — không cần key) ===
TTS_VOICE_FEMALE=vi-VN-HoaiMyNeural
TTS_VOICE_MALE=vi-VN-NamMinhNeural

# === Paths ===
OUTPUT_DIR=./output
FONT_PATH=./fonts/ggfonts.ttf
```

> 💡 **Lấy API key ở đâu?**
> - Gemini: [aistudio.google.com](https://aistudio.google.com) → Get API key (miễn phí, 1500 request/ngày)
> - Pexels: [pexels.com/api](https://www.pexels.com/api/) → Your API Key (miễn phí)

### Bước 4 — Kiểm tra FFmpeg & ImageMagick

```bash
ffmpeg -version      # Phải hiện version, ví dụ: ffmpeg version 6.x
magick -version      # Windows
convert -version     # macOS / Linux
```

Nếu lệnh không nhận, cài theo hướng dẫn tại:
- FFmpeg: https://ffmpeg.org/download.html
- ImageMagick: https://imagemagick.org/script/download.php

### Bước 5 — Chạy app

```bash
streamlit run webui/Main.py
```

Mở trình duyệt tại: **http://localhost:8501**

---

## 🚀 Demo nhanh

```
1. Nhập chủ đề: "5 lỗi skincare người Việt hay mắc phải"
2. Chọn giọng đọc: Nữ (HoaiMy) / Nam (NamMinh)
3. Chọn phong cách: Review / Hướng dẫn / Storytelling
4. Chọn độ dài: 30s / 60s
5. Nhấn "Tạo video" → chờ ~2-3 phút → tải video MP4
```

---

## 📁 Cấu trúc thư mục

```
JUPYTHON_VIAI/              ← fork từ MoneyPrinterTurbo
├── .github/                # CI/CD workflows
├── app/                    # Core logic (services, models, config)
├── docs/                   # Tài liệu kỹ thuật
├── resource/               # Font, âm thanh, assets tĩnh
├── test/                   # Unit tests
├── webui/                  # Streamlit frontend (Main.py ở đây)
│   └── Main.py             # Điểm chạy chính: streamlit run webui/Main.py
├── .dockerignore
├── .env.example            # Mẫu cấu hình API keys
├── requirements.txt
└── README.md
```

---

## 👥 Đội ngũ — JuPython

| Vai trò | Họ tên | Phụ trách |
|---|---|---|
| 🎖️ Leader | Huỳnh Ngọc Thùy Dunng | Quản lý dự án, điều phối, review |
| ⚙️ Backend | Võ Anh Khôi | FastAPI, pipeline video, TTS |
| 🎨 Frontend | Nguyễn Thị Thư | Streamlit UI, UX |
| 🤖 AI Engineer | Lê Hoàng Trường | Prompt design, Gemini, trend module |
| 📝 Reporter | Trịnh Phương Hoài An | Hồ sơ dự thi, slide, video demo |

---

## 📄 License & Credit

Dự án kế thừa kiến trúc từ [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) (MIT License).
Phần Việt hóa, prompt tiếng Việt, TTS tích hợp và module gợi ý trend được phát triển mới hoàn toàn bởi nhóm JuPython.

---

*Built with ❤️ by JuPython