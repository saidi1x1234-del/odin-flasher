import socket
import struct

def check_setting(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال: {e}")
        return

    # پکت اتصال اولیه (CNXN)
    command_id = 0x4e584e43
    header = struct.pack("<IIIIII", command_id, 0x01000000, 0x100000, 6, 0x00000018, command_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    s.recv(1024)

    # دستور برای خواندن مقدار سوییچ OEM در دیتابیس global
    command = "shell:settings get global oem_unlock_allowed\0".encode('utf-8')
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)

    print("[*] مقدار ثبت‌شده در سیستم:")
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            print(chunk.decode('utf-8', errors='ignore'), end='')
        except socket.timeout:
            break
        except Exception:
            break
            
    s.close()

if __name__ == "__main__":
    check_setting("127.0.0.1", 45853)

