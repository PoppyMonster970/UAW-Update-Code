import os
import sys
import glob
import ctypes
import winshell
import shutil
import pygame
import random
import threading
import tkinter as tk
import subprocess
import webbrowser
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox, Entry, Label, StringVar
from PIL import Image, ImageTk
import ctypes  # to check if we are admin
import threading
from shutil import copytree
from tkinter import ttk
from win32com.client import Dispatch

"""
def check():
 if len(sys.argv) < 2:
  print("Usage: python script.py <filename>")
  global check2
  check2 = 0
 else:
  check2 = 1
  global fileone
  fileone = sys.argv[1]
  print(fileone)

check()
  
if check2 == 1:
 print("file found")
 print(fileone)
else:
 print("No File Found")

os.system("pause>nul")
os.system("exit")
"""


def get_exe_location():
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys.executable
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.abspath(__file__)
    
    base_dir = os.path.dirname(bundle_dir)
    
    directories = {
        'base': base_dir,
        'game': os.path.join(base_dir, "Game\\Universe At War Earth Assault"),
        'mods': os.path.join(base_dir, "Game\\Mods"),
        'maps': os.path.join(base_dir, "Game\\Maps"),
    }

    return directories
	
def set_directory_address():
    directories = get_exe_location()
    new_dir = directories['game']  # get the game directory
    dst_dir.set(new_dir)  # update the destination directory
	

# UI states represented by indices
state_indices = [1, 2, 3, 4]
debug_state = [0, 1]
# Default to the first state
current_state = state_indices[0]
current_debug_state = debug_state[0]

# Tags that should always be visible
always_visible_tags = ["show_tag"]

# Define a dictionary where each state index maps to its related UI elements
# You will have to define these elements and their tags in your UI initialization
state_elements = {
    1: ["home_tag"],
    2: ["patch_tag"],
    3: ["map_tag"],
    4: ["mod_tag"]
}

debug_elements = {
    0: [],  # Normal state, no additional tags are visible
    1: ["debug_tag"]  # Debug state, debug_tag UI elements are visible
}

# Function to toggle debug state
def toggle_debug_state(event):
    global current_debug_state
    # If the current debug state is 0, change it to 1 and vice versa.
    current_debug_state = debug_state[(debug_state.index(current_debug_state) + 1) % len(debug_state)]
    update_debug_state()
    
# Function to update visibility of debug-tagged elements
def update_debug_state():
    # If current debug state is 1, show debug elements
    if current_debug_state == 1:
        for tag in debug_elements[current_debug_state]:
            canvas.itemconfig(tag, state="normal")
    # If current debug state is 0, hide debug elements
    else:
        for tag in debug_elements[debug_state[1]]:
            canvas.itemconfig(tag, state="hidden")

def next_state():
    global current_state
    current_state = state_indices[(state_indices.index(current_state) + 1) % len(state_indices)]
    update_state()

def previous_state():
    global current_state
    current_state = state_indices[(state_indices.index(current_state) - 1) % len(state_indices)]
    update_state()

def update_state():
    # Hide all UI elements
    for tag in canvas.find_all():
        if set(always_visible_tags).isdisjoint(set(canvas.gettags(tag))): 
            canvas.itemconfig(tag, state="hidden")

    # Show UI elements of the current state
    for tag in state_elements[current_state]:
        canvas.itemconfig(tag, state="normal")
		
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
		
def show_text():
    if not is_admin():
        canvas.itemconfig(message_label_admin, state="normal")
        root.after(1500, hide_text)  # Hide after x seconds

def hide_text():
    canvas.itemconfig(message_label_admin, state="hidden")
    root.after(1000, show_text)  # Show after x seconds		

def patch_directory(src_dir, dst_dir):
    directories = get_exe_location()
    src_dir = os.path.join(directories['base'], src_dir)

    if not os.path.exists(dst_dir):
        messagebox.showwarning("Warning", "Your directory doesn't exist")
        return

    # check for the existence of 'UAWEA.exe.cfg' in the destination directory
    if not os.path.isfile(os.path.join(dst_dir, 'UAWEA.exe.cfg')):
        messagebox.showwarning("Warning", "Your directory is incorrect")
        return
	
    root_files_to_delete = ['UAWEA.exe', 'UAWEA.exe.cat', 'UAWEA.exe.cfg', 'Patch_0.txt', 'Patch_1.txt', 'Patch_2.txt', 'Patch_3.txt',]
    data_files_to_delete = ['Config.meg', 'Maps.meg', 'MegaFiles.xml', 'Patch.meg', 'Retailers.meg']
    text_files_to_delete = ['CreditsText_CHINESE.DAT', 'CreditsText_CZECH.DAT', 'CreditsText_ENGLISH.DAT', 'CreditsText_FRENCH.DAT', 
                            'CreditsText_GERMAN.DAT', 'CreditsText_ITALIAN.DAT', 'CreditsText_JAPANESE.DAT', 'CreditsText_KOREAN.DAT', 
                            'CreditsText_POLISH.DAT', 'CreditsText_RUSSIAN.DAT', 'CreditsText_SPANISH.DAT', 'CreditsText_THAI.DAT', 
                            'CreditsText_UNITED_KINGDOM.DAT', 'MasterTextFile_CHINESE.DAT', 'MasterTextFile_CZECH.DAT', 'MasterTextFile_ENGLISH.DAT', 
                            'MasterTextFile_FRENCH.DAT', 'MasterTextFile_GERMAN.DAT', 'MasterTextFile_ITALIAN.DAT', 'MasterTextFile_JAPANESE.DAT', 
                            'MasterTextFile_KOREAN.DAT', 'MasterTextFile_POLISH.DAT', 'MasterTextFile_RUSSIAN.DAT', 'MasterTextFile_SPANISH.DAT', 
                            'MasterTextFile_THAI.DAT', 'MasterTextFile_UNITED_KINGDOM.DAT']
    audio_files_to_delete = ['Patch_SFX.meg']

    for file in root_files_to_delete:
        file_path = os.path.join(dst_dir, file)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    for file in data_files_to_delete:
        file_path = os.path.join(dst_dir, 'Data', file)
        if os.path.exists(file_path):
            os.remove(file_path)

    for file in text_files_to_delete:
        file_path = os.path.join(dst_dir, 'Data', 'Text', file)
        if os.path.exists(file_path):
            os.remove(file_path)

    for file in audio_files_to_delete:
        file_path = os.path.join(dst_dir, 'Data', 'Audio', 'SFX', file)
        if os.path.exists(file_path):
            os.remove(file_path)

    items = os.listdir(src_dir)
    for item in items:
        s = os.path.join(src_dir, item)
        d = os.path.join(dst_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    messagebox.showinfo("Patch Installed", f"Patch {src_dir[-1]} has successfully been installed")

    with open(os.path.join(dst_dir, f'Patch_{src_dir[-1]}.txt'), 'w') as f:
        f.write('This file indicates that the patch has been installed.')

    update_button_colors(dst_dir)
	
def save_last_dir(*args):
    directories = get_exe_location()  # Get all the directories
    base_dir = directories['base']  # Get the base directory
    file_path = os.path.join(base_dir, "Important Files", 'last_dir.txt')
    with open(file_path, 'w') as f:
        f.write(dst_dir.get())
    update_button_colors(dst_dir.get())

def reset_to_default():
    directories = get_exe_location()
    new_dir = directories['game']  # reset to the game directory
    dst_dir.set(new_dir)

def update_button_colors(directory):
    for i in range(4):
        if os.path.isfile(os.path.join(directory, f'Patch_{i}.txt')):
            buttons[i].config(bg='green')
        else:
            buttons[i].config(bg='red')


pygame.mixer.init()

base_path = os.path.dirname(os.path.realpath(__file__))
launch_sound = pygame.mixer.Sound(os.path.join(base_path, 'Assets', 'Launch.wav'))
hover_sound = pygame.mixer.Sound(os.path.join(base_path, 'Assets', 'Hover.wav'))
click_sound = pygame.mixer.Sound(os.path.join(base_path, 'Assets', 'Click.wav'))
press_sound = pygame.mixer.Sound(os.path.join(base_path, 'Assets', 'Press.wav'))

launch_sound.play()

root = tk.Tk()
root.title("Universe at War Community Launcher")

canvas = tk.Canvas(root, width=800, height=530)
canvas.pack()

root.minsize(100, 50)
root.maxsize(800, 530)

# Bind F4 key to toggle_debug_state
root.bind('<F4>', toggle_debug_state)

image_path = os.path.join(base_path, 'Assets', 'Backdrop.jpg')
bg_img = ImageTk.PhotoImage(Image.open(image_path))
canvas.background = bg_img
bg = canvas.create_image(0, 0, anchor=tk.NW, image=bg_img, tags=("show_tag"))

logo_path = os.path.join(base_path, 'Assets', 'Logo.png')
logo_image = Image.open(logo_path)
resized_logo_image = logo_image.resize((288, 80))

logo_photo = ImageTk.PhotoImage(resized_logo_image)
logo = canvas.create_image(506, 10, anchor=tk.NW, image=logo_photo, tags=("show_tag"))
canvas.logo_photo = logo_photo

src_dirs = ["Patch 0", "Patch 1", "Patch 2", "Patch 3"]
button_image_paths = [
    os.path.join(base_path, 'Assets', 'Button_0.png'),
    os.path.join(base_path, 'Assets', 'Button_1.png'),
    os.path.join(base_path, 'Assets', 'Button_2.png'),
    os.path.join(base_path, 'Assets', 'Button_3.png'),
]
button_hover_image_paths = [
    os.path.join(base_path, 'Assets', 'Button_0_Bright.png'),
    os.path.join(base_path, 'Assets', 'Button_1_Bright.png'),
    os.path.join(base_path, 'Assets', 'Button_2_Bright.png'),
    os.path.join(base_path, 'Assets', 'Button_3_Bright.png'),
]

button_photos = []
button_hover_photos = []
for path, hover_path in zip(button_image_paths, button_hover_image_paths):
    button_image = Image.open(path).resize((264, 50))
    button_photos.append(ImageTk.PhotoImage(button_image))

    button_hover_image = Image.open(hover_path).resize((264, 50))
    button_hover_photos.append(ImageTk.PhotoImage(button_hover_image))

buttons = []
for i, src_dir in enumerate(src_dirs, start=0):
    btn = tk.Button(root, text=f"Patch {i}", height=50, width=264, command=lambda src=src_dir: (click_sound.play(), patch_directory(src, dst_dir.get())), image=button_photos[i])
    btn.image = button_photos[i]  # Keep a reference to the image to prevent garbage collection
    btn.hover_image = button_hover_photos[i]  # Keep a reference to the hover image
    btn.bind("<Enter>", lambda event, btn=btn, i=i: (hover_sound.play(), btn.config(image=btn.hover_image)))
    btn.bind("<Leave>", lambda event, btn=btn: btn.config(image=btn.image))
    buttons.append(btn)
    canvas.create_window(400, 170+i*65, window=btn, tags=("patch_tag"), state="hidden")
default_dst_dir = "C:\\Program Files (x86)\\Sega\\Universe At War Earth Assault"

message_text = "Version 1.0 - 7/3/2023 - Created by PoppyMonster970"   
message_label = canvas.create_text(137, 10, text=message_text, font=("Arial", 8), fill="red", tags=("show_tag"))  

message_text2 = "Make sure that this is the correct address to your game's files." \
               " If it's not, type in the correct one."
message_label2 = canvas.create_text(400, 485, text=message_text2, font=("Arial", 11, "bold"), fill="red", tags=("debug_tag"), state="hidden")  

entry_frame = tk.Frame(root)
canvas.create_window(400, 515, window=entry_frame, tags=("debug_tag"), state="hidden")

entry_label = Label(entry_frame, text="Game Directory =", font=("Arial", 12))
entry_label.pack(side=tk.LEFT)

dst_dir = StringVar(root)
dst_dir.trace("w", save_last_dir)

try:
    directories = get_exe_location()  # Get all the directories
    base_dir = directories['base']  # Get the base directory
    file_path = os.path.join(base_dir, "Important Files", 'last_dir.txt')
    with open(file_path, 'r') as f:
        last_dir = f.read()
        dst_dir.set(last_dir)
except FileNotFoundError:
    dst_dir.set(default_dst_dir)


entry = Entry(entry_frame, textvariable=dst_dir, font=("Arial", 12), width=50)
entry.pack(side=tk.LEFT)

reset_button = tk.Button(entry_frame, text="Reset", command=reset_to_default)
reset_button.pack(side=tk.LEFT)

update_button_colors(dst_dir.get())

# Check for admin privileges and display the message if not run as admin
if not is_admin():
    message_text_admin = "PLEASE RELAUNCH THE APPLACATON IN ADMINISTRATOR MODE"
    message_label_admin = canvas.create_text(400, 115, text=message_text_admin, font=("Arial", 15, "bold"), fill="red", state="hidden")
    show_text()
	
previous_button = tk.Button(root, text="Previous", command=previous_state)
canvas.create_window(10, 250, window=previous_button, tags=("show_tag"))
previous_button.bind("<Enter>", lambda event: hover_sound.play())
previous_button.bind("<Button-1>", lambda event: press_sound.play())

next_button = tk.Button(root, text="Next", command=next_state)
canvas.create_window(790, 250, window=next_button, tags=("show_tag"))
next_button.bind("<Enter>", lambda event: hover_sound.play())
next_button.bind("<Button-1>", lambda event: press_sound.play())

#####################################################################
                              #HOME#
#####################################################################


# We can reuse the destination directory Entry widget from above
entry_destination = entry

def play_button_action():
    directories = get_exe_location()  # Get all the directories
    base_dir = directories['base']  # Get the base directory
    dst_dir = os.path.join(base_dir, "Important Files")  # Path to the "Important Files" folder
    launch_exe_path = os.path.join(dst_dir, "launch.bat")  # Path to the batch file
    print(f"Attempting to run: {launch_exe_path}")  # Print out the path
    if os.path.exists(launch_exe_path):
        try:
            subprocess.Popen(launch_exe_path, shell=True)
        except Exception as e:
            print(f"Exception occurred: {e}")  # Print out the exception
    else:
        messagebox.showwarning("Warning", "launch.bat not found in Important Files directory")


def discord_button_action():
    webbrowser.open("https://discord.gg/ZVae7mdH")

def help_button_action():
    help_pdf_path = Path(base_path) / "Assets" / "Help.pdf"
    if help_pdf_path.exists():
        os.startfile(help_pdf_path)
    else:
        print("Help.pdf not found in Assets directory")

def editor_button_action():
    dst_dir = entry.get()  # Assuming 'entry' is the Entry widget for destination
    editor_exe_path = os.path.join(dst_dir, "UAWEditor.exe")
    if os.path.exists(editor_exe_path):
        subprocess.run(editor_exe_path, shell=True)
    else:
        messagebox.showwarning("Warning", "UAWEditor.exe not found in destination directory")
		
		
		
def copy_with_progress(src, dst, progress_var):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(src):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    copied_size = 0
    progress_var.set(0)

    for dirpath, dirnames, filenames in os.walk(src):
        dst_dir = os.path.join(dst, os.path.relpath(dirpath, src))
        os.makedirs(dst_dir, exist_ok=True)

        for name in filenames:
            src_file = os.path.join(dirpath, name)
            dst_file = os.path.join(dst_dir, name)
            shutil.copy2(src_file, dst_file)

            copied_size += os.path.getsize(src_file)
            progress_var.set(copied_size / total_size * 100)

    progress_var.set(100)
	




def save_install_dir(target_folder):
    game_folder = "Universe At War Earth Assault"
    text_files_folder = "Text Files"
    home_path = os.path.expanduser('~')
    save_dir = os.path.join(home_path, game_folder, text_files_folder)
    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, 'install_dir.txt')
    with open(file_path, 'w') as f:
        f.write(target_folder)

def install_button_action():
    install_window = tk.Toplevel(root)
    install_window.title("Install - Universe at War: Earth Assault")

    # Set installation window as a top-level window and ensure it stays on top
    install_window.attributes("-topmost", True)
    install_window.wm_attributes("-topmost", True)

    # Make the window non-resizable and remove maximize button
    install_window.resizable(False, False)
    install_window.geometry("400x150")

    # Load the background image
    install_image_path = os.path.join(base_path, "Assets", "Install_Backdrop.png")
    install_bg_img = Image.open(install_image_path)
    install_bg_photo = ImageTk.PhotoImage(install_bg_img)

    # Create a canvas and set the background image
    install_canvas = tk.Canvas(install_window, width=400, height=150)
    install_canvas.pack()
    install_canvas.create_image(0, 0, anchor=tk.NW, image=install_bg_photo, tags="bg_image")

    # Keep a reference to the image to prevent garbage collection
    install_canvas.bg_image = install_bg_photo

    # Directory entry
    directory_var = tk.StringVar(install_window, value="C:\\Program Files (x86)")
    directory_entry = tk.Entry(install_window, textvariable=directory_var, width=50)
    directory_entry.place(x=20, y=20)

    def choose_folder():
        folder_selected = filedialog.askdirectory()
        directory_var.set(folder_selected)

    choose_folder_button = tk.Button(install_window, text="Choose Folder", command=choose_folder, font=("Arial", 7))
    choose_folder_button.place(x=310, y=19.5)

    def install_game():
        destination_folder = directory_var.get()

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        sega_folder = os.path.join(destination_folder, "Sega")

        if not os.path.exists(sega_folder):
            os.makedirs(sega_folder)

        source_folder = os.path.join(base_path, 'Exports', 'Universe At War Earth Assault')
        target_folder = os.path.join(sega_folder, "Universe At War Earth Assault")

        progress_var = tk.DoubleVar()  # Create progress_var here

        progress_bar = ttk.Progressbar(install_canvas, length=300, mode='determinate', variable=progress_var)
        progress_bar.place(x=50, y=60)

        thread = threading.Thread(target=copy_with_progress, args=(source_folder, target_folder, progress_var))
        thread.start()
	
        while thread.is_alive():
            install_window.update()
            progress_bar['value'] = progress_var.get()

        messagebox.showinfo("Info", "Installation completed")
        directory_var.set(target_folder)
        save_install_dir(target_folder) # save directory after successful installation

    # Load the Install button image
    install_button_image_path = os.path.join(base_path, "Assets", "Install.png")
    install_button_image = Image.open(install_button_image_path)
    # Resize the image to match the button size
    install_button_image_resized = install_button_image.resize((140, 30))  # Assuming the button size is 90x30
    install_button_photo = ImageTk.PhotoImage(install_button_image_resized)

    # Create the Install button with the image
    install_button = tk.Button(install_window, image=install_button_photo, command=install_game, bg="#97751e")
    install_button.image = install_button_photo  # Keep a reference to prevent GC
    install_button.place(x=130, y=105) 






def live_sign_in_button_action():
    window = tk.Toplevel(root)

    data = [
    ("90,c8,9a,8a,f6,57,a9,f7", "FXRHK-T8PDY-FHBCH-G6YJG-XF8PJ"),
    ("23,b3,bd,92,12,6b,c5,fc", "WBV4B-MFGR4-Y9XY7-MKRPM-HHJ96"),
    ("f3,42,a3,bb,c2,43,96,3c", "M2RHB-TDC2R-MTHXH-GP662-XG33W"),
    ("ec,9f,31,39,87,50,96,62", "WMBGX-HC2WR-JC92D-KVK2B-Q8YB3"),
    ("92,1e,37,df,f4,52,dd,01", "W6Y9P-MKP4C-FHT83-GQMMC-FYQQQ"),
    ("53,48,b4,94,11,01,d5,98", "JX3JC-CC2HX-TRWCY-49BKF-2CKYY"),
    ("eb,5f,76,a9,5d,87,d9,8d", "XH3CX-7D382-4TWG7-D9YT9-FFJMJ"),
    ("ec,78,57,e2,44,57,f2,91", "V7HM9-K3YBQ-K3XVF-4K6JF-RXXHG"),
    ("2b,2c,e1,af,16,ea,97,42", "DCKXY-JG4DH-JRDYB-KMT97-GPKPG"),
    ("d8,bf,b3,fd,49,11,9f,a7", "QGTD9-VM883-83FPP-KYKD2-FK3JD"),
    ("39,49,34,34,30,c0,7b,97", "MVKG6-8BPRK-93FPR-GTH9Y-GQJWT"),
    ("94,52,8c,e7,c8,e0,bc,80", "P72WF-GXDQM-8YTP4-7TYYB-72YGT"),
    ("1c,53,6d,92,2d,ef,26,76", "JY6GC-GD69H-G4TC2-BF9MJ-FW9YJ"),
    ("91,26,c1,de,83,b8,f8,f5", "Q38PK-B9WCR-8D8WP-C8Y28-9DW73"),
    ("f7,b0,2f,e2,18,ed,05,e8", "GXTHG-JCQMJ-WVBCP-MDVPV-JBX43"),
    ("7e,1a,c9,0c,6d,aa,4f,b1", "RHQV3-7G3FM-9T4CD-F9H8B-FT66Q"),
    ("ab,49,55,39,77,46,1d,90", "CMBMJ-CG3PC-R2HY8-6RYGG-CRWTY"),
    ("d9,bd,df,b7,aa,f9,b3,fd", "CPTJV-PYQRR-VY79Y-7PMM6-DWBF3"),
    ("40,f1,a1,5e,11,39,83,f2", "22TBG-D3PF4-YPMDJ-MMJ8Q-9Y68G"),
    ("ad,28,cc,13,2c,e2,b3,61", "CTJG4-V3MQY-3K272-6MHCV-R4GG6"),
    ("e3,c3,e6,3d,94,87,26,2e", "V3K6V-QTKQD-RDWCJ-X3WM2-G8XP8"),
    ("f8,37,19,46,ce,45,44,45", "DPQ7P-646DC-DM63Q-X4YD3-MPBMB"),
    ("24,59,1c,b5,37,2e,65,fe", "CHYXY-QYRXP-WR22C-8B47X-DGF93"),
    ("71,40,3a,3b,ad,26,98,5d", "RRQ6J-B2G7T-GMW8M-Q7QYX-3VJVQ"),
    ("d0,9e,87,b9,41,95,85,f5", "FYGQP-F7GQP-X6CX6-BFYVK-WQBBG"),
    ("86,0c,7e,9b,a5,08,5a,31", "HJKY7-6TQD6-6FPXT-DG9J3-K7YQD"),
    ("df,fa,68,3e,ed,ab,07,3b", "VY43Y-JYC9Q-84T4P-M22G8-WVBR6"),
    ("b6,37,7a,64,a9,f7,36,a3", "BYMGW-K33C2-WDDDD-VQ98P-DJC4M"),
    ("8c,b1,87,93,cd,fa,91,85", "G8FFP-FRBT6-DCKT9-HRMMX-XCMBJ"),
    ("84,a4,aa,7e,36,8a,45,b3", "DW9FC-B2DFG-TQB9Y-P3YKC-V8P7Y"),
    ("f6,01,85,6f,40,1e,26,61", "VDQBM-TYB29-QTRG6-WY7VB-YRD7J"),
    ("8a,c8,1d,58,52,bb,e6,88", "W8D7H-F2RBK-PRHCG-PRTQW-CHPDB")
    # Add the rest of the PC IDs and keys here
    ]

    def generate_key():
        pcid, key = random.choice(data)

        pcid_label['text'] = f"PCID: {pcid}"
        key_label['text'] = f"Key: {key}"

        # Modify the registry key
        registry_modification = f"""Windows Registry Editor Version 5.00

    [HKEY_CURRENT_USER\Software\Classes\SOFTWARE\Microsoft\XLive]
    "PCID"=hex(b):{pcid}"""

        with open('reg.reg', 'w') as file:
            file.write(registry_modification)

        subprocess.call(['reg', 'import', 'reg.reg'])

        os.remove('reg.reg')

    window.title("PC ID and Key Generator")

    pcid_label = tk.Label(window, text="PCID: Not Generated")
    key_label = tk.Label(window, text="Key: Not Generated")
    generate_button = tk.Button(window, text="Generate PC ID and Key", command=generate_key)

    pcid_label.pack()
    key_label.pack()
    generate_button.pack()


def uninstall_button_action():
    confirmation = messagebox.askquestion("Uninstall", "Are you sure you wish to uninstall the game?")
    if confirmation == "yes":
        for directory in directories:
            if all(os.path.exists(os.path.join(directory, file)) for file in file_names):
                shutil.rmtree(directory)
                messagebox.showinfo("Uninstall", "Game successfully uninstalled.")
                break
    else:
        pass

# Load button images
button_image_paths = [
    os.path.join(base_path, 'Assets', 'Home_1.png'),  # Play button image
    os.path.join(base_path, 'Assets', 'Home_2.png'),  # Discord button image
    os.path.join(base_path, 'Assets', 'Home_3.png'),  # Help button image
    os.path.join(base_path, 'Assets', 'Home_4.png'),  # Editor button image
    os.path.join(base_path, 'Assets', 'Home_5.png'),  # Install button image
    os.path.join(base_path, 'Assets', 'Home_6.png'),  # Live Sign-In button image
    os.path.join(base_path, 'Assets', 'Home_7.png'),   # Uninstall button image
	os.path.join(base_path, 'Assets', 'Home_1_Bright.png'),  # Play button image
    os.path.join(base_path, 'Assets', 'Home_2_Bright.png'),  # Discord button image
    os.path.join(base_path, 'Assets', 'Home_3_Bright.png'),  # Help button image
    os.path.join(base_path, 'Assets', 'Home_4_Bright.png'),  # Editor button image
    os.path.join(base_path, 'Assets', 'Home_5_Bright.png'),  # Install button image
    os.path.join(base_path, 'Assets', 'Home_6_Bright.png'),  # Live Sign-In button image
    os.path.join(base_path, 'Assets', 'Home_7_Bright.png')   # Uninstall button image
]

button_photos = []
button_hover_photos = []
for i, path in enumerate(button_image_paths):
    button_image = Image.open(path)
    resized_button_image = button_image.resize((264, 50))
    if i < 7:  # For the first seven images
        button_photos.append(ImageTk.PhotoImage(resized_button_image))
    else:  # For the rest of the images
        button_hover_photos.append(ImageTk.PhotoImage(resized_button_image))
canvas.button_photos = button_photos
canvas.button_hover_photos = button_hover_photos  # Keep a reference to the hover images too

# Create the buttons with images
play_button = tk.Button(root, command=play_button_action, image=button_photos[0], compound="center", width=264, height=50, bg="#97751e")
discord_button = tk.Button(root, command=discord_button_action, image=button_photos[1], compound="center", width=264, height=50, bg="#97751e")
help_button = tk.Button(root, command=help_button_action, image=button_photos[2], compound="center", width=264, height=50, bg="#97751e")
editor_button = tk.Button(root, command=editor_button_action, image=button_photos[3], compound="center", width=264, height=50, bg="#97751e")
install_button = tk.Button(root, command=install_button_action, image=button_photos[4], compound="center", width=264, height=50, bg="#97751e")
live_sign_in_button = tk.Button(root, command=live_sign_in_button_action, image=button_photos[5], compound="center", width=264, height=50, bg="#97751e")
uninstall_button = tk.Button(root, command=uninstall_button_action, image=button_photos[6], compound="center", width=264, height=50, bg="#97751e")

# Keep a reference to the images to prevent them from being garbage collected
canvas.button_photos = button_photos

# Add the buttons to the canvas at the same positions as the Patch buttons
canvas.create_window(259, 202, window=play_button, tags=("home_tag", "play_tag"), state="hidden")
canvas.create_window(259, 267, window=editor_button, tags=("home_tag", "editor_tag"), state="hidden")
canvas.create_window(259, 332, window=live_sign_in_button, tags=("home_tag", "live_sign_in_tag"), state="hidden")
canvas.create_window(541, 202, window=discord_button, tags=("home_tag", "discord_tag"), state="hidden")
canvas.create_window(541, 267, window=help_button, tags=("home_tag", "help_tag"), state="hidden")
canvas.create_window(541, 332, window=install_button, tags=("home_tag", "install_tag"), state="hidden")


"""
if check_files_exist():
    canvas.create_window(535, 332, window=uninstall_button, tags=("home_tag", "uninstall_tag"), state="hidden")
else:
    canvas.create_window(2000, 332, window=uninstall_button, tags=("home_tag", "uninstall_tag"), state="hidden")
"""

def check_directory_exists():
    directories = get_exe_location()
    game_dir = directories['game']  # The directory to check

    if os.path.exists(game_dir):
        # If the directory exists, create the window at the specified location
        canvas.create_window(535, 332, window=uninstall_button, tags=("home_tag", "uninstall_tag"), state="hidden")
    else:
        # If the directory does not exist, create the window at a different location
        canvas.create_window(600, 332, window=uninstall_button, tags=("home_tag", "uninstall_tag"), state="hidden")
   
check_directory_exists()

play_button.bind("<Enter>", lambda event: (hover_sound.play(), play_button.config(image=canvas.button_hover_photos[0])))
play_button.bind("<Leave>", lambda event: play_button.config(image=canvas.button_photos[0]))
play_button.bind("<Button-1>", lambda event: click_sound.play())

discord_button.bind("<Enter>", lambda event: (hover_sound.play(), discord_button.config(image=canvas.button_hover_photos[1])))
discord_button.bind("<Leave>", lambda event: discord_button.config(image=canvas.button_photos[1]))
discord_button.bind("<Button-1>", lambda event: click_sound.play())

help_button.bind("<Enter>", lambda event: (hover_sound.play(), help_button.config(image=canvas.button_hover_photos[2])))
help_button.bind("<Leave>", lambda event: help_button.config(image=canvas.button_photos[2]))
help_button.bind("<Button-1>", lambda event: click_sound.play())

editor_button.bind("<Enter>", lambda event: (hover_sound.play(), editor_button.config(image=canvas.button_hover_photos[3])))
editor_button.bind("<Leave>", lambda event: editor_button.config(image=canvas.button_photos[3]))
editor_button.bind("<Button-1>", lambda event: click_sound.play())

install_button.bind("<Enter>", lambda event: (hover_sound.play(), install_button.config(image=canvas.button_hover_photos[4])))
install_button.bind("<Leave>", lambda event: install_button.config(image=canvas.button_photos[4]))
install_button.bind("<Button-1>", lambda event: click_sound.play())

live_sign_in_button.bind("<Enter>", lambda event: (hover_sound.play(), live_sign_in_button.config(image=canvas.button_hover_photos[5])))
live_sign_in_button.bind("<Leave>", lambda event: live_sign_in_button.config(image=canvas.button_photos[5]))
live_sign_in_button.bind("<Button-1>", lambda event: click_sound.play())

uninstall_button.bind("<Enter>", lambda event: (hover_sound.play(), uninstall_button.config(image=canvas.button_hover_photos[6])))
uninstall_button.bind("<Leave>", lambda event: uninstall_button.config(image=canvas.button_photos[6]))
uninstall_button.bind("<Button-1>", lambda event: click_sound.play())


#####################################################################
                      #DESKTOP SHORTCUT WINDOW#
#####################################################################

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def create_shortcut(path, target='', wDir='', icon=''):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    if icon == '':
        pass
    else:
        shortcut.IconLocation = icon
    shortcut.save()

def ask_create_shortcut():
    base_dir = get_exe_location()['base']
    # Get the directory of the Important Files
    important_files_dir = os.path.join(base_dir, "Important Files")
    
    # Get the path of the last_dir.txt and old_dir.txt
    last_dir_path = os.path.join(important_files_dir, "last_dir.txt")
    old_dir_path = os.path.join(important_files_dir, "old_dir.txt")
    
    # Read the content of last_dir.txt and old_dir.txt
    last_dir = read_file(last_dir_path)
    old_dir = read_file(old_dir_path)
    
    if last_dir != old_dir:
        # If last_dir and old_dir are different, ask to create a shortcut
        answer = messagebox.askyesno("Create Shortcut", 
                                     "Would you like to create a Desktop shortcut for your launcher?")
        if answer:  # if user clicked 'yes'
            desktop = winshell.desktop()
            path = os.path.join(desktop, "UAW Launcher.lnk")
            target = os.path.join(base_dir, "UAW Launcher.exe")  # Get the absolute path of the executable
            wDir = base_dir  # Set the working directory to base_dir
            icon = os.path.join(important_files_dir, "X_X.ico")  # Path to the custom icon file
            create_shortcut(path, target, wDir, icon)
        
        # Update the content of old_dir.txt with the content of last_dir.txt, regardless of the user's answer
        write_file(old_dir_path, last_dir)



set_directory_address()
update_state()

if __name__ == "__main__":
    root.after(500, ask_create_shortcut)
    root.mainloop()