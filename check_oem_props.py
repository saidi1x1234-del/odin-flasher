import socket
import struct

def dump_oem_props(host, port):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    
    try:
        s.connect((host, port))
    except Exception as e:
        print(f"[!] خطا در اتصال: {e}")
        return

    # ارسال پکت اتصال (CNXN)
    cmd_id = 0x4e584e43  # 'CNXN'
    header = struct.pack("<IIIIII", cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    s.recv(1024)

    # دستور برای جستجوی پراپرتی‌های مربوط به آنلاک و اوئی‌ام
    command = "shell:getprop | grep -iE 'oem|unlock|flash|warranty'\0".encode('utf-8')
    open_cmd = 0x4e45504f    # 'OPEN'
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)

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
    print("\n[*] بررسی پراپرتی‌ها به پایان رسید.")

if __name__ == "__main__":
    dump_oem_props("127.0.0.1", 45853)

