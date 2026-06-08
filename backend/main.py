# main.py
import tkinter as tk
from auth_ui import AuthUI
from admin_ui import AdminUI
from guest_ui import GuestUI

# ==========================================
# Bootstrapper
# ==========================================
class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw() # Hide until authenticated
        AuthUI(self.root, self.on_auth_success)

    def on_auth_success(self, first_name, role):
        self.root.deiconify() # Show main window
        if role == "Admin":
            app = AdminUI(self.root, first_name)
            self.root.protocol("WM_DELETE_WINDOW", app.on_closing)
        else:
            app = GuestUI(self.root, first_name)
            self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.run()
