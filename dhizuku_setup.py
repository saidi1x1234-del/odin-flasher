import socket
import struct
import sys

def send_adb_command(host, port, command):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال به پورت: {e}")
        return

    # 1. ارسال پکت اتصال اولیه (CNXN)
    command_id = 0x4e584e43  # 'CNXN'
    arg0 = 0x01000000
    arg1 = 0x100000
    banner = b"host::\0"
    data_len = len(banner)
    magic = command_id ^ 0xffffffff
    
    header = struct.pack("<IIIIII", command_id, arg0, arg1, data_len, sum(banner) & 0xffffffff, magic)
    s.sendall(header + banner)
    
    response = s.recv(1024)
    print(f"[*] پاسخ اولیه سرور دریافت شد. در حال ارسال دستور...")

    # 2. ارسال پکت اجرای دستور شل (OPEN)
    open_cmd = 0x4e45504f    # 'OPEN'
    local_id = 1
    remote_id = 0
    destination = f"shell:{command}\0".encode('utf-8')
    d_len = len(destination)
    d_magic = open_cmd ^ 0xffffffff
    
    open_header = struct.pack("<IIIIII", open_cmd, local_id, remote_id, d_len, sum(destination) & 0xffffffff, d_magic)
    s.sendall(open_header + destination)
    
    # دریافت خروجی اجرای دستور
    output = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            output += chunk
            print(chunk.decode('utf-8', errors='ignore'), end='')
        except socket.timeout:
            break
        except Exception:
            break
            
    s.close()
    print("\n[*] اجرای دستور به پایان رسید.")

if __name__ == "__main__":
    # دستور فعال‌سازی دیزوکو به عنوان Device Owner
    target_command = "dpm set-device-owner com.rosan.dhizuku/.server.DhizukuDAReceiver"
    print(f"[*] دستور هدف: {target_command}")
    send_adb_command("127.0.0.1", 45853, target_command)

