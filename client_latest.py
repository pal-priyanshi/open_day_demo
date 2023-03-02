import time,socket
headersize=4
print('Clint server...')
time.sleep(1)
soc=socket.socket()
shost=socket.gethostname()
ip=socket.gethostbyname(shost)
print(f"{shost},{ip}")
server_host=input('Enter Server\'s IP address:')
name= input('Enter Client\'s name:')
port =12345
print(f'Trying to connect to the server:{server_host},{port}')
time.sleep(1)
soc.connect((server_host,port))
print('Connected...\n')
soc.send(name.encode())
#server_name=soc.recv(1024)
#server_name=server_name.decode()
#print('{} has joined...'.format(server_name))
#print('Enter [bye] to exit.')
#while True:
while True:
    message=soc.recv(1024)
    msglen=int(message[:headersize])
    message=message.decode("utf-8")
    if len(message)-headersize==msglen:
        print("full msg received",message)
        message=message.split()
        print("POST SPLITTING MESSAGE ", message, message[0], message[1])
        #message=message[:-1]
    else:
        print("SOMETHING IS WRONG!!!!!!!!!!!! MSG NOT RECVD")
    if (not message == ""):
        print('>',message)
    #message=input(str('Me > '))
    # if message == '[bye]':
    #     message='Leaving the Chat room'
    #     soc.send(message.encode())
    #     print('\n')

        #break
    #soc.send(message.encode())
