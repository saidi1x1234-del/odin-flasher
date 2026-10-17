import socket
import struct
import subprocess

def find_and_run():
    print("[*] در حال جستجوی پورت فعال ADB...")
    port = None
    
    # پیدا کردن پورت فعال از طریق دستورات سیستمی ترموکس
    try:
        out = subprocess.check_output(['ss', '-tln']).decode('utf-8', errors='ignore')
        for line in out.splitlines():
            if '127.0.0.1:' in line:
                p = int(line.split('127.0.0.1:')[1].split()[0])
                if test_adb(p):
                    port = p
                    break
    except:
        pass
        
    # اگر با ss پیدا نشد، رنج پورت‌های متداول رو اسکن می‌کنیم
    if not port:
        for p in range(35000, 48000):
            if test_adb(p):
                port = p
                break
                
    if not port:
        print("[!] هیچ پورت فعالی پیدا نشد. لطفاً شیزوکو رو یک بار ری‌استارت کن.")
        return

    print(f"[+] پورت فعال ADB پیدا شد: {port}")
    
    # اتصال به پورت پیدا شده و خواندن پراپرتی‌ها
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect(('127.0.0.1', port))
    
    cmd_id = 0x4e584e43
    header = struct.pack("<IIIIII", cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff)
    s.sendall(header + b"host::\0")
    s.recv(1024)
    
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
            if command == 0x45545257: # WRTE
                print(data.decode('utf-8', errors='ignore'), end='')
                okay = struct.pack("<IIIIII", 0x59414b4f, arg1, arg0, 0, 0, 0x59414b4f ^ 0xffffffff)
                s.sendall(okay)
            elif command == 0x454c4353: # CLSE
                break
        except Exception:
            break
    s.close()
    print("\n\n[*] پایان بررسی.")

def test_adb(p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.2)
    try:
        s.connect(('127.0.0.1', p))
        cmd_id = 0x4e584e43
        header = struct.pack("<IIIIII", cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff)
        s.sendall(header + b"host::\0")
        pkt = s.recv(24)
        s.close()
        return len(pkt) == 24
    except:
        try:
            s.close()
        except:
            pass
        return False

if __name__ == "__main__":
    find_and_run()

