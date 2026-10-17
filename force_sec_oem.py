import socket
import struct

def force_unlock(host, port):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال: {e}")
        return

    # ارسال پکت اتصال اولیه (CNXN)
    command_id = 0x4e584e43
    header = struct.pack("<IIIIII", command_id, 0x01000000, 0x100000, 6, 0x00000018, command_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    s.recv(1024)

    # دستورات جامع برای پاک کردن وضعیت‌های قفل و اجبار به فعال‌سازی OEM و ریست پروایدر تنظیمات
    # سامسونگ معمولاً به تغییر global settings و package state حساس است
    cmds = [
        "shell:settings put global oem_unlock_allowed 1",
        "shell:setprop sys.oem_unlock_allowed 1",
        "shell:am broadcast -a android.provider.action.SETTINGS_EMBEDDED",
        "shell:pm clear com.android.settings"
    ]
    
    for cmd in cmds:
        full_cmd = (cmd + "\0").encode('utf-8')
        open_cmd = 0x4e45504f
        open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(full_cmd), sum(full_cmd) & 0xffffffff, open_cmd ^ 0xffffffff)
        s.sendall(open_header + full_cmd)
        print(f"[*] ارسال شد: {cmd}")
        
    s.close()
    print("[*] عملیات تزریق دستورات اتمام یافت.")

if __name__ == "__main__":
    force_unlock("127.0.0.1", 45853)

