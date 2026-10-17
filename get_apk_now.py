import requests
import json
import os

print("=" * 50)
print("      در حال دریافت مستقیم لینک فایل APK ریلیز شده")
print("=" * 50)

repo = "saidi1x1234-del/odin-flasher"
# دریافت آخرین ریلیزها بدون نیاز به توکن
url = f"https://api.github.com/repos/{repo}/releases"
headers = {'User-Agent': 'Mozilla/5.0'}

try:
    res = requests.get(url, headers=headers, timeout=15)
    if res.status_code == 200:
        releases = res.json()
        if len(releases) > 0:
            latest = releases[0]
            assets = latest.get("assets", [])
            if assets:
                download_url = assets[0]["browser_download_url"]
                file_name = assets[0]["name"]
                print(f"[+] فایل پیدا شد: {file_name}")
                print("[*] در حال دانلود و ذخیره‌سازی در پوشه دانلودها...")
                
                apk_res = requests.get(download_url, headers=headers, stream=True)
                save_path = f"/sdcard/Download/mohammad1.2/{file_name}"
                with open(save_path, "wb") as f:
                    for chunk in apk_res.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                print("\n" + "=" * 50)
                print(f"✅ دانلود با موفقیت کامل شد!")
                print(f"📁 مسیر فایل نصب: {save_path}")
                print("=" * 50)
            else:
                print("[!] ریلیز ساخته شده اما فایل APK هنوز کامل آپلود نشده. ۱۰ ثانیه دیگه تست کن.")
        else:
            print("[!] هیچ ریلیزی پیدا نشد.")
    else:
        print(f"[!] خطا در دریافت اطلاعات: کد {res.status_code}")
except Exception as e:
    print(f"[!] خطا در اتصال: {e}")
