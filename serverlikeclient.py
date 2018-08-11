import socket

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",9001))
s.listen(1)


while True:
	con,addr=s.accept()
	print("Connected",addr[0],addr[1])
	data=con.recv(1024)
	print("Client send:",data)
	con.send(data[::-1])
	con.close()
