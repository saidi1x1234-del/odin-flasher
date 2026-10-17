import os
import subprocess

def scan_ports():
    print("[*] در حال جستجوی پورت‌های AT و سریال سیستم...")
    potential_paths = ['/dev/', '/dev/radio/', '/dev/stty', '/dev/umts_at']
    found = []
    
    # جستجو در مسیرهای احتمالی پورت‌های سامسونگ
    try:
        res = subprocess.run(['ls', '-l'] + [p for p in ['/dev/radio', '/dev/stty_at', '/dev/ttyACM0', '/dev/ttyHS3'] if os.path.exists(p)], 
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(res.stdout)
    except Exception as e:
        print(f"[!] خطا: {e}")

    # بررسی فایل‌های سیستمی برای پورت‌های مودم
    print("\n[*] بررسی گره‌های فعال مودم:")
    for root, dirs, files in os.walk('/dev'):
        for f in files:
            if 'at' in f.lower() or 'modem' in f.lower() or 'tty' in f.lower():
                full_path = os.path.join(root, f)
                if any(x in full_path for x in ['radio', 'stty', 'ACM', 'umts', 'at']):
                    found.append(full_path)
                    
    for p in sorted(set(found))[:15]:
        print(f"  [+] پورت پیدا شد: {p}")

if __name__ == "__main__":
    scan_ports()
