import os

# Use environment variables for pipe paths
pipe1 = os.getenv("PIPE1", "/tmp/pipe1")
pipe2 = os.getenv("PIPE2", "/tmp/pipe2")

read_first = os.getenv("READ_FIRST", "0")

# Create named pipes if they do not exist
try:
    os.mkfifo(pipe1, 0o600)
except FileExistsError:
    print("Named pipe for pipe1 already exists!")

try:
    os.mkfifo(pipe2, 0o600)
except FileExistsError:
    print("Named pipe for pipe2 already exists!")

if read_first == "1":
    fifo1 = os.open(pipe1, os.O_RDONLY)
    fifo2 = os.open(pipe2, os.O_WRONLY)
else:
    fifo1 = os.open(pipe1, os.O_WRONLY)
    fifo2 = os.open(pipe2, os.O_RDONLY)

while True:
    if read_first == "1":
        # Read message from pipe first
        msg = os.read(fifo1, 1024)
        msg_decoded = msg.decode().strip()
        
        # Check if the exit message is received
        if msg_decoded.lower() == "exit":
            print("Other user exited. Exiting chat...")
            break
        
        # Output the message to screen
        print(msg_decoded)
        
        # Get message from input
        msg = input(">")
        if msg.strip().lower() == "exit":
            print("Exiting chat...")
            os.write(fifo2, str.encode("exit"))
            break
        os.write(fifo2, str.encode(msg))
    else:
        # Read message from input first
        msg = input(">")
        if msg.strip().lower() == "exit":
            print("Exiting chat...")
            os.write(fifo1, str.encode("exit"))
            break
        
        # Send message to pipe
        os.write(fifo1, str.encode(msg))
        
        # Receive message from pipe
        msg = os.read(fifo2, 1024)
        msg_decoded = msg.decode().strip()
        
        # Check if the exit message is received
        if msg_decoded.lower() == "exit":
            print("Other user exited. Exiting chat...")
            break
        
        # Output the message to screen
        print(msg_decoded)

# Clean up by closing the pipes
os.close(fifo1)
os.close(fifo2)

