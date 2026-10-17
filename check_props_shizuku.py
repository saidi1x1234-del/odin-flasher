import subprocess

def get_props():
    print("[*] در حال دریافت پراپرتی‌ها از طریق رابط سیستم...")
    try:
        # استفاده از دستور مستقیم getprop با دسترسی شیزوکو/ADB
        result = subprocess.run(['getprop'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=5)
        lines = result.stdout.splitlines()
        print(f"\n[*] کل پراپرتی‌های دریافتی: {len(lines)}")
        
        matched = [l for l in lines if any(k in l.lower() for k in ['oem', 'unlock', 'flash', 'lock', 'kg', 'secure', 'factory'])]
        
        print("\n[*] نتایج فیلتر شده مرتبط با قفل و آنلاک:")
        if matched:
            for m in matched:
                print(f"  {m}")
        else:
            print("  [!] کلیدواژه‌ای پیدا نشد. ۵ خط اول سیستم:")
            for l in lines[:5]:
                print(f"  {l}")
    except Exception as e:
        print(f"[!] خطا: {e}")

if __name__ == "__main__":
    get_props()
