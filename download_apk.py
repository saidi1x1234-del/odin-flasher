import requests
import json
import os

print("=" * 50)
print("      در حال استعلام و دانلود مستقیم APK از گیت‌هاب")
print("=" * 50)

repo = "saidi1x1234-del/odin-flasher"
url = f"https://api.github.com/repos/{repo}/releases/latest"

try:
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        assets = data.get("assets", [])
        if assets:
            download_url = assets[0]["browser_download_url"]
            file_name = assets[0]["name"]
            print(f"[+] فایل شناسایی شد: {file_name}")
            print("[*] در حال دانلود فایل APK...")
            
            apk_data = requests.get(download_url)
            save_path = os.path.join("/sdcard/Download/mohammad1.2", file_name)
            with open(save_path, "wb") as f:
                f.write(apk_data.content)
            
            print(f"[SUCCESS] فایل APK با موفقیت دانلود شد در:\n{save_path}")
            print("حالا می‌تونی مستقیم از مدیریت فایل نصبش کنی!")
        else:
            print("[!] فایل APK هنوز آماده نشده است. سرور در حال کامپایل می‌باشد.")
            print("لطفاً ۲ تا ۳ دقیقه صبر کن و دوباره اسکریپت را اجرا کن.")
    else:
        print("[!] فرآیند بیلد هنوز روی گیت‌هاب در حال انجام است...")
        print("چند دقیقه زمان می‌بره تا سرور فایل اولیه را ریلیز کند.")
except Exception as e:
    print(f"[!] خطا در ارتباط: {e}")

print("=" * 50)
