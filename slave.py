import sys
import socket
import time
import subprocess
from mylib import cooldecode
slaveSocket = 0
port = 9999
host = 0


def connecttomaster():
    global slaveSocket
    global host
    global port
    slaveSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = socket.gethostname()
    print(slaveSocket)
    print("trying to connect",end = ' ')
    while True:
        try:
            time.sleep(0.3)
            print('.',end = '')
            slaveSocket.connect((host,port))
            break
        except :
            continue

    print("Connected to master")
    print(slaveSocket)
    return

def sendfeedback(arg):
    if(arg == 'help'):
        return 'Sends feedback to master. Argument will be the feedback.'
    
    feedback = arg
    byte = feedback.encode("utf")
    slaveSocket.send(byte)
    return

def connectioncheck(arg):
    if(arg == 'help'):
        return 'Sends feedback if slave is connected.'
    sendfeedback("connected")

    return

def cmd(arg):
    if(arg == 'help'):
        return 'Executes the cmd command with the arguments then sends output.'
    
    print("Trying to execute command "+arg)
    output = subprocess.check_output(arg,shell = True)
    output = cooldecode(output)
    sendfeedback(output)
    return

def myprint(arg):
    if(arg == 'help'):
        return 'prints the argument on slave\'s display'
    
    print(arg)
    sendfeedback("Slave has written "+arg)
    return 
    
def exit(arg):
    if(arg == 'help'):
        return 'shuts the slave'
        
    sendfeedback("Slave has been shutdown")
    sys.exit()
    return

def help(arg):
    result = 'List of available commands of slave:\n\n'
    temp = ''
    g = globals()
    for f in g:
        temp = str(globals()[f])
        if(temp.startswith('<function')):
            temp = temp.split(" ")[1]
            if(temp != 'execute' and temp != 'cycle' and temp != 'main' and temp != 'help' and temp != 'cooldecode' and temp != 'connecttomaster'):
                result += temp + ': '
                result += g[f]('help')
                result +='\n\n'
            
    sendfeedback(result)
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
        sendfeedback("Slave Bad argument")
    except KeyError:
        sendfeedback("Slave No function found (KeyError)")
    except TypeError:
        sendfeedback("Slave No function found (TypeError)")
    except:
        sendfeedback("Something went wrong in slave")
    return

def cycle():
    byte = 0
    while True:
        try:
            byte = slaveSocket.recv(4096)
            command = cooldecode(byte)
            execute(command)
        except ConnectionResetError:
            print("Master disconnected")
            connecttomaster()
        except ConnectionAbortedError:
            print("Master kicked")
            connecttomaster()
        except:
            print('Something went wrong')
            connecttomaster()
            continue
        
    
    return

def main():
    connecttomaster()
    cycle()
    return

main()
