#Layer 1: Both computers are connected to the sme WiFi Network
#Layer 2: Computers have NICs
#Layer 3: SSH uses IP addresses
#Layer 4: TCP is used to establish a secure connection

#to interact with operation system
import os

#paths for the named pipes
pipe1 = os.getenv("PIPE1", "/tmp/pipe1")
pipe2 = os.getenv("PIPE2", "/tmp/pipe2")

#if READ_FIRST is set to 1, then it reads first
read_first = os.getenv("READ_FIRST", "0")

#Layer 5: Named pipes for session establishment
#creating named pipes if they don't exist
try:
    os.mkfifo(pipe1, 0o600)
except:
    pass

try:
    os.mkfifo(pipe2, 0o600)
except:
    pass

#based off of if READ_ONLY is set to 1 or not
if read_first == "1":
    fifo1 = os.open(pipe1, os.O_RDONLY)
    fifo2 = os.open(pipe2, os.O_WRONLY)
else:
    fifo1 = os.open(pipe1, os.O_WRONLY)
    fifo2 = os.open(pipe2, os.O_RDONLY)


while True:
    if read_first == "1":
        #read and decode message first
        msg = os.read(fifo1, 1024)
        msg_decoded = msg.decode()
        
        #if the message received is exit then exit
        if msg_decoded.lower() == "exit":
            print("Other user exited. Exiting chat...")
            break
        
        #show message
        print(msg_decoded)
        
        #enter message
        msg = input(">")
        if msg.strip().lower() == "exit":
            print("Exiting chat...")
            os.write(fifo2, str.encode("exit"))
            break
        os.write(fifo2, str.encode(msg))
    else:
        #enter message and exit if told to
        msg = input(">")
        if msg.strip().lower() == "exit":
            print("Exiting chat...")
            os.write(fifo1, str.encode("exit"))
            break
        
        #send message to pipe
        os.write(fifo1, str.encode(msg))
        
        #receive message from pipe
        msg = os.read(fifo2, 1024)
        msg_decoded = msg.decode()
        
        #if told to exit then exit
        if msg_decoded.lower() == "exit":
            print("Other user exited. Exiting chat...")
            break
        
        #show message
        print(msg_decoded)

