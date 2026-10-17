import socket
import struct

def check_props():
    port = 44411
    print(f"[*] اتصال به پورت {port}...")
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

    # ارسال دستور برای گرفتن پراپرتی‌های مربوط به oem و unlock
    command = b'shell:getprop | grep -iE "oem|unlock"\0'
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)

    print("\n[*] نتیجه بررسی پراپرتی‌ها:\n")
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
    print("\n\n[*] پایان بررسی.")

if __name__ == "__main__":
    check_props()
