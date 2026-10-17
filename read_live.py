import socket
import struct

def exec_adb_shell(host, port, cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect((host, port))
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

    # 2. ارسال دستور شل به صورت مستقیم
    full_cmd = f"shell:{cmd}\0".encode('utf-8')
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(full_cmd), sum(full_cmd) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + full_cmd)

    # 3. دریافت خروجی زنده با هندل کردن پکت‌های WRTE و ارسال OKAY
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
                # ارسال تأییدیه OKAY به ADB برای ادامه دریافت داده‌ها
                okay_header = struct.pack("<IIIIII", 0x59414b4f, arg1, arg0, 0, 0, 0x59414b4f ^ 0xffffffff)
                s.sendall(okay_header)
            elif command == 0x454c4353: # CLSE (پایان استریم)
                break
        except Exception:
            break
    s.close()

if __name__ == "__main__":
    print("[*] در حال استخراج زنده پارامترهای بوت‌لودر و امنیت سامسونگ...\n")
    exec_adb_shell("127.0.0.1", 45853, "getprop | grep -iE 'oem|unlock|flash|lock|kg'")
    print("\n[*] پایان بررسی.")

