#imports socket
import socket

#lets host be any ip, also can put 0.0.0.0
thehost = ""
#random port number is okay i think
theport = 24949

#af_inet allows socket to use the normal ip addresses (IPv$)
#sock_stream is socket type for TCP which is safer than the other one
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	#binds the socket to the host and port
	s.bind((thehost, theport))

	#only allows one client on
	s.listen(1)
	
	#lets the server accept the client wanting to connect
	conn, addr = s.accept()
	with conn:
		print(f"Connected by {addr}")
		
		#when this can all happen
		while True:

			#1024 is max number of bytes
			data = conn.recv(1024)

			#happens when the client disconnects
			if not data:
				print("\nClient disconnected!")
				break

			#outputs message from client
			print(f"Message from the client: {data.decode()}")

			#inputs for the server to message, exits and disconnects when prompted to
			response_mess = input("Enter message to client (type exit to exit): ")
			if response_mess.lower() == "exit":
				print("\n...Server is exiting...")
				break
			conn.sendall(response_mess.encode())
