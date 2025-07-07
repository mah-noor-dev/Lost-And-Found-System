import tkinter as tk
from tkinter import ttk, messagebox
import re
from PIL import ImageTk, Image
from db.db_config import DBConfig
from gui.user import UserDashboard

class UserLogin:
    def __init__(self, master, login_master):
        self.master = master
        self.login_master = login_master
        self.master.title("User Login - Lost and Found System")
        self.master.geometry("1200x700")
        self.master.resizable(False, False)
        
        # Configure grid for 30%-70% split (consistent with login_page.py)
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
            
            logo_path = "gui/images/user.png"  #  folder structure
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
            text="User Login",
            font=('Helvetica', 22, 'bold'),
            fg='#ffffff',
            bg='#1a2c56'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            left_content,
            text="Access your account",
            font=('Helvetica', 12),
            fg='#b3b3b3',
            bg='#1a2c56'
        )
        subtitle_label.pack(pady=(0, 40))
        
        welcome_label = tk.Label(
            left_content,
            text="Please enter your details",
            font=('Helvetica', 16),
            fg='#ffffff',
            bg='#1a2c56'
        )
        welcome_label.pack()
        
        # Right Panel Content
        right_content = tk.Frame(self.right_panel, bg='#f5f5f5')
        right_content.place(relx=0.5, rely=0.5, anchor='center')
        
        login_prompt = tk.Label(
            right_content,
            text="Enter Your Information",
            font=('Helvetica', 18),
            fg='#333333',
            bg='#f5f5f5'
        )
        login_prompt.pack(pady=(0, 30))
        
        # Form Frame
        form_frame = tk.Frame(right_content, bg='#f5f5f5')
        form_frame.pack(pady=10)
        
        # Name Field
        tk.Label(
            form_frame,
            text="Full Name:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        
        self.name_entry = ttk.Entry(
            form_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Email Field
        tk.Label(
            form_frame,
            text="Email:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.email_entry = ttk.Entry(
            form_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Phone Field
        tk.Label(
            form_frame,
            text="Phone:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=2, column=0, padx=10, pady=10, sticky='e')
        
        self.phone_entry = ttk.Entry(
            form_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Button Frame
        button_frame = tk.Frame(right_content, bg='#f5f5f5')
        button_frame.pack(pady=20)
        
        # Custom Button Style (consistent with login_page.py)
        style = ttk.Style()
        style.configure('Custom.TButton', 
                        borderwidth=0,
                        relief="flat",
                        background='#1a2c56',
                        foreground='#1a2c56',
                        font=('Helvetica', 12),
                        padding=12,
                        width=15)
        style.map('Custom.TButton',
                  background=[('active', '#e6e6e6')],
                  foreground=[('active', '#1a2c56')])
        
        # Login Button
        self.login_btn = ttk.Button(
            button_frame,
            text="Login",
            command=self.validate_and_login,
            style='Custom.TButton'
        )
        self.login_btn.pack(side=tk.LEFT, padx=15, pady=10, ipadx=10)
        
        # Back Button
        self.back_btn = ttk.Button(
            button_frame,
            text="Back",
            command=self.go_back,
            style='Custom.TButton'
        )
        self.back_btn.pack(side=tk.LEFT, padx=15, pady=10, ipadx=10)
        
        # Handle window close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def validate_and_login(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        # Validate inputs
        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return
        
        if not email:
            messagebox.showerror("Error", "Please enter your email")
            return
        
        if not self.is_valid_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if not phone:
            messagebox.showerror("Error", "Please enter your phone number")
            return
        
        if not re.match(r'^03[0-9]{9}$', phone):
            messagebox.showerror("Error", "Please enter a valid Pakistani phone number (e.g., 03XXXXXXXXX)")
            return

        
        # If validation passes, proceed with login
        self.store_user_and_login(name, email, phone)
    
    def is_valid_email(self, email):
        """Simple email validation using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def store_user_and_login(self, name, email, phone):
        try:
            # Use your existing DBConfig
            db = DBConfig()
            connection = db.get_connection()
            cursor = connection.cursor()
            
            # Check if user already exists in login_users table
            cursor.execute("""
                SELECT COUNT(*) FROM login_users 
                WHERE email = :email AND phone = :phone
            """, {'email': email, 'phone': phone})
            
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert new user into login_users table
                cursor.execute("""
                    INSERT INTO login_users (name, email, phone) 
                    VALUES (:name, :email, :phone)
                """, {'name': name, 'email': email, 'phone': phone})
                connection.commit()
                messagebox.showinfo("Success", "New user login recorded successfully!")
            else:
                messagebox.showinfo("Welcome Back", f"Welcome back, {name}!")
            
            # Close database connection
            cursor.close()
            connection.close()
            
            # Proceed to main application
            self.open_main_application(name)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def open_main_application(self, name):
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Hide login window
        self.master.withdraw()
        
        # Create dashboard window
        dashboard_window = tk.Toplevel(self.master)
        UserDashboard(dashboard_window, self.login_master, name, email, phone)
    
    def go_back(self):
        """Return to the login page"""
        self.master.destroy()
        self.login_master.deiconify()
    
    def on_close(self):
        """Handle window close event"""
        self.go_back()
