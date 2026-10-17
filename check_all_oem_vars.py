import socket
import struct

def dump_all_vars(host, port):
    print(f"[*] در حال اتصال به پورت ADB ({host}:{port})...")
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
    try:
        s.recv(1024)
    except:
        pass

    # دستورات جامع برای جمع‌آوری تمام متغیرهای مرتبط با آنلاک و بوت‌لودر در یک فایل تدافعی
    shell_cmd = (
        "shell:echo '--- GLOBAL ---' > /data/local/tmp/oem_debug.txt && "
        "settings get global oem_unlock_allowed >> /data/local/tmp/oem_debug.txt 2>&1 && "
        "echo '--- SECURE ---' >> /data/local/tmp/oem_debug.txt && "
        "settings get secure oem_unlock_allowed >> /data/local/tmp/oem_debug.txt 2>&1 && "
        "echo '--- SYS PROPS ---' >> /data/local/tmp/oem_debug.txt && "
        "getprop | grep -iE 'oem|unlock|flash|lock' >> /data/local/tmp/oem_debug.txt 2>&1\0"
    ).encode('utf-8')

    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(shell_cmd), sum(shell_cmd) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + shell_cmd)
    
    s.close()
    print("[*] تمام متغیرها با موفقیت در /data/local/tmp/oem_debug.txt ذخیره شدند.")

if __name__ == "__main__":
    dump_all_vars("127.0.0.1", 45853)

