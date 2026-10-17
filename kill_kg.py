import subprocess

def stop_kg():
    print("[*] در حال متوقف کردن سرویس‌های Knox Guard...")
    cmds = [
        "stop kgtaserv",
        "setprop init.svc.kgtaserv stopped",
        "setprop knox.kg.state Normal",
        "setprop ro.boot.flash.locked 0",
        "setprop ro.boot.vbmeta.device_state unlocked"
    ]
    
    for cmd in cmds:
        try:
            res = subprocess.run(['su', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode != 0:
                # اگر su نبود با شیزوکو/sh امتحان می‌کنیم
                subprocess.run(['sh', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"[+] اجرا شد: {cmd}")
        except Exception as e:
            print(f"[!] خطا در {cmd}: {e}")

if __name__ == "__main__":
    stop_kg()
