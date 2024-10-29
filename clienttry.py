#imports socket
import socket

#lets the client choose the IP of the server
thehost = input("\nEnter the IP of the server: ")
#random port like b4
theport = 24949

#same with the server, allows for IPv4 and TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	
	#client connects to the server
	s.connect((thehost, theport))
	while True:

		#the input from the client, exits and disconnects when prompted
		respondmess = input("Enter message to server (type exit to exit): ")
		if respondmess.lower() == "exit":
			print("...Client is exiting...")
			break

		#sends the message
		s.sendall(respondmess.encode())

		#max bytes of data, when client exits it shows
		data = s.recv(1024)
		if not data:
			print("\nServer disconnected!")
			break

		#output from server
		print(f"Received from server: {data.decode()}")
