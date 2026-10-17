import socket
import struct
import sys

def get_system_props(host, port):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال به پورت: {e}")
        return

    # 1. ارسال پکت اتصال اولیه (CNXN) مشابه اسکریپت موفق قبلی
    command_id = 0x4e584e43  # 'CNXN'
    arg0 = 0x01000000
    arg1 = 0x100000
    banner = b"host::\0"
    data_len = len(banner)
    magic = command_id ^ 0xffffffff
    
    header = struct.pack("<IIIIII", command_id, arg0, arg1, data_len, sum(banner) & 0xffffffff, magic)
    s.sendall(header + banner)
    
    try:
        response = s.recv(1024)
        print(f"[*] اتصال برقرار شد. در حال خواندن پراپرتی‌های سیستم...")
    except Exception as e:
        print(f"[!] خطا در دریافت پاسخ: {e}")
        s.close()
        return

    # 2. ارسال دستور shell برای استخراج پراپرتی‌ها
    command = "shell:getprop | grep -iE 'oem|unlock|flash|warranty|kg|lock'\0".encode('utf-8')
    open_cmd = 0x4e45504f    # 'OPEN'
    local_id = 1
    remote_id = 0
    d_len = len(command)
    d_magic = open_cmd ^ 0xffffffff
    
    open_header = struct.pack("<IIIIII", open_cmd, local_id, remote_id, d_len, sum(command) & 0xffffffff, d_magic)
    s.sendall(open_header + command)
    
    # 3. دریافت و نمایش خروجی
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
    print("\n[*] استخراج اطلاعات به پایان رسید.")

if __name__ == "__main__":
    get_system_props("127.0.0.1", 45853)

