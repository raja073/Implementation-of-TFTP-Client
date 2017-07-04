
import struct

OP_CODE = {	"read" : 1,
			"write" : 2,
			"data" : 3,
			"ack" : 4,
			"error" : 5}

class TftpPackets:
	def __init__(self):
		self.opcode = OP_CODE

	def joinList(self, *arrs):
		joinedList = []
		for arr in arrs:
			if not isinstance(arr, list):
				arr = [arr]
			joinedList += arr
		return joinedList

	def readPacket(self, file_name, mode, op_code):
		return bytearray(self.joinList(0, op_code, map(ord, file_name), 0, map(ord, mode), 0))

	def writePacket(self,file_name, mode, op_code):
		return bytearray(self.joinList(0, op_code, map(ord, file_name), 0, map(ord, mode), 0))

	def dataPacket(self, pack_number, file_data):
		s = struct.pack('>H', pack_number)
		first, second = struct.unpack('>BB', s)
		encoding = 'latin1'
		return bytearray(self.joinList(0, self.opcode['data'],first,second, map(ord, file_data)))

	def ackPacket(self, pack_number):
		s = struct.pack('>H', pack_number)
		first, second = struct.unpack('>BB', s)
		return bytearray(self.joinList(0, self.opcode['ack'], first, second))

	def errorPacket(self, error_code,err_msg):
		return bytearray(self.joinList(0, self.opcode['error']))
