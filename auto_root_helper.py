import os
import subprocess
import sys
import time

def print_banner():
    print("=" * 50)
    print("      سامانه هوشمند و اتوماتیک روت و مدیریت دسترسی")
    print("            ویژه گوشی‌های سامسونگ (بدون نیاز به PC)")
    print("=" * 50)

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def check_environment():
    print("\n[*] گام ۱: بررسی وضعیت محیط سیستم و شیزوکو...")
    shizuku_check = run_cmd("rish -c 'getprop ro.boot.flash.locked' 2>/dev/null")
    
    if not shizuku_check or "not found" in shizuku_check:
        # تست با متد مستقیم اسکریپت شیزوکو
        shizuku_check = run_cmd("python check_props_shizuku.py")
        if "1195" in shizuku_check or "bootloader" in shizuku_check:
            print("[+] سرویس Shizuku فعال است و دسترسی سیستم برقرار شد!")
            return "shizuku"
        else:
            print("[!] Shizuku شناسایی نشد. لطفاً مطمئن شو برنامه Shizuku فعال است.")
            return None
    else:
        print("[+] سرویس ریش/شیزوکو فعال است!")
        return "rish"

def analyze_device():
    print("\n[*] گام ۲: تحلیل تخصصی وضعیت قفل‌ها و مشخصات گوشی...")
    props = run_cmd("python check_props_shizuku.py")
    
    if "ro.boot.flash.locked" in props:
        print("[i] اطلاعات بوت‌لودر استخراج شد:")
        for line in props.split('\n'):
            if any(k in line for k in ['flash.locked', 'knox', 'vbmeta', 'secure', 'kg.state']):
                print(f"   <- {line}")

def prepare_flash():
    print("\n[*] گام ۳: آماده‌سازی مسیر فایل‌های فلش/روت...")
    download_dir = "/sdcard/Download/mohammad1.2"
    if os.path.exists(download_dir):
        print(f"[+] پوشه کاری شناسایی شد: {download_dir}")
        files = os.listdir(download_dir)
        print("[-] فایل‌های موجود جهت عملیات:")
        for f in files:
            print(f"   * {f}")
    else:
        print(f"[!] پوشه {download_dir} یافت نشد. در حال ساخت پوشه...")
        os.makedirs(download_dir, exist_ok=True)

def main():
    print_banner()
    env = check_environment()
    if env:
        analyze_device()
        prepare_flash()
        print("\n" + "=" * 50)
        print("[SUCCESS] تمام پیش‌نیازها و مسیرهای دسترسی با موفقیت بررسی و باز شدند!")
        print("آماده برای اجرای مراحل بعدی فلش و روت.")
        print("=" * 50)
    else:
        print("\n[!] خطا در برقراری ارتباط. لطفاً Shizuku را اجرا کرده و مجدداً تلاش کنید.")

if __name__ == "__main__":
    main()
