import subprocess

def force_unlock_ui():
    print("[*] در حال باز کردن قفل سوییچ در رابط کاربری...")
    cmds = [
        "settings put secure oem_unlock_allowed 1",
        "settings put global oem_unlock_allowed 1",
        "am broadcast -a android.provider.Telephony.SECRET_CODE -d android_secret_code://276633683",
        "am force-stop com.android.settings"
    ]
    
    for cmd in cmds:
        try:
            res = subprocess.run(['sh', '-c', cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"[+] اجرا شد: {cmd}")
        except Exception as e:
            print(f"[!] خطا: {e}")

if __name__ == "__main__":
    force_unlock_ui()
