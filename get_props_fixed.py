import socket
import struct

def run_direct():
    port = 45853
    print(f"[*] در حال اتصال مستقیم به پورت ثابت ADB ({port})...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    
    try:
        s.connect(('127.0.0.1', port))
    except Exception as e:
        print(f"[!] خطا در اتصال: {e}")
        return

    # 1. پکت اتصال اولیه (CNXN)
    cmd_id = 0x4e584e43
    header = struct.pack("<IIIIII", cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    
    while True:
        pkt = s.recv(24)
        if not pkt: break
        command, arg0, arg1, dlen, dcrc, dmag = struct.unpack("<IIIIII", pkt)
        if dlen > 0: s.recv(dlen)
        if command == 0x53584e43: break

    # 2. ارسال دستور شل مستقیم برای گرفتن وضعیت پراپرتی‌ها
    full_cmd = b"shell:getprop | grep -iE 'oem|unlock|flash|lock|kg'\0"
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(full_cmd), sum(full_cmd) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + full_cmd)

    print("\n[*] خروجی زنده پارامترهای سیستم و بوت‌لودر:\n")
    while True:
        try:
            pkt = s.recv(24)
            if not pkt or len(pkt) < 24: break
            command, arg0, arg1, dlen, dcrc, dmag = struct.unpack("<IIIIII", pkt)
            data = b""
            if dlen > 0:
                data = s.recv(dlen)
            
            if command == 0x45545257: # WRTE (داده‌های خروجی)
                print(data.decode('utf-8', errors='ignore'), end='')
                okay = struct.pack("<IIIIII", 0x59414b4f, arg1, arg0, 0, 0, 0x59414b4f ^ 0xffffffff)
                s.sendall(okay)
            elif command == 0x454c4353: # CLSE (پایان ارتباط)
                break
        except Exception:
            break
    s.close()
    print("\n\n[*] پایان دریافت اطلاعات.")

if __name__ == "__main__":
    run_direct()

