import socket
import struct

def send_adb_shell_command(host, port, command):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال به پورت: {e}")
        return

    # ارسال پکت اتصال (CNXN)
    cmd_id = 0x4e584e43  # 'CNXN'
    header = struct.pack("<IIIIII", cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    s.recv(1024)

    # ارسال دستور شل برای فعال‌سازی و اجبار به نمایش OEM Unlocking
    full_cmd = f"shell:{command}\0".encode('utf-8')
    open_cmd = 0x4e45504f    # 'OPEN'
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(full_cmd), sum(full_cmd) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + full_cmd)

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
    # دستورات چندگانه برای باز کردن سوییچ‌های مخفی توسعه‌دهنده و تنظیمات ریجن/OEM
    target_command = "settings put global oem_unlock_allowed 1; setprop sys.oem_unlock_allowed 1"
    print(f"[*] دستور هدف: {target_command}")
    send_adb_shell_command("127.0.0.1", 45853, target_command)

