<img width="764" height="684" alt="image" src="https://github.com/user-attachments/assets/3912ea8d-ceab-45c1-9fa7-9052f52b5b3b" />

# MP3 Compressor

Ứng dụng giao diện máy tính dùng để nén file âm thanh xuống dưới một giới hạn dung lượng nhất định. Phần mềm tự động tính toán bitrate phù hợp dựa trên thời lượng file, hỗ trợ theo dõi tiến trình, hủy quá trình nén và chuyển âm thanh sang Mono.

## Chức năng chính

- Chọn file âm thanh từ máy tính.
- Hiển thị kích thước, thời lượng và bitrate của file đầu vào.
- Thiết lập dung lượng tối đa mong muốn theo MB.
- Tự động tính toán bitrate để file đầu ra không vượt quá giới hạn.
- Thử giảm bitrate nhiều lần nếu file sau nén vẫn còn quá lớn.
- Hỗ trợ chuyển âm thanh sang Mono, phù hợp với ghi âm, cuộc họp và podcast.
- Hiển thị phần trăm tiến trình nén.
- Cho phép hủy quá trình đang chạy.
- Mở nhanh thư mục chứa file sau khi nén.
- Hoạt động trên Windows, macOS và Linux.

## Định dạng hỗ trợ

### File đầu vào

- MP3
- WAV
- M4A
- AAC
- FLAC

### File đầu ra

- MP3

> Phần mềm luôn xuất file dưới định dạng MP3 và sử dụng bộ mã hóa `libmp3lame` của FFmpeg.

## Yêu cầu hệ thống

Để chạy phần mềm, máy tính cần có:

1. **Python 3.10 trở lên**
2. **pip** để cài thư viện Python
3. **Tkinter** để hiển thị giao diện
4. **CustomTkinter**
5. **FFmpeg và FFprobe**
6. FFmpeg và FFprobe phải được thêm vào biến môi trường `PATH`

## Cài đặt nhanh trên Windows

### Bước 1: Cài đặt Python

Tải và cài Python 3 từ trang chính thức của Python.

Trong cửa sổ cài đặt, cần tích chọn:

```text
Add Python to PATH
```

Sau khi cài đặt, mở Command Prompt hoặc PowerShell và kiểm tra:

```bash
python --version
pip --version
```

Nếu lệnh `python` không hoạt động, thử:

```bash
py --version
```

### Bước 2: Tải mã nguồn

Clone repository:

```bash
git clone <URL_REPOSITORY>
cd <TEN_THU_MUC_REPOSITORY>
```

Hoặc tải mã nguồn dạng ZIP từ Git và giải nén.

### Bước 3: Tạo môi trường ảo

Khuyến nghị tạo môi trường ảo để tránh xung đột thư viện:

```bash
python -m venv .venv
```

Kích hoạt môi trường ảo bằng Command Prompt:

```bash
.venv\Scripts\activate
```

Kích hoạt bằng PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu máy sử dụng lệnh `py`, có thể tạo môi trường bằng:

```bash
py -m venv .venv
```

### Bước 4: Cài đặt thư viện Python

Nâng cấp pip:

```bash
python -m pip install --upgrade pip
```

Cài CustomTkinter:

```bash
pip install customtkinter
```

### Bước 5: Cài đặt FFmpeg

Tải một bản FFmpeg dành cho Windows và giải nén, ví dụ vào thư mục:

```text
C:\ffmpeg
```

Sau khi giải nén, cần đảm bảo tồn tại hai file:

```text
C:\ffmpeg\bin\ffmpeg.exe
C:\ffmpeg\bin\ffprobe.exe
```

Thêm đường dẫn sau vào biến môi trường `PATH`:

```text
C:\ffmpeg\bin
```

Cách thêm vào PATH:

1. Mở **Start** và tìm `Environment Variables`.
2. Chọn **Edit the system environment variables**.
3. Chọn **Environment Variables**.
4. Trong mục `Path`, chọn **Edit**.
5. Chọn **New** và thêm `C:\ffmpeg\bin`.
6. Nhấn **OK** để lưu.
7. Đóng và mở lại Command Prompt, PowerShell hoặc Visual Studio Code.

Kiểm tra cài đặt:

```bash
ffmpeg -version
ffprobe -version
```

Cả hai lệnh phải hiển thị thông tin phiên bản.

### Bước 6: Chạy phần mềm

```bash
python MP3_Compress.py
```

Hoặc:

```bash
py MP3_Compress.py
```

## Cài đặt trên Ubuntu hoặc Debian

Cài Python, Tkinter và FFmpeg:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk ffmpeg
```

Tạo và kích hoạt môi trường ảo:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cài thư viện:

```bash
pip install --upgrade pip
pip install customtkinter
```

Chạy phần mềm:

```bash
python3 MP3_Compress.py
```

## Cài đặt trên macOS

Cài Python và FFmpeg bằng Homebrew:

```bash
brew install python ffmpeg
```

Tạo và kích hoạt môi trường ảo:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cài thư viện:

```bash
pip install --upgrade pip
pip install customtkinter
```

Chạy phần mềm:

```bash
python3 MP3_Compress.py
```

## Hướng dẫn sử dụng

1. Chạy file `MP3_Compress.py`.
2. Nhấn **Chọn file** và chọn file âm thanh cần nén.
3. Chờ phần mềm đọc kích thước, thời lượng và bitrate.
4. Nhập giới hạn dung lượng mong muốn, ví dụ `190` MB.
5. Tích **Chuyển sang Mono** khi file chủ yếu là giọng nói.
6. Chọn vị trí lưu file đầu ra nếu cần thay đổi.
7. Nhấn **Bắt đầu nén**.
8. Chờ thanh tiến trình hoàn tất.
9. Nhấn **Mở thư mục** để xem file đã nén.

## Khuyến nghị dung lượng

Nếu website giới hạn file tối đa `200 MB`, nên đặt giá trị:

```text
190 MB
```

Khoảng dự phòng này giúp hạn chế trường hợp dung lượng thực tế chênh lệch do metadata hoặc cách website tính MB.

## Cấu trúc thư mục đề xuất

```text
mp3-compressor/
├── MP3_Compress.py
├── README.md
├── requirements.txt
└── .gitignore
```

Nội dung đề xuất cho `requirements.txt`:

```text
customtkinter
```

Cài tất cả thư viện từ file này bằng lệnh:

```bash
pip install -r requirements.txt
```

## Xử lý lỗi thường gặp

### Lỗi `ModuleNotFoundError: No module named 'customtkinter'`

Cài lại thư viện trong đúng môi trường Python đang sử dụng:

```bash
python -m pip install customtkinter
```

Nếu dùng lệnh `py`:

```bash
py -m pip install customtkinter
```

### Lỗi không tìm thấy FFmpeg hoặc FFprobe

Kiểm tra:

```bash
ffmpeg -version
ffprobe -version
```

Nếu lệnh không được nhận diện:

- Kiểm tra thư mục `bin` có chứa `ffmpeg.exe` và `ffprobe.exe`.
- Thêm đúng đường dẫn thư mục `bin` vào `PATH`.
- Đóng rồi mở lại Terminal hoặc Visual Studio Code.
- Khởi động lại máy nếu biến môi trường chưa được cập nhật.

### Đã thêm PATH nhưng phần mềm vẫn báo thiếu FFmpeg

Trong Python, chạy lệnh sau để kiểm tra:

```bash
python -c "import shutil; print(shutil.which('ffmpeg')); print(shutil.which('ffprobe'))"
```

Kết quả đúng phải trả về đường dẫn đến hai file thực thi. Ví dụ:

```text
C:\ffmpeg\bin\ffmpeg.exe
C:\ffmpeg\bin\ffprobe.exe
```

Nếu kết quả là `None`, Python chưa nhận được biến môi trường mới.

### Lỗi PowerShell không cho kích hoạt môi trường ảo

Mở PowerShell với quyền người dùng và chạy:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Sau đó kích hoạt lại:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Lỗi giao diện Tkinter trên Linux

Cài gói Tkinter:

```bash
sudo apt install python3-tk
```

### File đầu ra vẫn lớn hơn giới hạn

- Giảm giá trị dung lượng tối đa.
- Tích tùy chọn **Chuyển sang Mono**.
- File quá dài có thể cần bitrate rất thấp, làm giảm chất lượng âm thanh.
- Không nên đặt giới hạn quá thấp đối với file có thời lượng dài.

### Chất lượng âm thanh bị giảm

Dung lượng file, thời lượng và chất lượng có quan hệ trực tiếp với nhau. Khi yêu cầu file rất nhỏ nhưng thời lượng dài, phần mềm phải giảm bitrate nên chất lượng sẽ thấp hơn.

Đối với nội dung giọng nói, bật Mono thường giúp giảm dung lượng mà vẫn giữ chất lượng nghe tương đối tốt.

## Cách hoạt động

Phần mềm sử dụng `ffprobe` để lấy thời lượng và bitrate của file đầu vào. Sau đó, phần mềm tính bitrate mục tiêu theo công thức gần đúng:

```text
Bitrate = Dung lượng mục tiêu / Thời lượng âm thanh
```

Một hệ số an toàn được áp dụng để file đầu ra có khoảng dự phòng. Nếu file vẫn vượt giới hạn, phần mềm tự giảm bitrate và thực hiện nén lại, tối đa 8 lần.

## Thành phần sử dụng

- **Python**: ngôn ngữ lập trình chính.
- **CustomTkinter**: xây dựng giao diện hiện đại.
- **Tkinter**: hộp thoại chọn file và thông báo.
- **FFmpeg**: mã hóa và nén âm thanh.
- **FFprobe**: đọc thông tin kỹ thuật của file âm thanh.
- **Threading**: chạy tác vụ nén mà không làm treo giao diện.

## Lưu ý

- Không chọn cùng một đường dẫn cho file đầu vào và file đầu ra.
- File đầu ra hiện tại luôn có đuôi `.mp3`.
- Nếu file đầu ra đã tồn tại, phần mềm sẽ hỏi trước khi ghi đè.
- File đang nén chưa hoàn tất sẽ được xóa khi người dùng hủy hoặc khi có lỗi.
- Tốc độ xử lý phụ thuộc vào thời lượng file và hiệu năng máy tính.

## Chạy nhanh

Sau khi đã cài Python và FFmpeg:

```bash
git clone <URL_REPOSITORY>
cd <TEN_THU_MUC_REPOSITORY>
python -m venv .venv
.venv\Scripts\activate
pip install customtkinter
python MP3_Compress.py
```

## Giấy phép

Có thể bổ sung thông tin giấy phép sử dụng của dự án tại đây, ví dụ MIT License hoặc giấy phép nội bộ của doanh nghiệp.
