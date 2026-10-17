import socket
import struct

def check_status():
    port = 44411
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    try:
        s.connect(('127.0.0.1', port))
    except Exception as e:
        print(f"[!] خطا: {e}")
        return

    cmd_id = 0x4e584e43
    s.sendall(struct.pack('<IIIIII', cmd_id, 0x01000000, 0x100000, 6, 0x00000018, cmd_id ^ 0xffffffff) + b'host::\0')
    try:
        s.recv(1024)
    except:
        pass

    c = b'shell:settings get global oem_unlock_allowed\0'
    s.sendall(struct.pack('<IIIIII', 0x4e45504f, 1, 0, len(c), sum(c) & 0xffffffff, 0x4e45504f ^ 0xffffffff) + c)
    
    print("[*] پاسخ سیستم:")
    try:
        print(s.recv(4096).decode('utf-8', errors='ignore'))
    except:
        print("چیزی دریافت نشد.")
    s.close()

if __name__ == "__main__":
    check_status()
