import socket
import threading

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(5)
print('Server is listing')
def listen(conn, addr):
	while True:
		data = conn.recv(1024)
		msg = data.decode()
		if not data:
			break
		conn.send(data)
		print(msg)
	conn.close()

msg = ''
while True:
	conn, addr = sock.accept()
	print(addr)
	threading.Thread(target=listen, args=(conn, addr)).start()
