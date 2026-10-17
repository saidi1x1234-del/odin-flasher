import socket
import struct

def unlock_on_port():
    port = 44411
    print(f"[*] اتصال به پورت جدید شیزوکو ({port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect(('127.0.0.1', port))
    except Exception as e:
        print(f"[!] خطا در اتصال: {e}")
        return

    # هندشک اتصال اولیه ADB
    cmd_id = 0x4e584e43
    header = struct.pack("<IIIIII", cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    try:
        s.recv(1024)
    except:
        pass

    # دستورات تزریق آنلاک و تغییر پراپرتی‌های سیستمی
    cmds = [
        "shell:settings put global oem_unlock_allowed 1",
        "shell:setprop sys.oem_unlock_allowed 1",
        "shell:setprop ro.oem_unlock_supported 1",
        "shell:am broadcast -a android.intent.action.BOOT_COMPLETED"
    ]

    for cmd in cmds:
        full_cmd = (cmd + "\0").encode('utf-8')
        open_cmd = 0x4e45504f
        open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(full_cmd), sum(full_cmd) & 0xffffffff, open_cmd ^ 0xffffffff)
        s.sendall(open_header + full_cmd)
        print(f"[*] دستور اجرا شد: {cmd}")
        
    s.close()
    print("[*] ضربه نهایی روی پورت جدید نشست!")

if __name__ == "__main__":
    unlock_on_port()
