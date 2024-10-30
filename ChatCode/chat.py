import os

pipe1 = "/Users/jianzhuowang/pipes/pipe1"
pipe2 = "/Users/jianzhuowang/pipes/pipe2"

read_first = os.getenv("READ_FIRST", 0)

try:
      os.mkfifo(pipe1, 0o600)
except FileExistsError:
      print("Named pipe already exists!")

try:
      os.mkfifo(pipe2, 0o600)
except FileExistsError:
      print("Named pipe already exists!")

if read_first == "1":
   try:
      fifo1 = os.open(pipe1, os.O_RDONLY)
   except FileExistsError:
      print("Named pipe already exists!")

   try:
      fifo2 = os.open(pipe2, os.O_WRONLY)
   except FileExistsError:
      print("Named pipe already exists!")
else:
   try:
      fifo1 = os.open(pipe1, os.O_WRONLY)
   except FileExistsError:
      print("Named pipe already exists!")

   try:
      fifo2 = os.open(pipe2, os.O_RDONLY)
   except FileExistsError:
      print("Named pipe already exists!")

while True:
   if read_first == "1":
      # read message from pipe first
      msg = os.read(fifo1, 1024)
      # output the message to screen
      print(msg.decode())
      # get message from input
      msg = input(">")
      os.write(fifo2, str.encode(msg))
   else:
      # read message from input first
      msg = input(">")
      # send message to pipe
      os.write(fifo1, str.encode(msg))
      # receive message from pipe
      msg = os.read(fifo2, 1024)
      # output the message to screen
      print(msg.decode())

