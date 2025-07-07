from gui.login_page import LoginPage
import tkinter as tk

def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop() 

if __name__ == "__main__":
    main()