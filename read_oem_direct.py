import socket
import struct

def read_oem_direct(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
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

    # ارسال دستور برای دریافت مستقیم مقدار oem_unlock_allowed
    command = "shell:settings get global oem_unlock_allowed\0".encode('utf-8')
    open_cmd = 0x4e45504f
    open_header = struct.pack("<IIIIII", open_cmd, 1, 0, len(command), sum(command) & 0xffffffff, open_cmd ^ 0xffffffff)
    s.sendall(open_header + command)

    print("[*] نتیجه دستور:")
    output = b""
    while True:
        try:
            chunk = s.recv(4096)
            if not chunk:
                break
            output += chunk
        except socket.timeout:
            break
        except Exception:
            break
        
    s.close()
    
    # چاپ خروجی تمیز شده
    clean_output = output.decode('utf-8', errors='ignore').strip()
    print(f"مقدار فعلی: {clean_output}")

if __name__ == "__main__":
    read_oem_direct("127.0.0.1", 45853)

