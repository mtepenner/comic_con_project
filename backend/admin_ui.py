# admin_ui.py
import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os
import time
from managers import BankManager
from config import *

# ==========================================
# Administrator Portal UI
# ==========================================
class AdminUI:
    def __init__(self, root, first_name):
        self.root = root
        self.root.geometry("950x650")
        self.root.configure(bg=BG_COLOR) 

        try:
            self.cpp_process = subprocess.Popen(
                [CPP_EXECUTABLE], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, text=True, bufsize=1
            )
        except FileNotFoundError:
            messagebox.showerror("FATAL ERROR", f"ERR_FILE_NOT_FOUND: {CPP_EXECUTABLE}")
            self.root.destroy()
            return

        tk.Label(self.root, text=f"LOGGED IN AS: ROOT//{first_name}", font=FONT_MAIN, bg=BG_COLOR, fg=FG_MAGENTA).pack(anchor="nw", padx=10, pady=5)
        tk.Label(self.root, text=">_ COMIC-CON MAINFRAME", font=FONT_TITLE, bg=BG_COLOR, fg=FG_GREEN).pack(fill=tk.X, pady=5, padx=10)

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        btn_style = {"font": FONT_MAIN, "bg": BTN_BG, "activebackground": FG_GREEN, "activeforeground": BG_COLOR, "width": 22, "pady": 10, "bd": 1, "relief": "solid"}
        tk.Button(btn_frame, text="[+] INJECT ARTIST", fg=FG_CYAN, command=self.add_artist, **btn_style).pack(pady=10)
        tk.Button(btn_frame, text="[+] INJECT ACTOR", fg=FG_CYAN, command=self.add_actor, **btn_style).pack(pady=10)
        tk.Button(btn_frame, text="[+] INJECT COSPLAYER", fg=FG_CYAN, command=self.add_cosplayer, **btn_style).pack(pady=10)
        
        tk.Button(btn_frame, text="[$] CONFIGURE LEDGER", fg=FG_GREEN, command=self.manage_bank, **btn_style).pack(pady=20)
        
        tk.Button(btn_frame, text="[x] TERMINATE SESSION", fg=FG_MAGENTA, command=self.on_closing, **btn_style).pack(side=tk.BOTTOM, pady=15)

        self.text_display = tk.Text(main_frame, font=("Consolas", 12), bg="#000000", fg=FG_GREEN, insertbackground=FG_GREEN, borderwidth=1, relief="solid", wrap=tk.WORD)
        self.text_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.refresh_display()

    def send_to_backend(self, command_string):
        if self.cpp_process.poll() is None:
            self.cpp_process.stdin.write(command_string)
            self.cpp_process.stdin.flush()
            self.cpp_process.stdin.write("4\n")
            self.cpp_process.stdin.flush()
            time.sleep(0.1) 
            self.refresh_display()

    def add_artist(self):
        name = simpledialog.askstring("INPUT", "PARAM_NAME:", parent=self.root)
        if not name: return
        style = simpledialog.askstring("INPUT", "PARAM_STYLE:", parent=self.root)
        booth = simpledialog.askinteger("INPUT", "PARAM_BOOTH_INT:", parent=self.root)
        if style and booth: self.send_to_backend(f"1\n{name}\n{style}\n{booth}\n")

    def add_actor(self):
        name = simpledialog.askstring("INPUT", "PARAM_NAME:", parent=self.root)
        if not name: return
        role = simpledialog.askstring("INPUT", "PARAM_ROLE:", parent=self.root)
        if role: self.send_to_backend(f"2\n{name}\n{role}\n")

    def add_cosplayer(self):
        name = simpledialog.askstring("INPUT", "PARAM_NAME:", parent=self.root)
        if not name: return
        character = simpledialog.askstring("INPUT", "PARAM_CHARACTER:", parent=self.root)
        if character: self.send_to_backend(f"3\n{name}\n{character}\n")

    def manage_bank(self):
        bank_win = tk.Toplevel(self.root)
        bank_win.title("SYSTEM // LEDGER_CONFIG")
        bank_win.geometry("400x420")
        bank_win.configure(bg=BG_COLOR)

        tk.Label(bank_win, text=">_ FINANCIAL_ROUTING", font=FONT_HEADER, bg=BG_COLOR, fg=FG_GREEN).pack(pady=15)

        current_bank = BankManager.get_bank_info()
        status_text = f"TARGET_NODE: {current_bank['bank_name']}" if current_bank else "ERR: UNLINKED"
        tk.Label(bank_win, text=status_text, bg=BG_COLOR, fg=FG_MAGENTA, font=FONT_MAIN).pack(pady=5)

        tk.Label(bank_win, text="INSTITUTION_ID:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack(anchor="w", padx=40)
        entry_bank = tk.Entry(bank_win, font=FONT_MAIN, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        entry_bank.pack(fill=tk.X, padx=40, pady=5)
        if current_bank: entry_bank.insert(0, current_bank["bank_name"])

        tk.Label(bank_win, text="ACCOUNT_HASH:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack(anchor="w", padx=40)
        entry_acc = tk.Entry(bank_win, font=FONT_MAIN, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        entry_acc.pack(fill=tk.X, padx=40, pady=5)
        if current_bank: entry_acc.insert(0, current_bank["account_number"])

        tk.Label(bank_win, text="ROUTING_VECTOR:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack(anchor="w", padx=40)
        entry_rout = tk.Entry(bank_win, font=FONT_MAIN, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        entry_rout.pack(fill=tk.X, padx=40, pady=5)
        if current_bank: entry_rout.insert(0, current_bank["routing_number"])

        def save_bank():
            bn, an, rn = entry_bank.get(), entry_acc.get(), entry_rout.get()
            if bn and an and rn:
                BankManager.save_bank_info(bn, an, rn)
                messagebox.showinfo("SYS_MSG", "ROUTING_TABLE_UPDATED", parent=bank_win)
                bank_win.destroy()
            else:
                messagebox.showerror("SYS_ERR", "ERR: NULL_PARAMETERS", parent=bank_win)

        def remove_bank():
            if messagebox.askyesno("WARN", "PURGE FINANCIAL ROUTING?", parent=bank_win):
                BankManager.remove_bank_info()
                messagebox.showinfo("SYS_MSG", "LEDGER PURGED", parent=bank_win)
                bank_win.destroy()

        btn_style = {"font": FONT_MAIN, "bg": BTN_BG, "bd": 1, "relief": "solid"}
        tk.Button(bank_win, text="[ COMMIT CHANGES ]", fg=FG_CYAN, command=save_bank, **btn_style).pack(fill=tk.X, padx=40, pady=10)
        tk.Button(bank_win, text="[ PURGE NODE ]", fg=FG_MAGENTA, command=remove_bank, **btn_style).pack(fill=tk.X, padx=40, pady=5)

    def refresh_display(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                content = file.read()
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, ">>> FETCHING DATABANKS...\n" + content)
            self.text_display.config(state=tk.DISABLED)

    def on_closing(self):
        if hasattr(self, 'cpp_process') and self.cpp_process.poll() is None:
            self.cpp_process.stdin.write("5\n") 
            self.cpp_process.stdin.flush()
            self.cpp_process.wait()
        self.root.destroy()
