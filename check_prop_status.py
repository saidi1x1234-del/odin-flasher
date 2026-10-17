import socket
import struct

def check_prop():
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

    c = b'shell:getprop | grep -i oem\0'
    s.sendall(struct.pack('<IIIIII', 0x4e45504f, 1, 0, len(c), sum(c) & 0xffffffff, 0x4e45504f ^ 0xffffffff) + c)
    
    print("[*] وضعیت پراپرتی‌های OEM:")
    while True:
        try:
            pkt = s.recv(24)
            if not pkt or len(pkt) < 24: break
            command, arg0, arg1, dlen, dcrc, dmag = struct.unpack("<IIIIII", pkt)
            if dlen > 0:
                data = s.recv(dlen)
                if command == 0x45545257:
                    print(data.decode('utf-8', errors='ignore'), end='')
                    s.sendall(struct.pack("<IIIIII", 0x59414b4f, arg1, arg0, 0, 0, 0x59414b4f ^ 0xffffffff))
            elif command == 0x454c4353:
                break
        except:
            break
    s.close()

if __name__ == "__main__":
    check_prop()
