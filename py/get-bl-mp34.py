import os
import re
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp


class BiliDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("小p站全能下载器 (Pro) powered by xxx © 2026-09-16")
        self.root.geometry("650x550")

        self.setup_ui()

        self.download_queue = []
        self.is_downloading = False

    def setup_ui(self):
        input_frame = tk.Frame(self.root, pady=10, padx=10)
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="合集/视频链接:").pack(anchor="w")
        self.url_entry = tk.Entry(input_frame, font=("微软雅黑", 10))
        self.url_entry.pack(fill="x", pady=5)
        self.url_entry.insert(0, "https://www.bilibili.com/video/BV1ct411W7kz/")

        setting_frame = tk.Frame(self.root, pady=5, padx=10)
        setting_frame.pack(fill="x")

        tk.Label(setting_frame, text="保存目录:").pack(anchor="w")
        path_frame = tk.Frame(setting_frame)
        path_frame.pack(fill="x", pady=5)

        self.path_var = tk.StringVar(value=os.getcwd())
        tk.Entry(path_frame, textvariable=self.path_var, state="readonly").pack(side="left", fill="x", expand=True)
        tk.Button(path_frame, text="浏览", command=self.select_path).pack(side="right", padx=5)

        # --- 模式选择 ---
        mode_frame = tk.Frame(setting_frame)
        mode_frame.pack(fill="x", pady=5)
        tk.Label(mode_frame, text="下载模式:").pack(side="left")

        self.mode_var = tk.StringVar(value="audio")
        self.mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var, state="readonly", width=15)
        self.mode_combo['values'] = ('提取音频 (MP3)', '下载视频 (MP4)')
        self.mode_combo.current(0)
        self.mode_combo.pack(side="left", padx=10)

        list_frame = tk.Frame(self.root, padx=10)
        list_frame.pack(fill="both", expand=True, pady=5)

        tk.Label(list_frame, text="下载队列:").pack(anchor="w")

        columns = ("status", "title")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        self.tree.heading("status", text="状态", anchor="center")
        self.tree.heading("title", text="文件名", anchor="w")
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("title", width=450, anchor="w")

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        bottom_frame = tk.Frame(self.root, pady=10, padx=10)
        bottom_frame.pack(fill="x")

        self.progress = ttk.Progressbar(bottom_frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=5)

        self.download_btn = tk.Button(bottom_frame, text="开始批量下载", bg="#4CAF50", fg="white",
                                      font=("微软雅黑", 10, "bold"), command=self.start_process)
        self.download_btn.pack(fill="x")

    def select_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def log(self, message):
        print(message)

    def sanitize_filename(self, name):
        """清理文件名中的非法字符"""
        return re.sub(r'[\\/:*?"<>|]', '_', name)

    def start_process(self):
        if self.is_downloading:
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("提示", "请输入链接")
            return

        self.is_downloading = True
        self.download_btn.config(text="正在解析...", state="disabled", bg="gray")
        self.progress.start(10)
        self.tree.delete(*self.tree.get_children())
        self.download_queue = []

        threading.Thread(target=self.parse_and_enqueue, args=(url,), daemon=True).start()

    def parse_and_enqueue(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            playlist_title = info.get('title', 'B站合集')
            entries = info.get('entries', [])

            if not entries:
                if info.get('title'):
                    entries = [info]
                else:
                    raise Exception("未找到可下载的视频")

            safe_playlist = self.sanitize_filename(playlist_title)
            self.log(f"ℹ️ 检测到合集: {playlist_title}，共 {len(entries)} 个视频")

            for i, entry in enumerate(entries):
                video_url = entry.get('url') or entry.get('webpage_url') or entry.get('id')
                if not video_url:
                    continue

                # 获取分P标题
                ep_title = entry.get('title', f'第{i + 1}P')

                # 清理分P标题：移除合集名称前缀，避免重复
                if ep_title.startswith(playlist_title):
                    ep_title = ep_title[len(playlist_title):].strip()

                # --- 新增：移除分P标题自带的序号前缀，如 "p13 " ---
                # 使用正则表达式匹配开头的 "p" + 数字 + 空格，并将其替换为空
                ep_title = re.sub(r'^p\d+\s*', '', ep_title, flags=re.IGNORECASE)

                # 清理非法字符
                safe_ep_title = self.sanitize_filename(ep_title)

                # 如果清理后标题为空，则使用序号兜底
                if not safe_ep_title:
                    safe_ep_title = f"第{i + 1}P"

                # 拼接格式：【合集标题】 p序号 【分P标题】
                p_num = i + 1
                base_filename = f"{safe_playlist} p{p_num:02d} {safe_ep_title}"

                self.download_queue.append({
                    'url': video_url if video_url.startswith('http') else f"https://www.bilibili.com/video/{video_url}",
                    'base_filename': base_filename,
                    'status': '等待中'
                })

            self.root.after(0, self.update_queue_ui)
            self.root.after(100, self.process_queue)

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("解析错误", str(e)))
            self.reset_ui()

    def update_queue_ui(self):
        mode = self.mode_var.get()
        ext = ".mp3" if "音频" in mode else ".mp4"
        for item in self.download_queue:
            self.tree.insert("", "end", values=(item['status'], item['base_filename'] + ext))

    def process_queue(self):
        if not self.download_queue:
            self.log("✅ 所有任务已完成")
            self.reset_ui()
            messagebox.showinfo("完成", "所有文件下载/提取完毕！")
            return

        task = self.download_queue.pop(0)
        task['status'] = '下载中'

        mode = self.mode_var.get()
        ext = ".mp3" if "音频" in mode else ".mp4"
        display_name = task['base_filename'] + ext
        self.update_item_status(display_name, '下载中')

        threading.Thread(target=self.download_single, args=(task,), daemon=True).start()

    def update_item_status(self, display_name, status):
        for child in self.tree.get_children():
            if self.tree.item(child, 'values')[1] == display_name:
                self.tree.item(child, values=(status, display_name))
                break

    def download_single(self, task):
        url = task['url']
        base_filename = task['base_filename']
        output_dir = self.path_var.get()

        mode = self.mode_var.get()
        is_audio_mode = "音频" in mode

        final_ext = ".mp3" if is_audio_mode else ".mp4"
        final_filename = base_filename + final_ext
        output_path = os.path.join(output_dir, final_filename)

        if os.path.exists(output_path):
            self.log(f"⏩ 文件已存在，跳过: {final_filename}")
            task['status'] = '已跳过'
            self.root.after(0, lambda: self.update_item_status(final_filename, '已跳过'))
            self.root.after(0, self.process_queue)
            return

        # yt-dlp 配置
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'outtmpl': os.path.join(output_dir, base_filename + '.%(ext)s'),
        }

        if is_audio_mode:
            ydl_opts.update({
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',  # 强制合并为mp4
            })

        try:
            self.log(f"🎵 正在处理: {final_filename}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            task['status'] = '完成'
            self.log(f"✅ 成功: {final_filename}")
            self.root.after(0, lambda: self.update_item_status(final_filename, '完成'))
        except Exception as e:
            task['status'] = '失败'
            self.log(f"❌ 失败 {final_filename}: {e}")
            self.root.after(0, lambda: self.update_item_status(final_filename, '失败'))
        finally:
            self.root.after(500, self.process_queue)

    def reset_ui(self):
        self.is_downloading = False
        self.download_btn.config(text="开始批量下载", state="normal", bg="#4CAF50")
        self.progress.stop()


if __name__ == "__main__":
    root = tk.Tk()
    app = BiliDownloader(root)
    root.mainloop()


# 打包发版
# pyinstaller get-bl-mp34.spec
'''
# get-bl-mp34.spec

# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['demo-mp34.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ffmpeg.exe', '.'),
        ('qrcode.png', '.'),
        # 这里的 'imageio-*.dist-info' 是为了通配版本号，比如 imageio-2.31.0.dist-info
        (r'.\.venv\Lib\site-packages\imageio', 'imageio'),
        (r'.\.venv\Lib\site-packages\imageio-2.37.3.dist-info', 'imageio-2.37.3.dist-info'),
        (r'.\.venv\Lib\site-packages\imageio_ffmpeg', 'imageio_ffmpeg'),
        (r'.\.venv\Lib\site-packages\imageio_ffmpeg-0.6.0.dist-info', 'imageio_ffmpeg-0.6.0.dist-info'),
        (r'.\.venv\Lib\site-packages\moviepy', 'moviepy'),
        (r'.\.venv\Lib\site-packages\moviepy-2.2.1.dist-info', 'moviepy-2.2.1.dist-info'),
    ],
    hiddenimports=[
        # --- 你的其他库 ---
        'yt_dlp',
        'yt_dlp.compat',
        'yt_dlp.utils',
        'Cryptodome',
        'mutagen',
        'imageio_ffmpeg',

        # --- 必须添加的 MoviePy 全家桶 ---
        'moviepy',
        'moviepy.audio',
        'moviepy.audio.AudioClip',
        'moviepy.audio.io',
        'moviepy.audio.io.ffmpeg_audiowriter',
        'moviepy.audio.io.AudioFileClip',
        'moviepy.video',
        'moviepy.video.io',
        'moviepy.video.io.ffmpeg_tools',
        'moviepy.video.io.VideoFileClip',
        'moviepy.editor',  # 很多代码依赖这个入口
        'moviepy.config',

        # --- 依赖库 ---
        'proglog',
        'decorator',
        'imageio',
        'imageio.plugins.ffmpeg',
        'numpy',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='小p站全能下载器 (Pro)',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='favicon.ico',
)
'''

