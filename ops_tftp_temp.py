
from socket import *
from packets import *
from tftpGUI2_temp import *
import sys, time
import struct

class OpsTftp:

	LENGTH_DATA = 512
	LENGTH_TOTAL = 516
	#runtime = 4294967295

	def __init__(self, app):

		self.app = app
		self.socket = socket(AF_INET, SOCK_DGRAM)
		self.op_code = OP_CODE
		self.mode = 'octet'
		self.pack_counter = 0
		self.error_counter = 0
		self.error_message = ''

		# Objects from TftpPackets Class
		tftp_packets = TftpPackets()
		self.readPacket = tftp_packets.readPacket
		self.writePacket = tftp_packets.writePacket
		self.ackPacket = tftp_packets.ackPacket
		self.dataPacket = tftp_packets.dataPacket

	def reading(self, host_id, port_num, remote_file, local_name):

		self.clear_statistics_field()
		op_code = self.op_code['read']
		read_pack_number = 1

		self.host_addr = (host_id, port_num)
		self.socket = socket(AF_INET, SOCK_DGRAM)

		sending_pack = self.readPacket(remote_file, self.mode, op_code)
		print "sending full: ", repr(sending_pack)
		print "sending packet[0]: ", repr(sending_pack[0])
		print "lendth of sending packet:", sys.getsizeof(sending_pack)

		self.socket.sendto(sending_pack, self.host_addr)
		(receiving_pack, (server_host, server_port)) = self.socket.recvfrom(self.LENGTH_TOTAL)

		print "receiving_pack: ", repr(receiving_pack)
		print "local_host: ", server_host
		print "local_port: ", server_port
		print "receiving_pack[0]: ", repr(receiving_pack[0])
		print "receiving_pack[1]: ", repr(receiving_pack[1])
		print "receiving_pack[2]: ", repr(receiving_pack[2])
		print "receiving_pack[3]: ", repr(receiving_pack[3])
		print "receiving_pack[4:]: ", repr(receiving_pack[4:])
		received_pack_length = len(receiving_pack)
		print "length of received pack", len(receiving_pack)

		##read_start_time = time.time()
		with open(local_name, 'wb+') as f:
			while True:

				if (map(ord, receiving_pack)[1]) == 3:
					f.write(receiving_pack[4:])
					print repr(receiving_pack[4:])
					print "END OF LINE"

					if self.LENGTH_TOTAL > len(receiving_pack):
						acking_pack = self.ackPacket(read_pack_number)
						self.socket.sendto(acking_pack, (server_host, server_port))
						print "Last Packet Received!!!"
						self.error_counter = 0
						self.pack_counter = self.pack_counter + 1
						self.update_packet_count(self.pack_counter)
						print "Total number of read packets: ", self.pack_counter
						break

					else:
						acking_pack = self.ackPacket(read_pack_number)
						read_pack_number += 1
						self.pack_counter = read_pack_number
						print "Packet count: ", self.pack_counter
						self.socket.sendto(acking_pack, (server_host, server_port))
						(receiving_pack, (server_host, server_port)) = self.socket.recvfrom(self.LENGTH_TOTAL)

				elif (map(ord, receiving_pack)[1]) == 5:
					print "Error message: ",repr(receiving_pack[4:])
					self.error_message = repr(receiving_pack[4:])
					self.update_error(self.error_message)
					self.error_counter += 1
					self.update_error_count(self.error_counter)
					print "Error count: ", self.error_counter

					if (self.error_counter > 150):
						print "Maximum Errors reached!!!"
						return
					else:	
						self.socket.sendto(sending_pack, self.host_addr)
						(receiving_pack, (server_host, server_port)) = self.socket.recvfrom(self.LENGTH_TOTAL)
				else:
					print("Unknown response from Server!!/ Error!!")


	def writing(self, host_id, port_num, local_file):

		self.clear_statistics_field()
		self.socket = socket(AF_INET, SOCK_DGRAM)
		op_code = self.op_code['write']
		write_pack_number = 0
		block_number = 0

		file = open(local_file, 'rb+')
		read_file = file.read()
		sending_pack = self.writePacket(local_file, self.mode, op_code)
		self.host_addr = (host_id, port_num)
		self.socket.sendto(sending_pack, self.host_addr)
		(receiving_pack, (server_host, server_port)) = self.socket.recvfrom(self.LENGTH_TOTAL)

		write_start_time = time.time()

		while True:
			try:
				
				if receiving_pack[1] ==  '\x04':
					file_data = read_file[block_number : (self.LENGTH_DATA + block_number)]
					write_pack_number += 1

					self.pack_counter = write_pack_number
					print "Write Packet count: ", self.pack_counter

					#create data packet
					data_packet = self.dataPacket(write_pack_number, file_data)

					# sending data packet on new port number
					self.socket.sendto(data_packet, (server_host, server_port))

					(receiving_pack,(server_host,server_port)) = self.socket.recvfrom(self.LENGTH_TOTAL)

					block_number += self.LENGTH_DATA

				if (map(ord, receiving_pack)[1]) == 5:
					print "Error message: ",repr(receiving_pack[4:])
					self.error_message = repr(receiving_pack[4:])
					self.update_error(self.error_message)
					self.error_counter += 1
					self.update_error_count(self.error_counter)
					print "Error count: ", self.error_counter

					if (self.error_counter > 250):
						print "Maximum Errors reached!!!"
						return
					else:
						data_packet = self.dataPacket(write_pack_number, file_data)	
						self.socket.sendto(data_packet, server_host,server_port)
						(receiving_pack, (server_host, server_port)) = self.socket.recvfrom(self.LENGTH_TOTAL)


				if self.LENGTH_TOTAL > len(data_packet):
					print "Last data packet sent!!"
					self.pack_counter = self.pack_counter + 1
					self.update_packet_count(self.pack_counter)
					print "Total number of write packets: ", self.pack_counter
					break


			except Exception as exc:
				file.close()
				print "Write exception: %s" % exc
				self.writing(host_id, port_num, local_file)
	
	def update_error(self, error_message):
		self.app.update_error_messsage(error_message)

	def update_error_count(self, error_counter):
		self.app.update_error_counter(error_counter)

	def update_packet_count(self, pack_counter):
		self.app.update_packet_counter(pack_counter)

	def clear_statistics_field(self):
		self.app.clear_statistics_fields()