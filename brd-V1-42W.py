"""BBC Radio Downloader V1.42W

By Steve Shambles Nov 2019 and Jan 2020
stevepython.wordpress.com
-------------------------------------------------
Currently for Windows 7 and higher only.

Requirements:
pip3 install pyperclip

FFmpeg installed from: ffmpeg.org

get_iplayer installed from:
https://github.com/get-iplayer/get_iplayer/releases
----------------------------------------------------
V1.42 - Added categories menu links and view and delete history menu.
V1.41 - Addded visit last url download in right click menu. Stored in txt file
        so available next time use program. Changed url of find shows to categories page.
V1.40 - Ran thru Pylint fixed what I could. Code tidy up. Play tested to hell.
        Renamed program to BBC Radio Downloader.
V1.39 - Explaination of bitrates in pop. Github menu link.
V1.38 - Added error trapping. Before clking on empty list, or no file properly
        selected would cause error. Also added clear entry box option in
        right click menu for user convience.I found it useful anyway.
V1.37 - Added proper exit program points, 3 of them. The x in window,
        via rclick menu and drop-down menu option.
V1,36 - Added right click menu.Moved delete file and convert to mp3 there.
V1.35 - Added menu option to change bitrate when converting to mp3
        and all the stuff related to this option.
V1.34 - Added menu option to delete selected file for convience.
V1.33 - Removed .m4a from converted to mp3 file name.
V1.32 - Cleared input box after started downloading so user
        can see when a new address is pasted in.

# How to tell when process has completed?
# No file selected error. What exception error should I use?
"""
import functools as ft
import getpass
import os
import sys
from pathlib import Path
from shutil import copyfile
import subprocess
from tkinter import BOTTOM, Button, E, END, Entry, IntVar, LabelFrame, Listbox
from tkinter import Menu, messagebox, RIGHT, Scrollbar, Tk, W, X, Y
import time
import webbrowser

import pyperclip

root = Tk()
root.title('BBC Radio Downloader V1.42W.')
root.geometry('413x355')



class Glo():
    """Global storage."""
    bit_rate = '128k' # Default bitrate.
    last_paste = ''   # Stores last paste url permanetly

# If last_paste.txt not found create blank one.
if not os.path.exists('last_paste.txt'):
    with open('last_paste.txt', 'w') as contents:
        pass

def visit_last_url():
    with open('last_paste.txt', 'r') as contents:
        Glo.last_paste = contents.read()
        if Glo.last_paste.startswith('https://www.bbc.co.uk/'):
            webbrowser.open(Glo.last_paste)


def dwnld_show():
    """Send command to get_iplayer to download show."""
    clpbrd_url = pyperclip.paste()

    if not clpbrd_url.startswith('https://www.bbc.co.uk/'):
        messagebox.showerror('Error', 'This does not llok like a valid BBC URL')
        return

    ask_yn = messagebox.askyesno('Question', 'Download show from pasted URL?')
    if ask_yn is False:
        return

    # Save the pasted address.
    Glo.last_paste = clpbrd_url
    with open('last_paste.txt', 'w') as contents:
        contents.write(str(Glo.last_paste))

    clear_entrybox()

    # Execute get_iplayer command.
    run_cmd = r'C:\Windows\System32\cmd.exe /kget_iplayer.cmd '  \
               +str(clpbrd_url)+' --type=radio'
    subprocess.Popen(run_cmd)

def clk_but():
    """Go to BBC Sounds website to manually find show URL."""
    webbrowser.open('https://www.bbc.co.uk/sounds/categories')

def on_right_click(event):
    """Enter URL from the clipboard into entry box."""
    clpbrd_url = pyperclip.paste()
    url_ent_box.delete(0, END)
    url_ent_box.insert(0, str(clpbrd_url))

def rcrdngs_folder():
    """Open the recordings folder in file explorer found in
       logged in users desktop."""
    sys_user = getpass.getuser()
    webbrowser.open('C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings')

def convert_2_mp3():
    """On right click convert selected file to mp3."""
    if not lst_bx.curselection(): # If no line selected.
        messagebox.showerror('Error:', 'No file selected')
        return

    q_yn = messagebox.askyesno('Question',
                               'Convert selected file to '
                               +str(Glo.bit_rate)+' mp3?')

    if q_yn is False:
        return

    sys_user = getpass.getuser()
    folder_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'
    os.chdir(folder_path)
    selection = lst_bx.curselection()
    slctd_file = lst_bx.get(selection[0])

    # Check file selected is .m4a to prevent re-encoding an mp3.
    if slctd_file.endswith('.mp3'):
        messagebox.showinfo('Notice!', 'File already converted.')
        return

    # Remove .m4a from filename add bitrate used as part of filename.
    renamed_file = slctd_file.replace('.m4a', '-'+str(Glo.bit_rate))

    # Set up FFmpeg command and execute it.
    br_str = ' -b:a '+str(Glo.bit_rate)+' '
    ff_comm = "ffmpeg -y -i "+str(slctd_file)+str(br_str)+str(renamed_file)+".mp3"
    subprocess.Popen(ff_comm)

def play_file(event):
    """Play file when double clicked on in the recordings list box."""
    if not lst_bx.curselection(): # If no line selected.
        messagebox.showerror('Error:', 'No file selected')
        return

    sys_user = getpass.getuser()
    folder_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    file_2_play = folder_path+'/'+str(value)
    webbrowser.open(file_2_play)

def get_list_of_recordings():
    """Search recordings folder for files and list them in listbox."""
    radio_files = [] # Clear list of files.
    lst_bx.delete('0', 'end')# Clear listbox.
    sys_user = getpass.getuser()# Get sytems user name.
    rec_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'

    for eachfile in Path(rec_path).glob('**/*.*'):
        radio_files.append(str(eachfile))

    # Print the list of files in the listbox.
    for hit in radio_files:
        file_name = (os.path.basename(hit))
        # skip if the file is last_paste.txt or history.txt
        if not file_name.endswith('.txt'):
            lst_bx.insert('end', file_name)

def del_sel_file():
    """Delete file selected by user in the list box."""
    # Get the path and change dir.
    sys_user = getpass.getuser()# Get sytems user name.
    rec_path = 'C:/Users/'+str(sys_user)+'/Desktop/iPlayer Recordings'
    os.chdir(rec_path)

    # Get the file that is selected in the list box.
    try:
        selection = lst_bx.curselection()
        slctd_file = lst_bx.get(selection[0])
    except:
        messagebox.showerror('Error:', 'No file selected')
        return # no file selected. What exception error should I use?

    qu_yn = messagebox.askyesno('Question', 'Delete selected file?')
    if qu_yn is False:
        return

    # Delete the file.
    os.remove(slctd_file) #How to tell when process has completed?
    time.sleep(1.5) # Arbirary guess work for now, lol.

    # Refresh the list box.
    get_list_of_recordings()

def about_menu():
    """About program menu text."""
    messagebox.showinfo('Program Information', 'BBC Radio Downloader V1.42W\n'
                        'Freeware. By Steve Shambles, Jan 2020\n\n'
                        'This program uses Get_iplayer and FFMpeg.\n'
                        'These programs need to be installed on your'
                        ' system first.'
                        '\n\nPlease refer to the links in the Help menu.')

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
                        '6: After download, click "Refresh Recordings List" button.\n\n'
                        '7: Double click on a file to play it.\n\n'
                        '8: Right click on a file to convert it to mp3 if req.\n\n'
                        '9: Click "Open recordings folder" to edit files.\n\n'
                        'A detailed visual step by step guide is also avaiable\n'
                        'online from this menu.')

def visit_blog():
    """Visit my python blog, you know it makes sense."""
    webbrowser.open('https://stevepython.wordpress.com/')

def visit_github():
    """Visit Github page for latest source code."""
    webbrowser.open('https://github.com/steveshambles/BBC-Radio-show-downloader')

def online_help():
    """Step by step online tutorial on using this app."""
    webbrowser.open('https://stevepython.wordpress.com/bbc-radio-downloader-help')

def get_ffmpeg():
    """Visit ffmpeg website for install."""
    webbrowser.open('https://ffmpeg.org')

def get_iplyr():
    """Visit get_iplayer website for install."""
    webbrowser.open('https://github.com/get-iplayer/get_iplayer/releases')


def exit_app():
    """Yes-no requestor to exit program."""
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to quit BBC Radio '
                                 'Downloader?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()

def clear_entrybox():
    """Clear entry box of any previous text."""
    url_ent_box.delete(0, END)

def pop_up(event):
    """On right click display popup menu at mouse position."""
    rc_menu.post(event.x_root, event.y_root)

def cat_menu(address):
    webbrowser.open(address)

def view_dl_history():
    
    sys_user = getpass.getuser()
    file_nme = 'C:/Users/'+str(sys_user)+'/.get_iplayer/download_history'

    if not os.path.exists(file_nme):
        messagebox.showerror('Error!', 'No download history file found')
        return
    
    # Copy history file to current dir, add .txt extension and open.
    copyfile(file_nme, 'history.txt')
    time.sleep(1)
    webbrowser.open('history.txt')

def delete_history ():
    ask_yn = messagebox.askyesno('Question',
                                 'Are you sure you want to delete your '
                                 'download history?'
                                 '\n\nThis action cannot be undone.')
    if ask_yn is False:
        return

    if os.path.exists('history.txt'):
        os.remove('history.txt')

    sys_user = getpass.getuser()
    file_nme = 'C:/Users/'+str(sys_user)+'/.get_iplayer/download_history'
    if os.path.exists(file_nme):
        os.remove(file_nme)

    messagebox.showinfo('Deleted!', 'Your download history has been deleted')


radio_frame = LabelFrame(root)
radio_frame.grid(padx=10, pady=10)

# Go to bbc sounds website to manually find a url.
go_bbc_radio_btn = Button(radio_frame, bg='limegreen',
                          text='Find shows', command=clk_but)
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

# Scrollbars for listbox.
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
lst_bx.bind('<Button-3>', pop_up) # Right click pop up menu.
get_list_of_recordings()

# Bottom window for refreesh and open folder buttons.
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

# Help Drop-down menu.
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Help', menu=file_menu)
file_menu.add_command(label='Quick help', command=help_menu)
file_menu.add_command(label='Detailed help', command=online_help)
file_menu.add_command(label='About', command=about_menu)
file_menu.add_separator()
file_menu.add_command(label='Install FFMpeg page', command=get_ffmpeg)
file_menu.add_command(label='Install get_iplayer page', command=get_iplyr)
file_menu.add_separator()
file_menu.add_command(label='Visit my blog for Python goodies', command=visit_blog)
file_menu.add_command(label='BBC Radio Downloader on GitHub', command=visit_github)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=exit_app)

### Categories menu
file_menu2 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Categories', menu=file_menu2)
file_menu2.add_command(label='Browse all categories',
                       command=ft.partial(cat_menu,
                                          'https://www.bbc.co.uk/sounds/categories'))
file_menu2.add_separator()
file_menu2.add_command(label='Audiobooks',  command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/audiobooks?sort=latest'))
file_menu2.add_command(label='Comedy',  command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/comedy?sort=latest'))
file_menu2.add_command(label='Drama', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/drama?sort=latest'))
file_menu2.add_command(label='Documentaries', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/documentaries?sort=latest'))
file_menu2.add_command(label='Health and wellbeing', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/factual-healthandwellbeing?sort=latest'))
file_menu2.add_command(label='Podcasts', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/podcasts?sort=latest'))
file_menu2.add_command(label='Sport', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/sport?sort=latest'))
file_menu2.add_command(label='Technology', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/factual-scienceandnature-scienceandtechnology?sort=latest'))
file_menu2.add_separator()
file_menu2.add_command(label='Classical music', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/music-classical?sort=latest'))
file_menu2.add_command(label='Dance and Electro music', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/music-danceandelectronica?sort=latest'))
file_menu2.add_command(label='Hip Hop, RnB, Dancehall music', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/music-hiphoprnbanddancehall?sort=latest'))
file_menu2.add_command(label='Pop and chart music', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/music-popandchart?sort=latest'))
file_menu2.add_command(label='Rock and Indie music', command=ft.partial(cat_menu,
                                                           'https://www.bbc.co.uk/sounds/category/music-rockandindie?sort=latest'))


def convert_64():
    """Menu option to select 64kbs mp3 conversion, with advice."""
    Glo.bit_rate = '64k'
    messagebox.showinfo('MP3 Bitrate', 'When you right click on a file'
                        '\nto convert it to mp3,\n\n64Kbps will be used.\n'
                        '\nThis will produce small files of low quality.'
                        '\nIs quick to convert.'
                        '\nUsable quality for radio shows, just about.'
                        '\n\nUseful if you are tight on disk space.')
    br_64.set(1)
    br_128.set(0)
    br_160.set(0)
    br_192.set(0)
    br_256.set(0)

def convert_128():
    """Menu option to select 128kbs mp3 conversion, with advice. The default rate."""
    Glo.bit_rate = '128k'
    messagebox.showinfo('MP3 Bitrate', 'When you right click on a file'
                        '\nto convert it to mp3,\n\n128Kbps will be used.\n'
                        '\nThis will produce fairly small files,'
                        '\nis quick to convert.'
                        '\nDecent quality.\n\nRecommended for radio shows.')
    br_64.set(0)
    br_128.set(1)
    br_160.set(0)
    br_192.set(0)
    br_256.set(0)

def convert_160():
    """Menu option to select 160kbs mp3 conversion, with advice."""
    Glo.bit_rate = '160k'
    messagebox.showinfo('MP3 Bitrate', 'When you right click on a file'
                        '\nto convert it to mp3,\n\n160Kbps will be used.\n'
                        '\nThis will produce large-ish files,'
                        '\nbut of good quality.'
                        '\n\nFor inbetweeners.')
    br_64.set(0)
    br_128.set(0)
    br_160.set(1)
    br_192.set(0)
    br_256.set(0)

def convert_192():
    """Menu option to select 192kbs mp3 conversion, with advice."""
    Glo.bit_rate = '192k'
    messagebox.showinfo('MP3 Bitrate', 'When you right click on a file'
                        '\nto convert it to mp3,\n\n192Kbps will be used.\n'
                        '\nThis will produce fairly large files,'
                        '\nbut of very good quality.\n'
                        '\nTakes a while to convert to mp3.\n\n'
                        'Recommended for music files.')
    br_64.set(0)
    br_128.set(0)
    br_160.set(0)
    br_192.set(1)
    br_256.set(0)

def convert_256():
    """Menu option to select 256kbs mp3 conversion, with advice."""
    Glo.bit_rate = '256k'
    messagebox.showinfo('MP3 Bitrate', 'When you right click on a file'
                        '\nto convert it to mp3,\n\n256Kbps will be used.\n'
                        '\nThis will produce large files,'
                        '\nbut of the best quality availble.'
                        '\nTakes quite a while to convert to mp3.'
                        '\n\nFor quality addicts.')
    br_64.set(0)
    br_128.set(0)
    br_160.set(0)
    br_192.set(0)
    br_256.set(1)

# Set up bitrate checkbutton menu start up state.
br_64 = IntVar()
br_160 = IntVar()
br_192 = IntVar()
br_256 = IntVar()

br_128 = IntVar()
br_128.set(1) # Start off 128k as default menu option.

# Bitrates menu.
file_menu3 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Bitrates', menu=file_menu3)
file_menu3.add_checkbutton(label=' 64kbps', variable=br_64,
                           command=convert_64)
file_menu3.add_checkbutton(label='128kbps - Speech', variable=br_128,
                           command=convert_128)
file_menu3.add_checkbutton(label='160Kbps', variable=br_160,
                           command=convert_160)
file_menu3.add_checkbutton(label='192Kbps - Music', variable=br_192,
                           command=convert_192)
file_menu3.add_checkbutton(label='256Kbps', variable=br_256,
                           command=convert_256)


# History menu.
file_menu4 = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='History', menu=file_menu4)
file_menu4.add_command(label='View download history', command=view_dl_history)
file_menu4.add_command(label='Delete history', command=delete_history)




root.config(menu=menu_bar)

# Create right click popup menu.
rc_menu = Menu(root, tearoff=0)
rc_menu.add_command(label='Clear URL entry box', command=clear_entrybox)
rc_menu.add_command(label='Visit last URL download', command=visit_last_url)
rc_menu.add_separator()
rc_menu.add_command(label='Convert file to mp3', command=convert_2_mp3)
rc_menu.add_command(label='Delete file', command=del_sel_file)
rc_menu.add_separator()
rc_menu.add_command(label='Quit program', command=exit_app)

# calls quit if window close is clicked.
root.protocol("WM_DELETE_WINDOW", exit_app)

root.mainloop()
