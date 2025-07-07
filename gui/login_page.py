import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image  # Add this import at the top
from .adminlogin import AdminLogin  
from .userlogin import UserLogin

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Lost and Found System")
        self.master.geometry("1200x700")
        self.master.resizable(False, False)
        
        # Configure grid for 30%-70% split
        self.master.columnconfigure(0, weight=35)
        self.master.columnconfigure(1, weight=65)
        self.master.rowconfigure(0, weight=1)
        
        # Left Panel (30%) - Dark Blue
        self.left_panel = tk.Frame(self.master, bg='#1a2c56')
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Right Panel (70%) - Light Grey
        self.right_panel = tk.Frame(self.master, bg='#f5f5f5')
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Left Panel Content
        left_content = tk.Frame(self.left_panel, bg='#1a2c56')
        left_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Load and display logo
        try:
            # Adjust the path according to your project structure
            logo_path = "gui/images/logo.png"  # or "../images/db.png" depending on your folder structure
            logo_img = Image.open(logo_path)
            # Resize logo (adjust dimensions as needed)
            logo_img = logo_img.resize((160,150 ), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            
            logo_label = tk.Label(
                left_content,
                image=self.logo,
                bg='#1a2c56'
            )
            logo_label.pack(pady=(0, 20))  # Add some padding below the logo
        except Exception as e:
            print(f"Error loading logo: {e}")
            # You could add a placeholder text here if the logo fails to load
        
        title_label = tk.Label(
            left_content,
            text="Lost and Found System",
            font=('Helvetica', 22, 'bold'),
            fg='#ffffff',
            bg='#1a2c56'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            left_content,
            text="Lab Project - Database",
            font=('Helvetica', 12),
            fg='#b3b3b3',
            bg='#1a2c56'
        )
        subtitle_label.pack(pady=(0, 20))  # Reduced padding to accommodate logo
        
        welcome_label = tk.Label(
            left_content,
            text="Welcome to the login page!",
            font=('Helvetica', 16),
            fg='#ffffff',
            bg='#1a2c56'
        )
        welcome_label.pack()
        
        # Rest of your code remains the same...
        # Right Panel Content
        right_content = tk.Frame(self.right_panel, bg='#f5f5f5')
        right_content.place(relx=0.5, rely=0.5, anchor='center')
        
        login_prompt = tk.Label(
            right_content,
            text="Select Login Type",
            font=('Helvetica', 18),
            fg='#333333',
            bg='#f5f5f5'
        )
        login_prompt.pack(pady=(0, 50))
        
        button_frame = tk.Frame(right_content, bg='#f5f5f5')
        button_frame.pack()
        
        # Custom Button Style
        style = ttk.Style()
        
        # Normal State
        style.configure('Custom.TButton', 
                      borderwidth=0,
                      relief="flat",
                      background='#1a2c56',
                      foreground='#1a2c56',
                      font=('Helvetica', 12),
                      padding=12,
                      width=15)
        
        # Hover State
        style.map('Custom.TButton',
                background=[('active', '#e6e6e6')],
                foreground=[('active', '#1a2c56')])
        
        # Admin Button
        self.admin_btn = ttk.Button(
            button_frame,
            text="Admin Login",
            command=self.open_admin_login,
            style='Custom.TButton'
        )
        self.admin_btn.pack(side=tk.LEFT, padx=15, pady=10, ipadx=10)
        
        # User Button
        self.user_btn = ttk.Button(
            button_frame,
            text="User Login",
            command=self.open_user_login,
            style='Custom.TButton'
        )
        self.user_btn.pack(side=tk.LEFT, padx=15, pady=10, ipadx=10)
    
    def open_admin_login(self):
        self.master.withdraw()
        admin_window = tk.Toplevel(self.master)
        AdminLogin(admin_window, self.master)
    
    def open_user_login(self):
        self.master.withdraw()
        user_window = tk.Toplevel(self.master)
        UserLogin(user_window, self.master)