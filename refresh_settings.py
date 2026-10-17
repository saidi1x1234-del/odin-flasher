import socket
import struct

def refresh_ui():
    port = 44411
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(('127.0.0.1', port))
    except Exception as e:
        print(f"[!] خطا: {e}")
        return

    cmd_id = 0x4e584e43
    s.sendall(struct.pack('<IIIIII', cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff) + b'host::\0')
    try:
        s.recv(1024)
    except:
        pass

    # بستن اجباری تنظیمات و ارسال سیگنال راه‌اندازی مجدد برای ریلود شدن پراپرتی‌ها
    c = b'shell:am force-stop com.android.settings && am broadcast -a android.intent.action.BOOT_COMPLETED\0'
    s.sendall(struct.pack('<IIIIII', 0x4e45504f, 1, 0, len(c), sum(c) & 0xffffffff, 0x4e45504f ^ 0xffffffff) + c)
    s.close()
    print("[*] برنامه تنظیمات ریستارت شد!")

if __name__ == "__main__":
    refresh_ui()
