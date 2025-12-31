import os
import tkinter as tk
from PIL import Image, ImageTk
from tkintervideo.player import Player

app = tk.Tk()
app.title("Video Opener")

try:
    icon_path = os.path.join(os.path.dirname(__file__), 'WishIKnew.png')
    if os.path.exists(icon_path):
        icon_img = Image.open(icon_path)
        icon_img = icon_img.resize((64, 64), Image.LANCZOS)
        icon_tk = ImageTk.PhotoImage(icon_img)
        app.iconphoto(True, icon_tk)
        app._icon_image = icon_tk  
except Exception as e:
    print('Window icon load failed:', e)


def play_video():
    file_path = '/home/wiktorus/WISH I KNEW/WishIKnew.mp4'  #change the file path to ours
    if os.path.exists(file_path):
        os.makedirs('cache', exist_ok=True)
        videoplayer = Player(master=app)
        videoplayer.load(file_path)
        videoplayer.loop = True
        app.videoplayer = videoplayer

        logo_h = 0

        screen_w = app.winfo_screenwidth()
        screen_h = app.winfo_screenheight()
        vid_w = getattr(videoplayer, 'video_w', getattr(videoplayer, 'video_size')[0])
        vid_h = getattr(videoplayer, 'video_h', getattr(videoplayer, 'video_size')[1])

        max_vid_h = max(0, screen_h - logo_h)
        width = min(int(vid_w), screen_w)
        height = min(int(vid_h), max_vid_h)

        videoplayer.playback_w = width
        videoplayer.playback_h = height

        x = (screen_w - width) // 2
        y = (screen_h - (height + logo_h)) // 2
        app.geometry(f"{width}x{height + logo_h}+{x}+{y}")
        app.resizable(False, False)

        videoplayer.pack(expand=True, fill="both")
        videoplayer.play()
    else:
        print("Video file does not exist.")


def on_close():
    vp = getattr(app, 'videoplayer', None)
    if vp:
        try:
            vp._player_exit = True
            vp.stop()
            if getattr(vp, 'play_thread', None):
                vp.play_thread.join(timeout=0.5)
        except Exception:
            pass
    app.destroy()
    try:
        import os, sys
        os._exit(0)
    except Exception:
        try:
            sys.exit(0)
        except Exception:
            pass


def start_title_marquee(root, text, delay=150):
    s = text + "    "
    i = 0
    def tick():
        nonlocal i
        i = (i + 1) % len(s)
        try:
            root.title(s[i:] + s[:i])
            root.after(delay, tick)
        except tk.TclError:
            return
    tick()

app.after(0, lambda: start_title_marquee(app, "oh oh wish i wish i knew knew knew ", 150))

app.after(0, play_video)

app.protocol("WM_DELETE_WINDOW", on_close)

app.mainloop()
