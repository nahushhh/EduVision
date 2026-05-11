import platform
import threading

def play_success():
    if platform.system() == "Windows":
        import winsound
        def _play():
            winsound.Beep(1000, 200)
            winsound.Beep(1500, 300)
        threading.Thread(target=_play, daemon=True).start()

def play_fail():
    if platform.system() == "Windows":
        import winsound
        def _play():
            winsound.Beep(300, 500)
        threading.Thread(target=_play, daemon=True).start()
