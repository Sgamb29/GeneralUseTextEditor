
from tkinter import *
from tkinter import scrolledtext, filedialog, messagebox
from sys import argv
from datetime import datetime
from os import path
import json

print(argv)

settings = {
	"color_scheme": "black",
}


def get_save_file():
	script_dir = path.dirname(__file__) + "/"
	opts_save = script_dir + "settings_pyeditor.json"
	return opts_save

def load_opts():
	global settings
	try:
		with open(get_save_file(), "r") as f:
			return json.load(f)
	except FileNotFoundError:
		return settings



file = ""
if len(argv) == 2:
	file = argv[1]

keypress_count = 0


def open_file():
	global file
	if not file:
		file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
	else:
  		file_path = file
	if file_path:
		try:
			with open(file_path, 'r') as f:
				text.delete(1.0, END)
				text.insert(END, f.read())
				display.config(text=file_path)
				file_opened = True
		except FileNotFoundError:
			display.config(text=file_path)
			file_opened = True

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, 'w') as f:
            f.write(text.get(1.0, END))
            display.config(text=file_path)

        keypress_count = 0

    global current_text
    current_text = text.get(1.0, END)

def save_default(*args):
	global file
	global keypress_count
	if not file:
		save_file()
		return
	with open(file, "w") as f:
		f.write(text.get(1.0, END))
		display.config(text=file)
	
	keypress_count = 0

	global current_text
	current_text = text.get(1.0, END)


def indicate_no_save(*args):
	global keypress_count
	global current_text
	changed_text = text.get(1.0, END)
	if current_text == changed_text:
		return
	else:
		# Key press count is a bit of a lazy hack to make sure to ask for save on close
		# Used in window exit function
		keypress_count = 3
	if "*" not in display["text"]:
		display.config(text=display["text"] + " *")
		
def close_hotkey(*args):
	choice = False
	if keypress_count >= 3:
		choice = ask_for_save()
	if choice == None:
		return
	elif choice == True:
		save_default()
	
	root.quit()

def minimize(*args):
	root.iconify()

def input_date(*args):
	current_date = datetime.now()
	date_str = current_date.strftime("%A %B %d, %Y")
	text.insert(INSERT, date_str)

def input_break(*args):
	break_str = "-" * 80
	text.insert(INSERT, break_str)


def ask_for_save():
	return messagebox.askyesnocancel(message="Save Before Closing?", icon="warning")

def window_exit():
	to_save = False
	if keypress_count >= 3:
		to_save = messagebox.askyesno(title="Unsaved Work", message="Save Before Closing?", icon="warning")
	if to_save:
		save_default()

	root.destroy()


def jump_to_bottom(*args):
	text.see(END)

def jump_to_top(*args):
	text.see(1.0)


root = Tk()
root.title("Text Editor")
root.bind("<Control-s>", save_default)
root.bind("<KeyPress>", indicate_no_save)
root.bind("<Control-w>", close_hotkey)
root.bind("<Control-minus>", minimize)
root.bind("<Control-equal>", input_date)
root.bind("<Control-plus>", input_break)
root.bind("<Control-g>", jump_to_bottom)
root.bind("<Control-G>", jump_to_top)

root.protocol("WM_DELETE_WINDOW", window_exit)

root.attributes("-zoomed", True)

display = Label(root, text="Text Editor")
display.pack()

text = scrolledtext.ScrolledText(root, wrap=WORD, bg="black", fg="white", insertbackground="white", font=("Times New Roman", 18), undo=True)
text.pack(expand=True, fill="both")

# To see the properties of a widget
#print(text.config())

menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)


def save_opts():
	global settings
	with open(get_save_file(), "w") as f:
		json.dump(settings, f)


def change_scheme(bg, fg):
	global settings
	text["background"] = bg
	text["foreground"] = fg
	text["insertbackground"] = fg
	settings["color_scheme"] = bg
	save_opts()


edit_menu = Menu(menu_bar)
menu_bar.add_cascade(label="Themes", menu=edit_menu)
edit_menu.add_command(label="Color Scheme: default", command= lambda: change_scheme("black", "white"))
edit_menu.add_command(label="Color Scheme: green", command= lambda: change_scheme("green", "white"))
edit_menu.add_command(label="Color Scheme: pink", command= lambda: change_scheme("pink", "purple"))
edit_menu.add_command(label="Color Scheme: blue", command= lambda: change_scheme("lightblue", "blue"))
edit_menu.add_command(label="Color Scheme: light", command= lambda: change_scheme("white", "black"))

# Testing different colors
edit_menu.add_command(label="Color Scheme: seagreen", command= lambda: change_scheme("seagreen4", "black"))
edit_menu.add_command(label="Color Scheme: moccasin", command= lambda: change_scheme("moccasin", "black"))
edit_menu.add_command(label="Color Scheme: gray", command= lambda: change_scheme("gray21", "white"))




opts = load_opts()
if opts["color_scheme"] == "black":
	change_scheme("black", "white")
elif opts["color_scheme"] == "green":
	change_scheme("green", "white")
elif opts["color_scheme"] == "pink":
	change_scheme("pink", "purple")
elif opts["color_scheme"] == "lightblue":
	change_scheme("lightblue", "blue")
elif opts["color_scheme"] == "white":
	change_scheme("white", "black")
elif opts["color_scheme"] == "seagreen4":
	change_scheme("seagreen4", "black")
elif opts["color_scheme"] == "moccasin":
	change_scheme("moccasin", "black")
elif opts["color_scheme"] == "gray21":
	change_scheme("gray21", "white")

is_file_arg = False
file_opened = False
if len(argv) > 1 and not file_opened:
	is_file_arg = True
	open_file()


# Getting current text to check when need to save
current_text = text.get(1.0, END)

root.mainloop()
