import socket
import struct

def get_status(host, port):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال: {e}")
        return

    # ارسال پکت اتصال اولیه (CNXN) با الگوی ساده و موفق قبلی
    command_id = 0x4e584e43
    header = struct.pack("<IIIIII", command_id, 0x01000000, 0x100000, 6, 0x00000018, command_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    try:
        s.recv(1024)
    except:
        pass

    # ذخیره مقدار oem_unlock_allowed در یک فایل متنی در حافظه داخلی
    command = "shell:settings get global oem_unlock_allowed > /sdcard/oem_status.txt\0".encode('utf-8')
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)
    
    s.close()
    print("[*] وضعیت oem_unlock_allowed در فایل /sdcard/oem_status.txt ذخیره شد.")

if __name__ == "__main__":
    get_status("127.0.0.1", 45853)

