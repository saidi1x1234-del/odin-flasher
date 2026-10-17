import socket
import struct

def save_system_props(host, port):
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

    # ارسال دستور برای ذخیره خروجی در یک فایل متنی
    command = "shell:getprop > /sdcard/props.txt\0".encode('utf-8')
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)
    
    s.close()
    print("[*] دستور اجرا شد. فایل props.txt در حافظه داخلی ذخیره گردید.")

if __name__ == "__main__":
    save_system_props("127.0.0.1", 45853)

