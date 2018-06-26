import socket 
from threading import Thread  

TCP_IP = '0.0.0.0' 
TCP_PORT = 31340 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 


class SuperSecretClass:
    def welcome(self):
        return 'Hi! Welcome to my SuperSecretClass! You can\'t get the flag though...'
#control + (255 or space)
    def __print_flag(self):
        print('MSHP{n0t_ex4ctly_pr07ec7ed_1s_17?}')

    def awesome(self):
        return 'You\'re awesome :3'

class ClientThread(Thread): 
 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print("[+] New server socket thread started for " + ip + ":" + str(port))
 
    def run(self): 
        try:
            instance = SuperSecretClass()
            conn.send((instance.welcome() + '\n').encode())
            while True:
                conn.send(b'> ')
                message = conn.recv(1024).decode(errors='ignore').strip()
                print(message)
                try:
                    result = getattr(instance, message)()
                    print(((result + '\n').encode()))
                except:
                    if 'flag' in message:
                        conn.send(b'Don\'t hack me pls =(\n')
                    else:
                        conn.send(b'No such field\n')
                else:
                    print(result.encode())
                    conn.send((result + '\n').encode())

        except:
            pass
        finally:
            conn.close()

while True: 
    tcpServer.listen(10) 
    print("Multithreaded Python server : Waiting for connections from TCP clients...")
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join() 
