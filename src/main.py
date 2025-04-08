import ctypes
import os
import shutil
import subprocess
import sys
import threading
import winsound

'''
部分文件注释
music.wav为本地音频名（需要有同包下同名文件）
op.exe为安装包名（同上）
并且无论如何都不建议填绝对路径
'''



def is_admin():

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():

    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([f'"{param}"' for param in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit()


def resource(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def music_installer():
    music_path=resource("music.wav")
    desktop = os.path.expanduser("~/Desktop")  # 动态获取桌面路径
    dest_path = os.path.join(desktop, "music.wav")

    try:
        shutil.copyfile(music_path, dest_path)
        return dest_path
    except Exception as c:
        print(f"释放音乐包失败: {c}")
        return None

def run_installer():
    installer_src =resource("op.exe")
    desktop = os.path.expanduser("~/Desktop")  # 动态获取桌面路径
    dest_path = os.path.join(desktop, "op.exe")

    try:
        shutil.copyfile(installer_src, dest_path)
        return dest_path
    except Exception as e:
        print(f"释放安装包失败: {e}")
        return None

def open_install():
    op_path = os.path.expanduser("~/Desktop/op.exe")
    try:
        subprocess.Popen([op_path])
    except Exception as e:
        print(f"打开安装包失败: {e}")

def play_music():
    music_path = music_installer()
    if music_path:
        winsound.PlaySound(music_path, winsound.SND_FILENAME)


if __name__ == '__main__':
    run_as_admin()
    try:
        run_installer()
        music_installer()

        install_thread = threading.Thread(target=open_install)
        music_thread = threading.Thread(target=play_music)

        install_thread.start()
        music_thread.start()

        install_thread.join()
        music_thread.join()
    except Exception as e:
        print(f"程序运行出错: {e}")



'''
Power By Voltucit
'''