import socket
from DiffieHellman import DiffieHellman
import json


class Client:
	def __init__(self):
		self.__dh = DiffieHellman.DH()

	def initDiffieHellman(self, socket):

		socket.send("connected".encode())

		# Step1: recive the shared primes and the public secret
		step1 = socket.recv(1024)
		print(step1)

		# Step 1.1: Parse them
		jsonData = json.loads(step1.decode())
		jsonData = jsonData["dh-keyexchange"]

		self.__dh.base = int(jsonData["base"])
		self.__dh.sharedPrime = int(jsonData["prime"])
		publicSecret = int(jsonData["publicSecret"])

		# Step2: calculate public secret and send to server
		calcedPubSecret = str(self.__dh.calcPublicSecret())
		step2 = "{"
		step2 += "\"dh-keyexchange\":"
		step2 += "{"
		step2 += "\"step\": {},".format(2)
		step2 += "\"publicSecret\": {}".format(calcedPubSecret)
		step2 += "}}"
		socket.send(step2.encode())

		# Step3: calculate the shared secret
		self.__dh.calcSharedSecret(publicSecret)
		print("The secret key is {}".format(self.__dh.key))

	def start_client(self, ip):
		# Start the Socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, 50000))

		# Start the Key-Exchange
		self.initDiffieHellman(sock)

		# Close the Socket
		sock.close()
