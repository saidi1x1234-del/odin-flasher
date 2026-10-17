import requests
import time
import os

repo = "saidi1x1234-del/odin-flasher"
url = f"https://api.github.com/repos/{repo}/releases/latest"
save_dir = "/sdcard/Download/mohammad1.2"

print("=" * 50)
print("   در حال پایش خودکار گیت‌هاب برای دانلود APK...")
print("   (هر ۱۵ ثانیه چک می‌شود؛ لطفاً منتظر بمانید)")
print("=" * 50)

while True:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            assets = data.get("assets", [])
            if assets:
                download_url = assets[0]["browser_download_url"]
                file_name = assets[0]["name"]
                print(f"\n[+] فایل APK روی گیت‌هاب آماده شد: {file_name}")
                print("[*] در حال دانلود فایل به داخل گوشی...")
                
                apk_data = requests.get(download_url)
                save_path = os.path.join(save_dir, file_name)
                with open(save_path, "wb") as f:
                    f.write(apk_data.content)
                
                print("\n==================================================")
                print(f"[SUCCESS] دانلود با موفقیت انجام شد!")
                print(f"مسیر فایل: {save_path}")
                print("می‌توانی مستقیم از مدیریت فایل آن را نصب کنی.")
                print("==================================================")
                break
            else:
                print(".", end="", flush=True)
        else:
            print(".", end="", flush=True)
    except Exception as e:
        print("x", end="", flush=True)
    
    time.sleep(15)
