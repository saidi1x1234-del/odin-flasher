import requests
import time
import os

repo = "saidi1x1234-del/odin-flasher"
releases_url = f"https://api.github.com/repos/{repo}/releases"
runs_url = f"https://api.github.com/repos/{repo}/actions/runs"
save_dir = "/sdcard/Download/mohammad1.2"

print("=" * 50)
print("   پایش هوشمند گیت‌هاب برای ساخت و دانلود APK...")
print("   (هر ۱۵ ثانیه وضعیت بررسی می‌شود)")
print("=" * 50)

while True:
    try:
        # ۱. اول وضعیت آخرین بیلد را چک می‌کنیم
        runs_res = requests.get(runs_url, timeout=10)
        if runs_res.status_code == 200:
            runs = runs_res.json().get("workflow_runs", [])
            if runs:
                latest_run = runs[0]
                status = latest_run.get("status")
                conclusion = latest_run.get("conclusion")
                print(f"[وضعیت بیلد: {status} | نتیجه: {conclusion}]", end="\r", flush=True)
                
                if status == "completed":
                    if conclusion == "success":
                        print("\n[+] بیلد با موفقیت تمام شد! در حال دریافت فایل...")
                        break
                    elif conclusion == "failure":
                        print("\n[!] بیلد با خطا مواجه شد. لطفاً لاگ گیت‌هاب را بررسی کنید.")
                        break
        
        # ۲. چک کردن ریلیز برای دانلود مستقیم
        res = requests.get(releases_url, timeout=10)
        if res.status_code == 200:
            releases = res.json()
            if releases:
                assets = releases[0].get("assets", [])
                if assets:
                    download_url = assets[0]["browser_download_url"]
                    file_name = assets[0]["name"]
                    print(f"\n[+] فایل APK پیدا شد: {file_name}")
                    print("[*] در حال دانلود روی گوشی...")
                    
                    apk_res = requests.get(download_url, stream=True)
                    save_path = os.path.join(save_dir, file_name)
                    with open(save_path, "wb") as f:
                        for chunk in apk_res.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    print("=" * 50)
                    print(f"✅ دانلود با موفقیت انجام شد!")
                    print(f"📁 مسیر ذخیره: {save_path}")
                    print("=" * 50)
                    break
    except Exception as e:
        print(f"ع", end="", flush=True)
    
    time.sleep(15)
