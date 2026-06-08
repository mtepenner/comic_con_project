# auth_ui.py
import tkinter as tk
from tkinter import messagebox
from managers import AuthManager
from config import *

# ==========================================
# Authentication UI
# ==========================================
class AuthUI:
    def __init__(self, root, on_success_callback):
        self.root = root
        self.on_success = on_success_callback
        
        self.auth_win = tk.Toplevel(self.root)
        self.auth_win.title("SYSTEM // AUTHENTICATION")
        self.auth_win.geometry("380x520")
        self.auth_win.configure(bg=BG_COLOR)
        self.auth_win.protocol("WM_DELETE_WINDOW", self.on_close)

        tk.Label(self.auth_win, text="> AUTH_PROTOCOL", font=FONT_HEADER, bg=BG_COLOR, fg=FG_CYAN).pack(pady=20)

        tk.Label(self.auth_win, text="SYS_USER:", bg=BG_COLOR, fg=FG_GREEN, font=FONT_MAIN).pack(anchor="w", padx=40)
        self.entry_user = tk.Entry(self.auth_win, font=FONT_MAIN, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        self.entry_user.pack(fill=tk.X, padx=40, pady=5)

        tk.Label(self.auth_win, text="PASS_KEY:", bg=BG_COLOR, fg=FG_GREEN, font=FONT_MAIN).pack(anchor="w", padx=40)
        self.entry_pass = tk.Entry(self.auth_win, show="*", font=FONT_MAIN, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        self.entry_pass.pack(fill=tk.X, padx=40, pady=5)

        btn_style = {"font": FONT_MAIN, "bg": BTN_BG, "activebackground": FG_GREEN, "activeforeground": BG_COLOR, "pady": 5, "bd": 1, "relief": "solid"}

        tk.Button(self.auth_win, text="[ EXECUTE LOGIN ]", fg=FG_GREEN, command=self.do_login, **btn_style).pack(fill=tk.X, padx=40, pady=15)
        tk.Button(self.auth_win, text="[ ALLOCATE ACCOUNT ]", fg=FG_CYAN, command=self.show_create_account, **btn_style).pack(fill=tk.X, padx=40, pady=5)
        tk.Button(self.auth_win, text="[ BYPASS AS GUEST ]", fg=FG_MAGENTA, command=self.do_guest, **btn_style).pack(fill=tk.X, padx=40, pady=15)

    def do_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()
        success, first_name, role = AuthManager.verify_login(user, pwd)
        
        if success:
            self.auth_win.destroy()
            self.on_success(first_name, role)
        else:
            messagebox.showerror("ACCESS DENIED", "ERR: INVALID_CREDENTIALS", parent=self.auth_win)

    def do_guest(self):
        self.auth_win.destroy()
        self.on_success("ANON_GUEST", "Guest")

    def show_create_account(self):
        reg_win = tk.Toplevel(self.auth_win)
        reg_win.title("SYSTEM // REGISTRY")
        reg_win.geometry("320x380")
        reg_win.configure(bg=BG_COLOR)
        
        tk.Label(reg_win, text="IDENTIFIER:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack(pady=(10, 0))
        entry_first = tk.Entry(reg_win, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        entry_first.pack(pady=5)

        tk.Label(reg_win, text="SYS_USER:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack()
        entry_user = tk.Entry(reg_win, bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        entry_user.pack(pady=5)

        tk.Label(reg_win, text="PASS_KEY:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack()
        entry_pass = tk.Entry(reg_win, show="*", bg=BTN_BG, fg=FG_GREEN, insertbackground=FG_GREEN)
        entry_pass.pack(pady=5)

        tk.Label(reg_win, text="PRIVILEGE_LEVEL:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack()
        role_var = tk.StringVar(value="Guest")
        tk.Radiobutton(reg_win, text="USER", variable=role_var, value="Guest", bg=BG_COLOR, fg=FG_GREEN, selectcolor=BG_COLOR, activebackground=BG_COLOR, activeforeground=FG_GREEN).pack()
        tk.Radiobutton(reg_win, text="ROOT", variable=role_var, value="Admin", bg=BG_COLOR, fg=FG_MAGENTA, selectcolor=BG_COLOR, activebackground=BG_COLOR, activeforeground=FG_MAGENTA).pack()

        def submit():
            success, msg = AuthManager.create_account(entry_first.get(), entry_user.get(), entry_pass.get(), role_var.get())
            if success:
                messagebox.showinfo("SYS_MSG", msg, parent=reg_win)
                reg_win.destroy()
            else:
                messagebox.showerror("SYS_ERR", msg, parent=reg_win)

        tk.Button(reg_win, text="[ COMMIT TO REGISTRY ]", command=submit, bg=BTN_BG, fg=FG_CYAN, bd=1, relief="solid").pack(pady=15)

    def on_close(self):
        self.root.destroy()
