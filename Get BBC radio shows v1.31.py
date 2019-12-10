"""Get BBC radio shows V1.31

By Steve Shambles Nov 2019
stevepython.wordpress.com

Currently for Windows 7 and higher only.

Requirements:
pip3 install pyperclip

FFmpeg installed from: ffmpeg.org

get_iplayer installed from:
https://github.com/get-iplayer/get_iplayer/releases
"""
import getpass
import os
from pathlib import Path
import subprocess
from tkinter import BOTTOM, Button, E, END, Entry, LabelFrame, Listbox
from tkinter import Menu, messagebox, RIGHT, Scrollbar, Tk, W, X, Y
import webbrowser

import pyperclip

root = Tk()
root.title('Download BBC Radio Shows V1.31')
root.geometry('413x355')

def dwnld_show():
    """Send command to get_iplayer to download show"""
    ask_yn = messagebox.askyesno('Question', 'Download show from pasted URL?')
    if ask_yn is False:
        return

    clpbrd_url = pyperclip.paste()

    if not clpbrd_url.startswith('https://www.bbc.co.uk/sounds/'):
        messagebox.showerror('Error', 'This does not look like a valid URL')
        return

    run_cmd = 'C:\Windows\System32\cmd.exe /kget_iplayer.cmd '+str(clpbrd_url)+' --type=radio'
    subprocess.Popen(run_cmd)

def clk_but():
    """Go to BBC Sounds website to manually find show URL"""
    webbrowser.open('https://www.bbc.co.uk/sounds')

def on_right_click(event):
    """Enter URL from the clipboard into entry box."""
    clpbrd_url = pyperclip.paste()
    url_ent_box.delete(0, END)
    url_ent_box.insert(0, str(clpbrd_url))

def rcrdngs_folder():
    """Open the recordings folder in file explorer found in logged in users desktop"""
    sys_user = getpass.getuser()
    webbrowser.open('C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings')

def convert_2_mp3(event):
    """On right click convert selected file to mp3."""
    if lst_bx.curselection() is (): # If no line selected.
        return

    q_yn = messagebox.askyesno('Question', 'Convert selected file to mp3?')
    if q_yn is False:
        return

    global radio_files
    sys_user = getpass.getuser()
    folder_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'
    os.chdir(folder_path)
    widget = event.widget
    selection = widget.curselection()
    slctd_file = widget.get(selection[0])

    # Check file selecte is .m4a to prevent re-encoding an mp3.
    if slctd_file.endswith('.mp3'):
        messagebox.showinfo('Notice!', 'File already converted.')
        return
    
    # Set up FFmpeg command and execute it.
    ff_comm = "ffmpeg -y -i "+str(slctd_file)+" "+str(slctd_file)+".mp3"
    subprocess.Popen(ff_comm)

def play_file(event):
    """Play file double clicked on in the recordings list box"""
    sys_user = getpass.getuser()
    folder_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    file_2_play = folder_path+'/'+str(value)
    webbrowser.open(file_2_play)

def get_list_of_recordings():
    """Search recordings folder for files and list them in listbox"""
    global radio_files
    radio_files = [] # Clear list of files.
    lst_bx.delete('0', 'end')# Clear listbox.
    sys_user = getpass.getuser()# Get sytems user name
    rec_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'

    for eachfile in Path(rec_path).glob('**/*.*'):
        radio_files.append(str(eachfile))

    # Print the list of files in the listbox.
    for hit in radio_files:
        file_name = (os.path.basename(hit))
        lst_bx.insert('end', file_name)

def about_menu():
    """About program menu text."""
    messagebox.showinfo('Program Information', 'Download BBC Radio Shows V1.31\n'
                        'Freeware. By Steve Shambles, Nov 2019\n\n')

def help_menu():
    """How to use the program, menu help text."""
    messagebox.showinfo('How To...', 'Download BBC Radio Shows\n\n'
                        'Requires FFmpeg and get_iplayer,\n'
                        'links to those are in the help menu.\n\n'
                        '1: Click on the green "Finds shows" button.\n\n'
                        '2: Choose a program you want to download.\n\n'
                        '3: Copy the URL of the show to the clipboard.\n\n'
                        '4: Right click to paste the URL into the entry box.\n\n'
                        '5: Click the "Download" button.\n\n'
                        '6: After download, click orange "Refresh Recordings List" button.\n\n'
                        '7: Double click on a file to play it.\n\n'
                        '8: Right click on a file to convert it to mp3 if desired.\n\n'
                        '9: Click "Open recordings folder" to copy,delete or rename files\n\n.'
                        'A detailed visual step by step guide is also avaiable from this menu.')

def visit_blog():
    """Visit my python blog, you know it makes sense."""
    webbrowser.open('https://stevepython.wordpress.com/')

def online_help():
    """Step by step online tutorial on using this app."""
    webbrowser.open('https://stevepython.wordpress.com/2019/11/16/python-bbc-radio-download')

def get_ffmpeg():
    """Visit ffmpeg website for install"""
    webbrowser.open('https://ffmpeg.org')

def get_iplyr():
    """Visit get_iplayer website for install"""
    webbrowser.open('https://github.com/get-iplayer/get_iplayer/releases')

radio_frame = LabelFrame(root)
radio_frame.grid(padx=10, pady=10)

# Go to bbc sounds website to manually find a url.
go_bbc_radio_btn = Button(radio_frame, bg='limegreen', text='Find shows', command=clk_but)
go_bbc_radio_btn.grid(sticky=W+E, padx=5, pady=5, row=0, column=0)

# Entry box.
url_ent_box = Entry(radio_frame, bd=4)
url_ent_box.grid(sticky=W+E, padx=5, pady=5, row=0, column=1)
url_ent_box.delete(0, END)
url_ent_box.insert(0, 'Right click to paste URL')
url_ent_box.focus()
url_ent_box.bind('<Button-3>', on_right_click)

# Download button.
dwnld_btn = Button(radio_frame, bg='indianred', text='Download', command=dwnld_show)
dwnld_btn.grid(sticky=W+E, padx=5, pady=5, row=0, column=2)

# Listbox window.
message = 'Recordings: Double click to play, right click to convert file to mp3'
lbox_frame = LabelFrame(root, fg='blue', text=message)
lbox_frame.grid(padx=10, pady=10)

lst_bx = Listbox(
    master=lbox_frame,
    selectmode='single',
    width=52,
    height=10,
    fg='black',
    bg='lightgoldenrod'
    )

# Scrollbars for above listbox.
scrl_bar = Scrollbar(lbox_frame, orient='vertical')
scrl_bar.pack(side=RIGHT, fill=Y)
lst_bx.configure(yscrollcommand=scrl_bar.set)
scrl_bar.configure(command=lst_bx.yview)

scrl_bar2 = Scrollbar(lbox_frame, orient='horizontal')
scrl_bar2.pack(side=BOTTOM, fill=X)
lst_bx.configure(xscrollcommand=scrl_bar2.set)
scrl_bar2.configure(command=lst_bx.xview)

# Mouse button bindings.
lst_bx.pack()
lst_bx.bind('<Double-1>', play_file) # Dbl click to play file.
lst_bx.bind('<Button-3>', convert_2_mp3) # Right click to convert to mp3.
get_list_of_recordings()

# Bottom window.
bot_frame = LabelFrame(root)
bot_frame.grid(padx=10, pady=5)

# Refresh list button.
refresh_btn = Button(bot_frame, bg='darkorange',
                     text='Refresh recordings list', command=get_list_of_recordings)
refresh_btn.grid(row=0, column=0, sticky=W+E, padx=5, pady=5)

# Open recordings folder btn.
rcrdngs_btn = Button(bot_frame, bg='cornflowerblue',
                     text='Open recordings folder', command=rcrdngs_folder)
rcrdngs_btn.grid(row=0, column=1, sticky=W+E, padx=5, pady=5)

# Drop-down menu.
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Help menu', menu=file_menu)
file_menu.add_command(label='Quick help', command=help_menu)
file_menu.add_command(label='Detailed help', command=online_help)
file_menu.add_command(label='About', command=about_menu)
file_menu.add_separator()
file_menu.add_command(label='Install FFMpeg page', command=get_ffmpeg)
file_menu.add_command(label='Install get_iplayer page', command=get_iplyr)
file_menu.add_separator()
file_menu.add_command(label='Visit my blog for goodies', command=visit_blog)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.destroy)
root.config(menu=menu_bar)

root.mainloop()

#v1.31- Stopped mp3s being reencoded.
