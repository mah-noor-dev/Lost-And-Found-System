import tkinter as tk
from tkinter import ttk, messagebox
from db.db_config import DBConfig
from PIL import ImageTk, Image
from gui.admin import AdminDashboard

class AdminLogin:
    def __init__(self, master, login_master):
        self.master = master
        self.login_master = login_master
        self.master.title("Admin Login")
        self.master.geometry("1200x700")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configure grid for 30%-70% split (consistent with login_page)
        self.master.columnconfigure(0, weight=30)
        self.master.columnconfigure(1, weight=70)
        self.master.rowconfigure(0, weight=1)
        
        # Left Panel (30%) - Dark Blue
        self.left_panel = tk.Frame(self.master, bg='#1a2c56')
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Right Panel (70%) - Light Grey
        self.right_panel = tk.Frame(self.master, bg='#f5f5f5')
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Left Panel Content (same as login_page)
        left_content = tk.Frame(self.left_panel, bg='#1a2c56')
        left_content.place(relx=0.5, rely=0.5, anchor='center')
        # Load and display logo
        try:
            # Adjust the path according to your project structure
            logo_path = "gui/images/adminlogo.png"  # or "../images/db.png" depending on your folder structure
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
            text="Admin Portal",
            font=('Helvetica', 12),
            fg='#b3b3b3',
            bg='#1a2c56'
        )
        subtitle_label.pack(pady=(0, 40))
        
        welcome_label = tk.Label(
            left_content,
            text="Admin Authentication",
            font=('Helvetica', 16),
            fg='#ffffff',
            bg='#1a2c56'
        )
        welcome_label.pack()
        
        # Right Panel Content - Login Form
        right_content = tk.Frame(self.right_panel, bg='#f5f5f5')
        right_content.place(relx=0.5, rely=0.5, anchor='center')
        
        login_prompt = tk.Label(
            right_content,
            text="Admin Login",
            font=('Helvetica', 18),
            fg='#333333',
            bg='#f5f5f5'
        )
        login_prompt.pack(pady=(0, 30))
        
        # Form Frame
        form_frame = tk.Frame(right_content, bg='#f5f5f5')
        form_frame.pack()
        
        # Email Field
        ttk.Label(
            form_frame,
            text="Email:",
            background='#f5f5f5',
            font=('Helvetica', 11)
        ).grid(row=0, column=0, pady=10, sticky='e')
        
        self.email_entry = ttk.Entry(
            form_frame,
            width=30,
            font=('Helvetica', 11)
        )
        self.email_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Password Field
        ttk.Label(
            form_frame,
            text="Password:",
            background='#f5f5f5',
            font=('Helvetica', 11)
        ).grid(row=1, column=0, pady=10, sticky='e')
        
        self.password_entry = ttk.Entry(
            form_frame,
            width=30,
            show="*",
            font=('Helvetica', 11)
        )
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Button Style
        style = ttk.Style()
        style.configure('Login.TButton',
                      borderwidth=0,
                      relief="flat",
                      background="#ffffff",
                      foreground='#1a2c56',
                      font=('Helvetica', 12),
                      padding=10)
        style.map('Login.TButton',
                background=[('active', '#2a3c66')])
        
        # Login Button
        login_btn = ttk.Button(
            right_content,
            text="Login",
            style='Login.TButton',
            command=self.authenticate
        )
        login_btn.pack(pady=30, ipadx=20)
    
    def authenticate(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        try:
            connection = DBConfig.get_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM admin WHERE email = :email AND password = :password",
                    {'email': email, 'password': password}
)
                admin = cursor.fetchone()
                
                if admin:
                    self.master.withdraw()
                    admin_dash_window = tk.Toplevel(self.master)
                    AdminDashboard(admin_dash_window, self.master)
                else:
                    messagebox.showerror("Login Failed", "Invalid email or password")
                
                cursor.close()
                connection.close()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
    
    def on_close(self):
        self.login_master.deiconify()
        self.master.destroy()