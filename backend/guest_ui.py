# guest_ui.py
import tkinter as tk
from tkinter import messagebox
import os
from managers import BankManager
from config import *

# ==========================================
# Guest Portal & Billing UI
# ==========================================
class GuestUI:
    def __init__(self, root, first_name):
        self.root = root
        self.root.geometry("900x600")
        self.root.configure(bg=BG_COLOR) 

        tk.Label(self.root, text=f"SYS_USER: {first_name}", font=FONT_MAIN, bg=BG_COLOR, fg=FG_CYAN).pack(anchor="nw", padx=10, pady=5)
        tk.Label(self.root, text=">_ ITINERARY BUILDER", font=FONT_TITLE, bg=BG_COLOR, fg=FG_GREEN).pack(fill=tk.X, pady=5, padx=10)

        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(main_frame, text=">>> SELECT TARGET ENTITIES (CTRL+CLICK FOR MULTI_TARGET):", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack(anchor="w")
        self.listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, font=("Consolas", 12), bg="#000000", fg=FG_GREEN, selectbackground=FG_MAGENTA, selectforeground="#000000", width=80, height=15, bd=1, relief="solid")
        self.listbox.pack(pady=10)
        
        self.load_events()

        btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
        btn_frame.pack(fill=tk.X, pady=10)

        btn_style = {"font": FONT_MAIN, "bg": BTN_BG, "width": 20, "pady": 5, "bd": 1, "relief": "solid"}
        tk.Button(btn_frame, text="[ EXECUTE TRANSACTION ]", fg=FG_CYAN, command=self.checkout, **btn_style).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="[ ABORT ]", fg=FG_MAGENTA, command=self.root.destroy, **btn_style).pack(side=tk.RIGHT, padx=20)

    def load_events(self):
        if not os.path.exists(DATA_FILE):
            self.listbox.insert(tk.END, "ERR: DATABANK_EMPTY. AWAITING SYSADMIN INPUT.")
            self.listbox.config(state=tk.DISABLED)
            return
            
        with open(DATA_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() and "===" not in line:
                    self.listbox.insert(tk.END, f"> {line.strip()}")

    def checkout(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("SYS_WARN", "ERR: NO_TARGETS_SELECTED")
            return

        bank_info = BankManager.get_bank_info()
        if not bank_info:
            messagebox.showerror("SYS_ERR", "CRITICAL: NO_ROUTING_NODE_FOUND. CONTACT SYSADMIN.")
            return

        total_cost = len(selected_indices) * PRICE_PER_EVENT

        bill_win = tk.Toplevel(self.root)
        bill_win.title("SYSTEM // SECURE_CHECKOUT")
        bill_win.geometry("400x400")
        bill_win.configure(bg=BG_COLOR)

        tk.Label(bill_win, text=">_ INVOICE GENERATED", font=FONT_HEADER, bg=BG_COLOR, fg=FG_CYAN).pack(pady=10)
        tk.Label(bill_win, text=f"TARGET_COUNT: {len(selected_indices)}", bg=BG_COLOR, fg=FG_GREEN, font=FONT_MAIN).pack(pady=5)
        tk.Label(bill_win, text=f"CREDITS_REQUIRED: {total_cost:.2f} cR", bg=BG_COLOR, fg=FG_MAGENTA, font=("Courier", 16, "bold")).pack(pady=10)

        tk.Label(bill_win, text=f"NODE_LINK: {bank_info['bank_name']}", bg=BG_COLOR, fg="#555555", font=("Courier", 10)).pack(pady=5)

        tk.Label(bill_win, text="SELECT TRANSFER PROTOCOL:", bg=BG_COLOR, fg=FG_CYAN, font=FONT_MAIN).pack(pady=10)
        pay_var = tk.StringVar(value="SECURE_NET")
        tk.Radiobutton(bill_win, text="SECURE_NET (CREDIT)", variable=pay_var, value="CREDIT", bg=BG_COLOR, fg=FG_GREEN, selectcolor=BG_COLOR, activebackground=BG_COLOR, activeforeground=FG_GREEN).pack()
        tk.Radiobutton(bill_win, text="CRYPTO_LEDGER", variable=pay_var, value="CRYPTO", bg=BG_COLOR, fg=FG_GREEN, selectcolor=BG_COLOR, activebackground=BG_COLOR, activeforeground=FG_GREEN).pack()

        def process_payment():
            messagebox.showinfo("SYS_MSG", f"TRANSACTION VERIFIED.\n{total_cost:.2f} cR TRANSFERRED VIA {pay_var.get()}.\nSESSION SECURE.", parent=bill_win)
            bill_win.destroy()
            self.listbox.selection_clear(0, tk.END)

        tk.Button(bill_win, text="[ AUTHORIZE TRANSFER ]", command=process_payment, bg=BTN_BG, fg=FG_CYAN, font=FONT_MAIN, bd=1, relief="solid", pady=5).pack(pady=20)
