import sys
import os

def check_termux_usb_env():
    print("[*] در حال بررسی وضعیت محیطی پورت USB در ترموکس...")
    
    # بررسی وجود فایل‌های کتابخانه libusb
    lib_path = "/data/data/com.termux/files/usr/lib/libusb-1.0.so"
    if os.path.exists(lib_path):
        print(f"[+] فایل کتابخانه سیستم پیدا شد: {lib_path}")
    else:
        print("[-] کتابخانه libusb-1.0.so در مسیر اصلی نیست.")

    try:
        import usb.core
        import usb.backend.libusb1
        
        # تلاش برای بارگذاری صریح بک‌اند با هندل کردن خطای I/O
        print("[*] در حال مقداردهی اولیه به درایور USB...")
        devs = list(usb.core.find(find_all=True))
        
        if not devs:
            print("[-] هیچ دستگاهی روی باس USB شناسایی نشد. کابل OTG یا دانلود مود را چک کن.")
            return
            
        print(f"[+] تعداد {len(devs)} دستگاه روی باس پیدا شد:")
        for d in devs:
            print(f"    -> Vendor ID: {hex(d.idVendor)}, Product ID: {hex(d.idProduct)}")
            if d.idVendor == 0x04e8:
                print("[+] عجب! دستگاه سامسونگ توی دانلود مود صید شد!")
                
    except Exception as e:
        print(f"[!] خطای سطح دسترسی یا ارتباط سخت‌افزاری: {e}")
        print("[*] نکته: مطمئن شو کابل OTG محکم وصله و گوشی هدف دقیقاً توی صفحه Download Mode هست.")

if __name__ == "__main__":
    print("=" * 45)
    print("   بررسی‌کننده تخصصی پورت USB سامسونگ")
    print("=" * 45)
    check_termux_usb_env()
    print("=" * 45)

