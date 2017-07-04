import Tkinter as tk 
import tkFileDialog

from ops_tftp_temp import *

class TftpClient(tk.Frame):
	def __init__(self, master):

		opsTftp = OpsTftp(self)
		self.reading_fun = opsTftp.reading
		self.writing_fun = opsTftp.writing

		tk.Frame.__init__(self, master)
		self.pack()
		self.master.title("TFTP Client App")

		##Frame for Titles (TFTP Client, THM)
		title_frame = tk.Frame(self, highlightbackground="green", highlightcolor="green", highlightthickness=1, width=600, height = 30, bd= 0)
		title_frame.pack(padx = 10, pady = 5, anchor = 'w')
		tk.Label(title_frame, text = "TFTP Client ----------------------------------").pack(side = 'left')
		tk.Label(title_frame, text = "-------------------THM").pack(side = 'right')

		##Frame for user inputs
		input_frame = tk.Frame(self, highlightbackground="red", highlightcolor="red", highlightthickness=1, width=600, height = 60, bd= 0)
		input_frame.pack(padx = 10, anchor = 'w')

			## Host IP Address Label and Entry
		tk.Label(input_frame, text = 'HOST Ip Address:').grid(row = 0, column = 0, sticky = 'w')
		self.host_ip = tk.Entry(input_frame, background = 'white', width = 30)
		self.host_ip.grid(row = 0, column = 1, sticky = 'w', padx = 5, pady = 5)
		self.host_ip.focus_set()

			## Port number Label and Entry
		tk.Label(input_frame, text = 'Port Number:').grid(row = 1, column = 0, sticky = 'w')
		self.port_number = tk.Entry(input_frame, background = 'white', width = 8)
		self.port_number.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 5)

		##Frame for local/ remote file selection
		file_frame = tk.Frame(self, highlightbackground="blue", highlightcolor="blue", highlightthickness=1, width=600, height = 60, bd= 0)
		file_frame.pack(padx = 10, pady = 5, anchor = 'w')

			## File to send Field and Entry
		tk.Label(file_frame, text = 'Select file to send:').grid(row = 0, column = 0, sticky = 'w')
		self.file_to_send = tk.Entry(file_frame, background = 'white', width = 30)
		self.file_to_send.grid(row = 0, column = 1, sticky = 'w', padx = 5, pady = 5)

			##Browse button
		self.browse_button = tk.Button(file_frame, text = 'BROWSE', command = self.file_browser)
		self.browse_button.grid(row = 0, column = 2, sticky = 'w', padx = 5, pady = 5)

			## File to receive Filed and Entry
		tk.Label(file_frame, text = 'Enter file to receive:').grid(row = 1, column = 0, sticky = 'w')
		self.file_to_receive = tk.Entry(file_frame, background = 'white', width = 30)
		self.file_to_receive.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 5)

			##Clear button
		self.clear_button = tk.Button(file_frame, text = 'CLEAR', command = self.clear_fields)
		self.clear_button.grid(row = 1, column = 2, sticky = 'w', padx = 5, pady = 5)

			## Local file name (rename) Filed and Entry
		tk.Label(file_frame, text = 'Enter local file name:').grid(row = 2, column = 0, sticky = 'w')
		self.local_file = tk.Entry(file_frame, background = 'white', width = 30)
		self.local_file.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

			##Default timeout Label and Entry in Seconds
		tk.Label(file_frame, text = 'Default Timeout:').grid(row = 3, column = 0, sticky = 'w')
		self.time_out = tk.Entry(file_frame, background = 'white', width = 10)
		self.time_out.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)
		tk.Label(file_frame, text = 'Seconds').grid(row = 3, column = 1, sticky = 'e')


		##Frame for buttons (GET/ PUT/ CANCEL)
		button_frame = tk.Frame(self, highlightbackground="orange", highlightcolor="orange", highlightthickness=1, width=600, height = 60, bd= 0)
		button_frame.pack(padx = 10, anchor = 'center')

			##GET button
		self.get_button = tk.Button(button_frame, text = 'GET', command = self.click_get)
		self.get_button.grid(row = 0, column = 0, sticky = 'w', padx = 5, pady = 5)

			##PUT button
		self.put_button = tk.Button(button_frame, text = 'PUT', command = self.click_put)
		self.put_button.grid(row = 0, column = 1, sticky = 'w', padx = 5, pady = 5)

			##QUIT button
		self.quit_button = tk.Button(button_frame, text = 'QUIT', command = self.click_quit)
		self.quit_button.grid(row = 0, column = 2, sticky = 'w', padx = 5, pady = 5)


		##Frame for file transfer statistics disply
		statistics_frame = tk.Frame(self, highlightbackground="violet", highlightcolor="violet", highlightthickness=1, width=600, height = 60, bd= 0)
		statistics_frame.pack(padx = 10, pady = 5, anchor = 'w')

			## Title for Statistics frame
		tk.Label(statistics_frame, text = '--Statistics--').grid(row = 0, column = 0, sticky = 'w')

			## Number of packets needed: Label and Entry
		tk.Label(statistics_frame, text = 'Packets needed to transfer the file:').grid(row = 1, column = 0, sticky = 'w')
		self.packet_number = tk.Entry(statistics_frame, background = 'white', width = 27)
		self.packet_number.grid(row = 1, column = 1, sticky = 'w', padx = 5, pady = 5)

			## Number of errors: Label and Entry
		tk.Label(statistics_frame, text = 'Number of errors:').grid(row = 2, column = 0, sticky = 'w')
		self.error_number = tk.Entry(statistics_frame, background = 'white', width = 27)
		self.error_number.grid(row = 2, column = 1, sticky = 'w', padx = 5, pady = 5)

			## Last error code: Label and Entry
		tk.Label(statistics_frame, text = 'Last error code:').grid(row = 3, column = 0, sticky = 'w')
		self.error_code = tk.Entry(statistics_frame, background = 'white', width = 27)
		self.error_code.grid(row = 3, column = 1, sticky = 'w', padx = 5, pady = 5)

	def file_browser(self):
		self.selected_file = tkFileDialog.askopenfilename(parent = self)
		self.file_to_send.delete(0, 'end')
		self.file_to_send.insert(0, self.selected_file)
		print "File selected to put: ", self.selected_file

	def clear_fields(self):
		self.file_to_send.delete(0, 'end')
		self.file_to_receive.delete(0, 'end')
		self.local_file.delete(0, 'end')
		self.time_out.delete(0, 'end')

	def click_quit(self):
		print("The user clicked Quit!!")
		self.master.destroy()

	def click_get(self):
		self.val_host_ip = self.host_ip.get()
		self.val_port_number = int(self.port_number.get())
		self.val_file_to_receive = self.file_to_receive.get()
		self.val_local_file = self.local_file.get()
		print("The user clicked GET: \nHost Ip: {}\nPort no: {}\nFile to receive: {}\nLocal File: {}".format(self.val_host_ip, self.val_port_number, self.val_file_to_receive, self.val_local_file))
		self.reading_fun(self.val_host_ip, self.val_port_number, self.val_file_to_receive, self.val_local_file)

	def click_put(self):
		self.val_host_ip = self.host_ip.get()
		self.val_port_number = int(self.port_number.get())
		self.val_file_to_send = self.file_to_send.get()
		print("The user clicked PUT: \nHost Ip: {}\nPort no: {}\nFile to send: {}".format(self.val_host_ip, self.val_port_number, self.val_file_to_send))
		self.writing_fun(self.val_host_ip, self.val_port_number, self.val_file_to_send)

	def update_error_messsage(self, val_error_code):
		self.error_code.delete(0, 'end')
		self.error_code.insert(0, val_error_code)

	def update_error_counter(self, val_error_number):
		self.error_number.delete(0, 'end')
		self.error_number.insert(0, val_error_number)

	def update_packet_counter(self, val_packet_number):
		self.packet_number.delete(0, 'end')
		self.packet_number.insert(0, val_packet_number)

	def clear_statistics_fields(self):
		self.error_code.delete(0, 'end')
		self.error_number.delete(0, 'end')
		self.packet_number.delete(0, 'end')

if __name__ == '__main__':
	root = tk.Tk()
	tftp_client = TftpClient(root)
	tftp_client.mainloop()