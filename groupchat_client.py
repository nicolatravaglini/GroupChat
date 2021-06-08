from tkinter import *
from threading import Thread
import socket

# App version
VERSION = "1.5.3"

# Client global variables
BUFFER = 1024
FORMAT = "utf-8"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receive_from_server(choice, text, username, password):
	# Pack the list of information into a string
	string = str([choice, str(text), str(username), str(password)])
	# Send it
	server_socket.sendall(string.encode(FORMAT))
	# Return what the server replied
	return server_socket.recv(BUFFER).decode(FORMAT)


def send_to_server(choice, text, username, password):
	# Pack the list of information into a string
	string = str([choice, str(text), str(username), str(password)])
	# Send it
	server_socket.sendall(string.encode(FORMAT))


class ServerPage:
	def __init__(self, root, color):
		self.root = root
		self.root.geometry("300x250")
		self.root.minsize(300, 250)
		self.main_color = color

	def config(self):
		# Config the server widgets
		self.general_frame = Frame(self.root, bg=self.main_color)
		self.first_frame = Frame(self.general_frame, bg=self.main_color)
		self.second_frame = Frame(self.general_frame, bg=self.main_color)
		self.third_frame = Frame(self.general_frame, bg=self.main_color)
		self.ip_label = Label(self.first_frame, text="Server IP", bg=self.main_color)
		self.port_label = Label(self.first_frame, text="Server Port", bg=self.main_color)
		self.ip_entry = Entry(self.first_frame, relief=FLAT)
		self.port_entry = Entry(self.first_frame, relief=FLAT)
		self.connect_button = Button(self.second_frame, text="Connect", command=self.connect, relief=FLAT)
		self.wrong_text_label = Label(self.third_frame, text="", bg=self.main_color)

		# Draw the server widgets
		self.general_frame.pack(expand=True)
		self.first_frame.pack()
		self.second_frame.pack()
		self.third_frame.pack()
		self.ip_label.pack(pady=5)
		self.ip_entry.pack(pady=5)
		self.port_label.pack(pady=5)
		self.port_entry.pack(pady=5)
		self.connect_button.pack(pady=5)
		self.wrong_text_label.pack(pady=5)

	def connect(self):
		self.host = self.ip_entry.get()
		self.port = self.port_entry.get()

		if self.host and self.port:
			# Try to connect to the server
			try:
				server_socket.connect((self.host, int(self.port)))
				self.quit()
			except Exception:
				self.reset_entry(self.ip_entry, self.port_entry)
				self.wrong_text_label["text"] = "Can't connect to the server"
		else:
			self.reset_entry(self.ip_entry, self.port_entry)
			self.wrong_text_label["text"] = "Insert valid credentials"

	def reset_entry(self, *args):
		for arg in args:
			arg.delete(0, END)

	def quit(self):
		self.general_frame.destroy()
		self.first_frame.destroy()
		self.second_frame.destroy()
		self.third_frame.destroy()
		self.root.quit()

	def loop(self):
		self.root.mainloop()


class LoginPage:
	def __init__(self, root, color):
		self.root = root
		self.root.geometry("300x250")
		self.root.minsize(300, 250)
		self.main_color = color

	def config(self):
		# Config the login widgets
		self.general_frame = Frame(self.root, bg=self.main_color)
		self.first_frame = Frame(self.general_frame, bg=self.main_color)
		self.second_frame = Frame(self.general_frame, bg=self.main_color)
		self.third_frame = Frame(self.general_frame, bg=self.main_color)
		self.username_label = Label(self.first_frame, text="Username", bg=self.main_color)
		self.password_label = Label(self.first_frame, text="Password", bg=self.main_color)
		self.username_entry = Entry(self.first_frame, relief=FLAT)
		self.password_entry = Entry(self.first_frame, show='*', relief=FLAT)
		self.login_button = Button(self.second_frame, text="Login", command=self.login, relief=FLAT)
		self.register_button = Button(self.second_frame, text="Register", command=self.register, relief=FLAT)
		self.wrong_text_label = Label(self.third_frame, text="", bg=self.main_color)

		# Draw the login widgets
		self.general_frame.pack(expand=True)
		self.first_frame.pack()
		self.second_frame.pack()
		self.third_frame.pack()
		self.username_label.pack(pady=5)
		self.username_entry.pack(pady=5)
		self.password_label.pack(pady=5)
		self.password_entry.pack(pady=5)
		self.login_button.pack(side="left", padx=5, pady=5)
		self.register_button.pack(side="right", padx=5, pady=5)
		self.wrong_text_label.pack(pady=5)

	def login(self):
		# Get the entry text
		self.username = self.username_entry.get()
		self.password = self.password_entry.get()

		# Check if username and password aren't empty
		if self.username and self.password:
			# Ask to the server the list of accounts
			accounts = eval(receive_from_server("read_log_database", None, None, None))

			# Check if the account correspond to someone
			registered = False
			# If there's almost one account ("no_accounts" is a flag variable)
			if accounts[0] != "no_accounts":
				for acc in accounts:
					acc = acc.split()
					if acc[0] == self.username and acc[1] == self.password:
						registered = True
						break

			# If there's no account with these credentials reset the entries and label it
			if not registered:
				self.reset_entry(self.username_entry, self.password_entry)
				self.wrong_text_label["text"] = "Login failed"
			# Else label it
			else:
				self.wrong_text_label["text"] = "Login is successful"
				self.quit()
		else:
			self.reset_entry(self.username_entry, self.password_entry)
			self.wrong_text_label["text"] = "Insert valid credentials"

	def register(self):
		# Get the entry text
		self.username = self.username_entry.get()
		self.password = self.password_entry.get()

		# Check if username and password aren't empty
		if self.username and self.password and '_' not in self.username and ' ' not in self.username and ' ' not in self.password and self.username != '*' and len(self.username) <= 20 and len(self.password) <= 20:
			# Ask the server the list of the accounts
			accounts = eval(receive_from_server("read_log_database", None, None, None))

			# Check if the account already exists
			registered = False
			# If there's almost one account ("no_accounts" is a flag variable)
			if accounts[0] != "no_accounts":
				for acc in accounts:
					acc = acc.split()
					if acc[0] == self.username:
						registered = True
						break

			# If there's also an account already registered reset the entries and label it
			# Else write the credential into the database and label it
			if registered:
				self.reset_entry(self.username_entry, self.password_entry)
				self.wrong_text_label["text"] = "Account already registered"
			else:
				send_to_server("write_log_database", None, self.username, self.password)
				self.wrong_text_label["text"] = "Registration is successful"
				self.quit()
		else:
			self.reset_entry(self.username_entry, self.password_entry)
			self.wrong_text_label["text"] = "Insert valid credentials"

	def reset_entry(self, *args):
		for arg in args:
			arg.delete(0, END)

	def quit(self):
		self.general_frame.destroy()
		self.first_frame.destroy()
		self.second_frame.destroy()
		self.third_frame.destroy()
		self.root.quit()

	def loop(self):
		self.root.mainloop()
		return self.username, self.password


class RoomPage:
	def __init__(self, root, color):
		self.root = root
		self.root.geometry("350x300")
		self.root.minsize(350, 300)
		self.main_color = color

	def config(self):
		# Config the room page widgets
		self.general_frame = Frame(self.root, bg=self.main_color)
		self.first_frame = Frame(self.general_frame, bg=self.main_color)
		self.second_frame = Frame(self.general_frame, bg=self.main_color)
		self.room_listbox = Listbox(self.first_frame, bg=self.main_color, selectmode="single", font="consolas 10", relief=FLAT)
		self.room_entry = Entry(self.second_frame, relief=FLAT)
		self.add_room_button = Button(self.second_frame, text="+", command=self.create, height=1, relief=FLAT)
		self.enter_room_button = Button(self.second_frame, text="Join", command=self.join, height=1, relief=FLAT)

		# Get from the server the list of rooms of the server, and insert each room on the room list box
		rooms = eval(receive_from_server("read_room_database", None, None, None))
		if rooms[0] != "no_rooms":
			for i in range(len(rooms)):
				self.room_listbox.insert(i, rooms[i])

		self.general_frame.pack(fill=BOTH, expand=True)
		self.first_frame.pack(fill=BOTH, expand=True, side=TOP)
		self.second_frame.pack(fill=BOTH, side=BOTTOM)
		self.room_listbox.pack(fill=BOTH, expand=True, padx=5, pady=10)
		self.room_entry.pack(fill=BOTH, expand=True, side="left", padx=5, pady=10)
		self.add_room_button.pack(fill=Y, side="left", padx=5, pady=10)
		self.enter_room_button.pack(fill=Y, side="right", padx=5, pady=10)

		# Bind the selection of an item of the list box as the copy of its content in the entry room
		self.room_listbox.bind("<<ListboxSelect>>", self.listbox_selection)

	def listbox_selection(self, selection):
		self.reset_entry(self.room_entry)
		self.room_entry.insert("0", self.room_listbox.get(ANCHOR))

	def join(self):
		self.room = self.room_entry.get()

		if self.room:
			self.reset_entry(self.room_entry)
			rooms = eval(receive_from_server("read_room_database", None, None, None))

			# Check if the room exists
			room_existence = False
			# If there's almost one room ("no_rooms" is a flag variable)
			if rooms[0] != "no_rooms":
				for room in rooms:
					if room == self.room:
						room_existence = True
						break

			if room_existence:
				self.room_entry.insert("0", "Joining room")
				self.quit()
			else:
				self.room_entry.insert("0", "Room doesn't exist")
		else:
			self.reset_entry(self.room_entry)
			self.room_entry.insert("0", "Insert valid credentials")

	def create(self):
		self.room = self.room_entry.get()

		self.reset_entry(self.room_entry)
		if self.room and ' ' not in self.room and self.room != '*' and len(self.room) <= 20:
			rooms = eval(receive_from_server("read_room_database", None, None, None))

			# Check if the room exists
			room_existence = False
			# If there's almost one room ("no_rooms" is a flag variable)
			if rooms[0] != "no_rooms":
				for room in rooms:
					if room == self.room:
						room_existence = True
						break

			if room_existence:
				self.room_entry.insert("0", "Room already created")
			else:
				send_to_server("write_room_database", self.room, None, None)
				self.room_entry.insert("0", "Creating room")
				self.quit()

		else:
			self.room_entry.insert("0", "Insert valid credentials")

	def reset_entry(self, *args):
		for arg in args:
			arg.delete(0, END)

	def quit(self):
		self.general_frame.destroy()
		self.first_frame.destroy()
		self.second_frame.destroy()
		self.root.quit()

	def loop(self):
		self.root.mainloop()
		return self.room


class MainPage:
	def __init__(self, root, color, username, password, room):
		self.root = root
		self.root.geometry("800x600")
		self.root.minsize(500, 550)
		self.main_color = color
		self.username = username
		self.password = password
		self.room = room

	def config(self):
		# Config the main window widgets
		self.first_frame = Frame(self.root, bg=self.main_color)
		self.second_frame = Frame(self.root, bg=self.main_color)
		self.third_frame = Frame(self.root, bg=self.main_color)
		self.home_label = Label(self.first_frame, text=self.room, bg=self.main_color)
		self.user_label = Label(self.first_frame, text=self.username, bg=self.main_color)
		self.messages_text = Text(self.second_frame, font="consolas 10", height=18, bg="RoyalBlue4", fg="snow3", relief=FLAT)
		# In particular, config the Checkbutton for "reading news mode"
		self.reading_loop_variable = IntVar()
		self.reading_loop_checkbutton = Checkbutton(self.second_frame, text="Reading news mode", bg=self.main_color,
													variable=self.reading_loop_variable, command=self.read)
		self.post_text = Text(self.third_frame, font="ubuntu 10", width=40, height=2, relief=FLAT)
		self.post_button = Button(self.third_frame, text="Post", width=4, command=self.post, relief=FLAT)

		# In particular, set the tags that will generate different foreground colors for
		# the user and the message into the message_text widget
		self.messages_text.tag_add("user", "1.0", END)
		self.messages_text.tag_add("message", "1.0", END)
		self.messages_text.tag_config("user", font="consolas 10", foreground="dark orange")
		self.messages_text.tag_config("message", font="consolas 10")

		# Draw the main widgets
		self.first_frame.pack(fill=X)
		self.second_frame.pack(fill=BOTH, expand=True)
		self.third_frame.pack(fill=X)
		self.home_label.pack(side="left", padx=5, pady=10)
		self.user_label.pack(side="right", padx=5, pady=10)
		self.messages_text.pack(fill=BOTH, expand=True, padx=5, pady=10)
		self.reading_loop_checkbutton.pack(side="left", padx=5, pady=10)
		self.post_text.pack(fill=BOTH, expand=True, side="left", padx=5, pady=10)
		self.post_button.pack(fill=Y, side="right", padx=5, pady=10)

	def post(self):
		# Just take the text written in the Text widget
		text = self.post_text.get("1.0", END)
		# Replace every "\n" with nothing --> yes, you can't go to a new line
		text = text.replace('\n', '')

		self.reset_text(self.post_text)
		# If it is empty write it
		if not text:
			self.post_text.insert(1.0, "Insert a valid text")
		# Else if the length of the message is bigger than the buffer, write it
		elif len(text) > BUFFER:
			self.post_text.insert(1.0, f"You can't send more than {BUFFER} characters")
		# Else if the message is good
		else:
			# Send to server the text, the username of that text and the actual room
			send_to_server("post_text_database", text, self.username, self.room)

	def read(self):
		# Ask to the server the sorted by date list of the messages
		text_files = eval(receive_from_server("read_sorted_text_database", self.room, None, None))

		# If there's almost one account ("no_text" is a flag variable)
		if text_files[0] != "no_text":
			self.messages_text["state"] = "normal"
			self.reset_text(self.messages_text)

			# For all the files in the array insert the content in the message_text widget
			for file in text_files:
				title = file.split('_')[0]

				# Ask to the server the content of the current file
				string = receive_from_server("read_text_database", file, self.room, None)

				# Write in the messages Text widget the title (the sender) and the string (the message)
				# in different colors
				self.messages_text.insert(END, title+": ", "user")
				self.messages_text.insert(END, string+"\n", "message")

			self.messages_text.see(END)

		self.messages_text["state"] = "disabled"

		# If the "reading news mode" is on, update every second the Text widget
		if self.reading_loop_variable.get():
			self.messages_text.after(1000, self.read)

	def reset_text(self, *args):
		for arg in args:
			arg.delete("1.0", END)

	def loop(self):
		# Reading is a matter of threading
		Thread(target=self.read).start()
		self.root.mainloop()
		# If the user (client) close the window, close the socket connection
		server_socket.close()


def main():
	# Create the main general window
	main_color = "dim gray"
	general_root = Tk()
	general_root.title(f"GroupChat {VERSION}")
	general_root.configure(bg=main_color)
	general_root.resizable(True, True)

	# Generate the Server Page window
	server_p = ServerPage(general_root, main_color)
	server_p.config()
	server_p.loop()

	# Generate the Login Page window
	log_p = LoginPage(general_root, main_color)
	log_p.config()
	username, password = log_p.loop()

	# Generate the Room Page window
	room_p = RoomPage(general_root, main_color)
	room_p.config()
	room = room_p.loop()

	# Generate the Main Page window
	main_p = MainPage(general_root, main_color, username, password, room)
	main_p.config()
	main_p.loop()


if __name__ == "__main__":
	main()