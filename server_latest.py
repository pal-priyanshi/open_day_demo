import time,socket

# connection = None

def setup_socket():
    print('Setup server...')
    time.sleep(1)
    soc=socket.socket()
    host_name=socket.gethostname()
    ip=socket.gethostbyname(host_name)
    port=12345
    soc.bind((host_name,port))
    print(f"host name {host_name} ip and is {ip}")
    soc.listen(1)
    print('Waiting for connection...')
    connection,addr=soc.accept()
    print('receive connection from',addr[0],'(',addr[0],')\n')
    print(f'connection established form {addr[0]}')
    clint_name=connection.recv(1024)
    clint_name=clint_name.decode()
    print(clint_name+'has connected')

    return connection

#connection.send(name.encode())
def sending_data(input_d, connection): #input_d should be json
    if (not connection): return print("Not connected")
    headersize = 4
    msg=f'{len(input_d):<{headersize}}'+input_d
    print("SENDING MESSAGE at client",msg, type(msg))
    connection.send(bytes(msg, "utf-8")) #whatever list is there, dump to json and send json
    
# sending_data("222") 
