import socket
import struct

def get_all_props():
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

    # ارسال دستور getprop
    command = b'shell:getprop\0'
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)

    output = b""
    while True:
        try:
            pkt = s.recv(24)
            if not pkt or len(pkt) < 24: 
                break
            command_type, arg0, arg1, dlen, dcrc, dmag = struct.unpack("<IIIIII", pkt)
            data = b""
            if dlen > 0:
                # خواندن کامل دیتا با توجه به سایز پکت
                while len(data) < dlen:
                    chunk = s.recv(dlen - len(data))
                    if not chunk:
                        break
                    data += chunk
            
            if command_type == 0x45545257: # WRTE (داده)
                output += data
                # ارسال تأییدیه OKAY به سرور
                okay = struct.pack("<IIIIII", 0x59414b4f, arg1, arg0, 0, 0, 0x59414b4f ^ 0xffffffff)
                s.sendall(okay)
            elif command_type == 0x59414b4f: # OKAY از سمت سرور
                pass
            elif command_type == 0x454c4353: # CLSE (پایان)
                break
        except Exception as e:
            break
            
    s.close()

    lines = output.decode('utf-8', errors='ignore').splitlines()
    print(f"\n[*] کل پراپرتی‌های دریافتی: {len(lines)}")
    
    matched = [l for l in lines if any(k in l.lower() for k in ['oem', 'unlock', 'flash', 'lock', 'kg', 'secure', 'factory'])]
    
    print("\n[*] نتایج فیلتر شده مرتبط با قفل و آنلاک:")
    if matched:
        for m in matched:
            print(f"  {m}")
    else:
        print("  [!] کلیدواژه‌ای پیدا نشد. نمونه‌ای از خطوط اول:")
        for l in lines[:10]:
            print(f"  {l}")

if __name__ == "__main__":
    get_all_props()
