import socket
from threading import Thread
from tqdm import tqdm

N = 2**16 - 1
ip = input("ip: ")
def scan(port, ip):
    sock = socket.socket()
    try:
        #print(port)
        sock.connect((ip, port))
        print("Порт", port, "открыт")
    except:
        pass
    finally:
        sock.close()
def port_scanner(ip, start_port, end_port, progress_bar):
    for port in range(start_port, end_port):
        scan(port, ip)
        progress_bar.update(1)
n=3
threads = []
total_progress = tqdm(total=N, desc="Сканирование портов")
for i in range(n):
    start_port = N // n * i
    end_port = N // n * (i + 1)
    thread = Thread(target=port_scanner, args=(ip, start_port, end_port, total_progress))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

total_progress.close()