from socket import *

def getIPAddress():
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def getMessage(sock):
    data = sock.recv(1024)
    return data.decode('ascii')

def sendMessage(sock, msg):
    try:
        sock.send(msg.encode('ascii'))
    except:
        print("Message failed to send")

def protocolError(sock, msg="Error in protocol. Terminating connection..."):
    sendMessage(sock, msg)
    sock.close()
    print("Closed connection")
    
### Add MockDNS Lookup here.
def mockDNS(location, who = "ok"):
    server = socket(AF_INET, SOCK_STREAM)
    server.connect((location, 2001))

    outgoing = gethostname()+","+getIPAddress()
    sendMessage(server,outgoing)
    print(f"Sent: {outgoing}")

    incoming = getMessage(server)
    print(incoming)

    outgoing = "ok" if who == "ok" else "who " + who
    sendMessage(server,outgoing)
    print(f"Sent: {outgoing}")

    incoming = getMessage(server)
    print(incoming)
    return incoming
