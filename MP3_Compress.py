import json
import os
import shutil
import subprocess
import sys
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class MP3CompressorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MP3 Compressor")
        self.geometry("760x650")
        self.minsize(720, 610)

        self.input_file = ""
        self.output_file = ""
        self.audio_duration = 0.0
        self.process = None
        self.is_compressing = False
        self.cancel_requested = False

        self.create_ui()
        self.check_ffmpeg_on_start()

    def create_ui(self):
        # =========================
        # Header
        # =========================
        header_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=("#EAF3FF", "#12233D"),
        )
        header_frame.pack(fill="x")

        ctk.CTkLabel(
            header_frame,
            text="MP3 COMPRESSOR",
            font=ctk.CTkFont(size=27, weight="bold"),
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            header_frame,
            text="Nén file âm thanh xuống dưới giới hạn dung lượng của website",
            font=ctk.CTkFont(size=14),
            text_color=("gray35", "gray75"),
        ).pack(pady=(0, 24))

        # =========================
        # Main content
        # =========================
        main_frame = ctk.CTkFrame(self, corner_radius=16)
        main_frame.pack(fill="both", expand=True, padx=24, pady=20)

        # File đầu vào
        ctk.CTkLabel(
            main_frame,
            text="1. Chọn file MP3",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=22, pady=(22, 8))

        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=22)

        self.input_entry = ctk.CTkEntry(
            input_frame,
            height=42,
            placeholder_text="Chưa chọn file MP3...",
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.choose_file_button = ctk.CTkButton(
            input_frame,
            text="Chọn file",
            width=120,
            height=42,
            command=self.choose_input_file,
        )
        self.choose_file_button.pack(side="right")

        # Thông tin file
        self.file_info_label = ctk.CTkLabel(
            main_frame,
            text="Kích thước: -- | Thời lượng: -- | Bitrate: --",
            anchor="w",
            text_color=("gray40", "gray70"),
        )
        self.file_info_label.pack(fill="x", padx=22, pady=(8, 15))

        # Cài đặt
        ctk.CTkLabel(
            main_frame,
            text="2. Thiết lập nén",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=22, pady=(6, 8))

        settings_frame = ctk.CTkFrame(main_frame)
        settings_frame.pack(fill="x", padx=22)

        # Target size
        target_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        target_frame.pack(fill="x", padx=15, pady=(14, 8))

        ctk.CTkLabel(
            target_frame,
            text="Dung lượng tối đa:",
            width=160,
            anchor="w",
        ).pack(side="left")

        self.target_size_entry = ctk.CTkEntry(
            target_frame,
            width=110,
            height=36,
        )
        self.target_size_entry.insert(0, "190")
        self.target_size_entry.pack(side="left")

        ctk.CTkLabel(
            target_frame,
            text="MB",
            anchor="w",
        ).pack(side="left", padx=(8, 0))

        ctk.CTkLabel(
            target_frame,
            text="Khuyến nghị 190 MB để tránh lỗi giới hạn 200 MB",
            text_color=("gray45", "gray65"),
        ).pack(side="right")

        # Mono option
        mono_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        mono_frame.pack(fill="x", padx=15, pady=(8, 14))

        self.mono_variable = ctk.BooleanVar(value=False)

        self.mono_checkbox = ctk.CTkCheckBox(
            mono_frame,
            text="Chuyển sang Mono",
            variable=self.mono_variable,
        )
        self.mono_checkbox.pack(side="left")

        ctk.CTkLabel(
            mono_frame,
            text="Phù hợp với ghi âm, cuộc họp, podcast và giọng nói",
            text_color=("gray45", "gray65"),
        ).pack(side="right")

        # File đầu ra
        ctk.CTkLabel(
            main_frame,
            text="3. Vị trí lưu file",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=22, pady=(20, 8))

        output_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        output_frame.pack(fill="x", padx=22)

        self.output_entry = ctk.CTkEntry(
            output_frame,
            height=42,
            placeholder_text="File đầu ra sẽ tự động được tạo...",
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.choose_output_button = ctk.CTkButton(
            output_frame,
            text="Chọn nơi lưu",
            width=120,
            height=42,
            command=self.choose_output_file,
        )
        self.choose_output_button.pack(side="right")

        # Progress
        self.progress_bar = ctk.CTkProgressBar(main_frame, height=14)
        self.progress_bar.pack(fill="x", padx=22, pady=(28, 8))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Sẵn sàng",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.status_label.pack(pady=(2, 4))

        self.detail_label = ctk.CTkLabel(
            main_frame,
            text="Hãy chọn một file MP3 để bắt đầu.",
            text_color=("gray40", "gray70"),
        )
        self.detail_label.pack(pady=(0, 15))

        # Action buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=22, pady=(5, 22))

        self.compress_button = ctk.CTkButton(
            button_frame,
            text="Bắt đầu nén",
            height=48,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.start_compression,
        )
        self.compress_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8),
        )

        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Hủy",
            width=100,
            height=48,
            fg_color="#B3261E",
            hover_color="#8C1D18",
            state="disabled",
            command=self.cancel_compression,
        )
        self.cancel_button.pack(side="left", padx=8)

        self.open_folder_button = ctk.CTkButton(
            button_frame,
            text="Mở thư mục",
            width=120,
            height=48,
            state="disabled",
            command=self.open_output_folder,
        )
        self.open_folder_button.pack(side="right", padx=(8, 0))

    def run_command(self, command):
        creation_flags = 0

        if os.name == "nt":
            creation_flags = subprocess.CREATE_NO_WINDOW

        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            creationflags=creation_flags,
        )

    def check_ffmpeg_on_start(self):
        ffmpeg_exists = shutil.which("ffmpeg")
        ffprobe_exists = shutil.which("ffprobe")

        if not ffmpeg_exists or not ffprobe_exists:
            self.after(
                500,
                lambda: messagebox.showwarning(
                    "Chưa tìm thấy FFmpeg",
                    "Ứng dụng chưa tìm thấy FFmpeg hoặc FFprobe.\n\n"
                    "Hãy cài FFmpeg và thêm thư mục bin vào PATH.",
                ),
            )

    def choose_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file MP3",
            filetypes=[
                ("MP3 files", "*.mp3"),
                ("Audio files", "*.mp3 *.wav *.m4a *.aac *.flac"),
                ("All files", "*.*"),
            ],
        )

        if not file_path:
            return

        self.input_file = file_path

        self.input_entry.delete(0, "end")
        self.input_entry.insert(0, file_path)

        input_path = Path(file_path)
        default_output = (
            input_path.parent
            / f"{input_path.stem}_compressed.mp3"
        )

        self.output_file = str(default_output)
        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, self.output_file)

        self.open_folder_button.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Đang đọc thông tin file...")
        self.detail_label.configure(text="Vui lòng chờ trong giây lát.")

        threading.Thread(
            target=self.load_audio_information,
            daemon=True,
        ).start()

    def choose_output_file(self):
        initial_name = "compressed.mp3"

        if self.input_file:
            input_path = Path(self.input_file)
            initial_name = f"{input_path.stem}_compressed.mp3"

        file_path = filedialog.asksaveasfilename(
            title="Chọn nơi lưu file",
            defaultextension=".mp3",
            initialfile=initial_name,
            filetypes=[("MP3 files", "*.mp3")],
        )

        if not file_path:
            return

        self.output_file = file_path
        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, file_path)

    def load_audio_information(self):
        try:
            information = self.get_audio_information(self.input_file)

            self.audio_duration = information["duration"]
            file_size_mb = os.path.getsize(self.input_file) / 1024 / 1024
            bitrate_kbps = information["bitrate"] / 1000

            duration_text = self.format_duration(self.audio_duration)

            info_text = (
                f"Kích thước: {file_size_mb:.2f} MB"
                f"  |  Thời lượng: {duration_text}"
                f"  |  Bitrate: {bitrate_kbps:.0f} kbps"
            )

            self.after(
                0,
                lambda: self.file_info_label.configure(text=info_text),
            )
            self.after(
                0,
                lambda: self.status_label.configure(text="Đã tải file"),
            )
            self.after(
                0,
                lambda: self.detail_label.configure(
                    text="Bạn có thể thiết lập dung lượng và bắt đầu nén."
                ),
            )

        except Exception as error:
            self.after(
                0,
                lambda: messagebox.showerror(
                    "Không đọc được file",
                    str(error),
                ),
            )
            self.after(
                0,
                lambda: self.status_label.configure(text="Có lỗi xảy ra"),
            )

    def get_audio_information(self, file_path):
        command = [
            "ffprobe",
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            file_path,
        ]

        result = self.run_command(command)

        if result.returncode != 0:
            raise RuntimeError(
                "Không thể đọc thông tin file âm thanh.\n"
                "Hãy kiểm tra FFmpeg hoặc thử chọn file khác."
            )

        data = json.loads(result.stdout)
        file_format = data.get("format", {})

        duration = float(file_format.get("duration", 0))
        bitrate = float(file_format.get("bit_rate", 0))

        if duration <= 0:
            raise RuntimeError("Không xác định được thời lượng file.")

        return {
            "duration": duration,
            "bitrate": bitrate,
        }

    def validate_inputs(self):
        self.input_file = self.input_entry.get().strip()
        self.output_file = self.output_entry.get().strip()

        if not self.input_file:
            messagebox.showwarning(
                "Thiếu file đầu vào",
                "Hãy chọn file MP3 cần nén.",
            )
            return None

        if not os.path.isfile(self.input_file):
            messagebox.showerror(
                "Không tìm thấy file",
                "File đầu vào không tồn tại.",
            )
            return None

        if not self.output_file:
            messagebox.showwarning(
                "Thiếu file đầu ra",
                "Hãy chọn vị trí lưu file sau nén.",
            )
            return None

        if not self.output_file.lower().endswith(".mp3"):
            self.output_file += ".mp3"
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, self.output_file)

        try:
            target_size_mb = float(
                self.target_size_entry.get().strip()
            )
        except ValueError:
            messagebox.showerror(
                "Dung lượng không hợp lệ",
                "Dung lượng tối đa phải là một số.",
            )
            return None

        if target_size_mb <= 0:
            messagebox.showerror(
                "Dung lượng không hợp lệ",
                "Dung lượng tối đa phải lớn hơn 0 MB.",
            )
            return None

        if Path(self.input_file).resolve() == Path(
            self.output_file
        ).resolve():
            messagebox.showerror(
                "File đầu ra không hợp lệ",
                "File đầu ra phải khác file đầu vào.",
            )
            return None

        if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
            messagebox.showerror(
                "Thiếu FFmpeg",
                "Không tìm thấy FFmpeg hoặc FFprobe trong PATH.",
            )
            return None

        return target_size_mb

    def start_compression(self):
        if self.is_compressing:
            return

        target_size_mb = self.validate_inputs()

        if target_size_mb is None:
            return

        if os.path.exists(self.output_file):
            overwrite = messagebox.askyesno(
                "File đã tồn tại",
                "File đầu ra đã tồn tại. Bạn có muốn ghi đè không?",
            )

            if not overwrite:
                return

        output_parent = Path(self.output_file).parent
        output_parent.mkdir(parents=True, exist_ok=True)

        self.is_compressing = True
        self.cancel_requested = False

        self.compress_button.configure(state="disabled")
        self.choose_file_button.configure(state="disabled")
        self.choose_output_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.open_folder_button.configure(state="disabled")

        self.progress_bar.set(0)
        self.status_label.configure(text="Đang chuẩn bị nén...")
        self.detail_label.configure(text="Đang tính toán bitrate phù hợp.")

        threading.Thread(
            target=self.compress_audio,
            args=(target_size_mb,),
            daemon=True,
        ).start()

    def calculate_bitrate(
        self,
        duration_seconds,
        target_size_mb,
        safety_factor=0.94,
    ):
        target_bits = target_size_mb * 1024 * 1024 * 8
        bitrate_bps = target_bits / duration_seconds
        bitrate_kbps = int(
            (bitrate_bps / 1000) * safety_factor
        )

        return max(16, min(bitrate_kbps, 320))

    def compress_audio(self, target_size_mb):
        try:
            if self.audio_duration <= 0:
                info = self.get_audio_information(self.input_file)
                self.audio_duration = info["duration"]

            bitrate_kbps = self.calculate_bitrate(
                self.audio_duration,
                target_size_mb,
            )

            maximum_attempts = 8

            for attempt in range(1, maximum_attempts + 1):
                if self.cancel_requested:
                    raise InterruptedError(
                        "Quá trình nén đã được hủy."
                    )

                self.update_status(
                    f"Đang nén lần {attempt}/{maximum_attempts}",
                    f"Bitrate hiện tại: {bitrate_kbps} kbps",
                )

                success = self.run_ffmpeg_with_progress(
                    bitrate_kbps
                )

                if not success:
                    if self.cancel_requested:
                        raise InterruptedError(
                            "Quá trình nén đã được hủy."
                        )

                    raise RuntimeError(
                        "FFmpeg không thể nén file âm thanh."
                    )

                output_size_mb = (
                    os.path.getsize(self.output_file)
                    / 1024
                    / 1024
                )

                if output_size_mb <= target_size_mb:
                    self.after(
                        0,
                        lambda: self.compression_completed(
                            output_size_mb,
                            bitrate_kbps,
                        ),
                    )
                    return

                bitrate_kbps = int(bitrate_kbps * 0.90)

                if bitrate_kbps < 16:
                    break

            raise RuntimeError(
                f"Không thể nén file xuống dưới "
                f"{target_size_mb:.2f} MB.\n"
                "File có thể quá dài hoặc giới hạn dung lượng quá thấp."
            )

        except InterruptedError:
            self.delete_incomplete_output()

            self.after(
                0,
                lambda: self.reset_interface(
                    "Đã hủy quá trình nén.",
                    success=False,
                ),
            )

        except Exception as error:
            self.delete_incomplete_output()

            self.after(
                0,
                lambda: messagebox.showerror(
                    "Nén file thất bại",
                    str(error),
                ),
            )

            self.after(
                0,
                lambda: self.reset_interface(
                    "Nén file thất bại.",
                    success=False,
                ),
            )

    def run_ffmpeg_with_progress(self, bitrate_kbps):
        command = [
            "ffmpeg",
            "-y",
            "-i",
            self.input_file,
            "-vn",
            "-map_metadata",
            "-1",
            "-codec:a",
            "libmp3lame",
            "-b:a",
            f"{bitrate_kbps}k",
        ]

        if self.mono_variable.get():
            command.extend(["-ac", "1"])

        command.extend(
            [
                "-progress",
                "pipe:1",
                "-nostats",
                self.output_file,
            ]
        )

        creation_flags = 0

        if os.name == "nt":
            creation_flags = subprocess.CREATE_NO_WINDOW

        self.process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            bufsize=1,
            universal_newlines=True,
            creationflags=creation_flags,
        )

        while True:
            if self.cancel_requested:
                self.process.terminate()
                return False

            line = self.process.stdout.readline()

            if not line:
                if self.process.poll() is not None:
                    break
                continue

            line = line.strip()

            if line.startswith("out_time_ms="):
                try:
                    time_microseconds = int(
                        line.split("=", 1)[1]
                    )
                    current_seconds = (
                        time_microseconds / 1_000_000
                    )

                    progress = current_seconds / self.audio_duration
                    progress = max(0.0, min(progress, 1.0))

                    percent = int(progress * 100)

                    self.after(
                        0,
                        lambda value=progress: self.progress_bar.set(
                            value
                        ),
                    )

                    self.after(
                        0,
                        lambda value=percent: self.detail_label.configure(
                            text=f"Đang xử lý âm thanh: {value}%"
                        ),
                    )

                except ValueError:
                    pass

        return self.process.returncode == 0

    def cancel_compression(self):
        if not self.is_compressing:
            return

        confirm = messagebox.askyesno(
            "Hủy quá trình",
            "Bạn có chắc chắn muốn dừng quá trình nén không?",
        )

        if not confirm:
            return

        self.cancel_requested = True
        self.cancel_button.configure(state="disabled")
        self.status_label.configure(text="Đang hủy...")
        self.detail_label.configure(
            text="Đang dừng tiến trình FFmpeg."
        )

        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
            except Exception:
                pass

    def compression_completed(
        self,
        output_size_mb,
        bitrate_kbps,
    ):
        self.progress_bar.set(1)

        self.status_label.configure(
            text="Nén file thành công!"
        )

        self.detail_label.configure(
            text=(
                f"Dung lượng: {output_size_mb:.2f} MB"
                f"  |  Bitrate: {bitrate_kbps} kbps"
            )
        )

        self.reset_controls()
        self.open_folder_button.configure(state="normal")

        messagebox.showinfo(
            "Hoàn thành",
            "Nén file thành công.\n\n"
            f"Dung lượng sau nén: {output_size_mb:.2f} MB\n"
            f"Bitrate: {bitrate_kbps} kbps\n\n"
            f"File lưu tại:\n{self.output_file}",
        )

    def reset_interface(self, detail_text, success=False):
        if not success:
            self.progress_bar.set(0)

        self.status_label.configure(
            text="Sẵn sàng" if not success else "Hoàn thành"
        )
        self.detail_label.configure(text=detail_text)
        self.reset_controls()

    def reset_controls(self):
        self.is_compressing = False
        self.process = None

        self.compress_button.configure(state="normal")
        self.choose_file_button.configure(state="normal")
        self.choose_output_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")

    def update_status(self, status, detail):
        self.after(
            0,
            lambda: self.status_label.configure(text=status),
        )
        self.after(
            0,
            lambda: self.detail_label.configure(text=detail),
        )

    def delete_incomplete_output(self):
        try:
            if self.output_file and os.path.exists(
                self.output_file
            ):
                os.remove(self.output_file)
        except OSError:
            pass

    def open_output_folder(self):
        if not self.output_file:
            return

        folder_path = str(Path(self.output_file).parent)

        try:
            if sys.platform.startswith("win"):
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", folder_path])
            else:
                subprocess.Popen(["xdg-open", folder_path])

        except Exception as error:
            messagebox.showerror(
                "Không mở được thư mục",
                str(error),
            )

    @staticmethod
    def format_duration(seconds):
        total_seconds = int(seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        remaining_seconds = total_seconds % 60

        if hours > 0:
            return (
                f"{hours:02d}:"
                f"{minutes:02d}:"
                f"{remaining_seconds:02d}"
            )

        return f"{minutes:02d}:{remaining_seconds:02d}"


if __name__ == "__main__":
    app = MP3CompressorApp()
    app.mainloop()