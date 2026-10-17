import subprocess

def check_usb_with_root():
    print("[*] در حال بررسی پورت USB با دسترسی روت...")
    try:
        # استفاده از روت برای گرفتن لیست دستگاه‌های USB متصل از طریق OTG
        result = subprocess.run(["su", "-c", "lsusb"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[+] خروجی پورت‌های متصل:\n{result.stdout.strip()}")
            if "04e8" in result.stdout:
                print("[+] عجب! سامسونگ توی دانلود مود با موفقیت روی پورت شنت شد!")
            else:
                print("[-] دستگاه سامسونگ توی لیست دیده نشد. کابل OTG یا اتصال رو چک کن.")
        else:
            print("[-] نتونست دستور روت رو اجرا کنه. دسترسی su رو چک کن داداش.")
    except Exception as e:
        print(f"[!] خطا در اجرای لایه سخت‌افزاری: {e}")

if __name__ == "__main__":
    print("--- ردیاب سخت‌افزاری پورت OTG سامسونگ ---")
    check_usb_with_root()

