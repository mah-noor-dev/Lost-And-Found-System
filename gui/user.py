import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
from gui.addlost import AddLostItem
from gui.addfound import AddFoundItem
from db.db_config import DBConfig

class UserDashboard:
    def __init__(self, master, login_master, name, email, phone):
        self.master = master
        self.login_master = login_master
        self.name = name
        self.email = email
        self.phone = phone
        
        self.master.title(f"User Dashboard - {name}")
        self.master.geometry("1200x700")
        self.master.resizable(False, False)
        
        # Configure grid for 20%-80% split
        self.master.columnconfigure(0, weight=30)
        self.master.columnconfigure(1, weight=70)
        self.master.rowconfigure(0, weight=1)
        
        # Left Panel (20%) - Dark Blue
        self.left_panel = tk.Frame(self.master, bg='#1a2c56')
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        # Right Panel (80%) - Light Grey
        self.right_panel = tk.Frame(self.master, bg='#f5f5f5')
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # Left Panel Content (Navigation)
        self.create_navigation_panel()
        
        # Right Panel Content (Main Content)
        self.create_welcome_content()
        
        # Handle window close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_navigation_panel(self):
        nav_content = tk.Frame(self.left_panel, bg='#1a2c56')
        nav_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Welcome Label
        welcome_label = tk.Label(
            nav_content,
            text=f"Welcome,\n{self.name}",
            font=('Helvetica', 14, 'bold'),
            fg='#ffffff',
            bg='#1a2c56',
            justify='center'
        )
        welcome_label.pack(pady=(0, 30))
        
        # Navigation Buttons
        buttons = [
            ("Dashboard", self.show_welcome),
            ("Report Lost Item", self.show_add_lost),
            ("Report Found Item", self.show_add_found),
            ("View Lost Items", self.show_all_lost_items),
            ("View Found Items", self.show_all_found_items),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                nav_content,
                text=text,
                font=('Helvetica', 12),
                bg='#1a2c56',
                fg="#FFFFFF",
                activebackground='#2d3e76',
                activeforeground='#ffffff',
                bd=0,
                padx=20,
                pady=10,
                width=15,
                command=command,
                relief='flat'
            )
            btn.pack(pady=5)
    
    def create_welcome_content(self):
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        welcome_content = tk.Frame(self.right_panel, bg='#f5f5f5')
        welcome_content.place(relx=0.5, rely=0.5, anchor='center')
        
        tk.Label(
            welcome_content,
            text=f"Welcome to Lost and Found System",
            font=('Helvetica', 20, 'bold'),
            fg='#333333',
            bg='#f5f5f5'
        ).pack(pady=(0, 20))
        
        tk.Label(
            welcome_content,
            text=f"Hello, {self.name}!",
            font=('Helvetica', 16),
            fg='#1a2c56',
            bg='#f5f5f5'
        ).pack(pady=(0, 10))
        
        tk.Label(
            welcome_content,
            text="Please use the navigation menu to report or view lost and found items.",
            font=('Helvetica', 12),
            fg='#666666',
            bg='#f5f5f5'
        ).pack(pady=(0, 30))
        
        # User info frame
        info_frame = tk.Frame(welcome_content, bg='#e6e6e6', padx=20, pady=15)
        info_frame.pack()
        
        tk.Label(
            info_frame,
            text="Your Information:",
            font=('Helvetica', 12, 'bold'),
            fg='#333333',
            bg='#e6e6e6'
        ).grid(row=0, column=0, sticky='w', pady=(0, 10))
        
        tk.Label(
            info_frame,
            text=f"Email: {self.email}",
            font=('Helvetica', 11),
            fg='#333333',
            bg='#e6e6e6'
        ).grid(row=1, column=0, sticky='w')
        
        tk.Label(
            info_frame,
            text=f"Phone: {self.phone}",
            font=('Helvetica', 11),
            fg='#333333',
            bg='#e6e6e6'
        ).grid(row=2, column=0, sticky='w')
    
    def show_welcome(self):
        self.create_welcome_content()
    
    def show_add_lost(self):
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Create AddLostItem frame in right panel
        AddLostItem(self.right_panel, self.email)
    
    def show_add_found(self):
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Create AddFoundItem frame in right panel
        AddFoundItem(self.right_panel, self.email)
    
    def show_all_lost_items(self):
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Create container frame with 70%-30% split
        container = tk.Frame(self.right_panel, bg='#f5f5f5')
        container.pack(fill='both', expand=True)
        
        # Left panel (70%) for table
        left_panel = tk.Frame(container, bg='#f5f5f5')
        left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Right panel (30%) for image display
        right_panel = tk.Frame(container, bg='#ffffff', width=300, relief='groove', bd=1)
        right_panel.pack(side='right', fill='y', padx=10, pady=10)
        right_panel.pack_propagate(False)
        
        # Image display area
        image_frame = tk.Frame(right_panel, bg='#ffffff')
        image_frame.pack(pady=20)
        
        self.lost_item_image_label = tk.Label(
            image_frame,
            text="Select an item to view image",
            bg='#ffffff',
            fg='#666666',
            wraplength=250
        )
        self.lost_item_image_label.pack()
        
        # Title
        title_frame = tk.Frame(left_panel, bg='#f5f5f5')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="All Lost Items",
            font=('Helvetica', 18, 'bold'),
            fg='#1a2c56',
            bg='#f5f5f5'
        ).pack(side='left')
        
        # Refresh button
        refresh_btn = tk.Button(
            title_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#1a2c56',
            fg='white',
            command=self.show_all_lost_items
        )
        refresh_btn.pack(side='right')
        
        # Treeview frame
        tree_frame = tk.Frame(left_panel, bg='#f5f5f5')
        tree_frame.pack(fill='both', expand=True)
        
        # Create Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'item_name', 'lost_date', 'location', 'status'),
            show='headings',
            selectmode='browse'
        )
        
        # Define columns
        tree.heading('id', text='ID')
        tree.heading('item_name', text='Item Name')
        tree.heading('lost_date', text='Lost Date')
        tree.heading('location', text='Location')
        tree.heading('status', text='Status')
        
        # Set column widths
        tree.column('id', width=50, anchor='center')
        tree.column('item_name', width=150)
        tree.column('lost_date', width=100)
        tree.column('location', width=120)
        tree.column('status', width=80, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        # Bind selection event
        tree.bind('<<TreeviewSelect>>', lambda e: self.show_selected_lost_item_image(tree))
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background='#1a2c56', foreground='white')
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        style.map("Treeview", background=[('selected', '#2d3e76')])
        
        # Fetch data from database
        try:
            lost_items = self.get_lost_items_from_db()
            
            # Insert data into treeview
            for item in lost_items:
                tree.insert('', 'end', values=item)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load lost items: {str(e)}")
    
    def show_selected_lost_item_image(self, tree):
        selected_item = tree.focus()
        if not selected_item:
            return
        
        item_data = tree.item(selected_item)
        item_id = item_data['values'][0]
        
        conn = None
        try:
            conn = DBConfig.get_connection()
            if conn:
                cursor = conn.cursor()
                
                # First check if image exists
                cursor.execute("""
                    SELECT CASE WHEN item_image IS NULL THEN 0 ELSE 1 END as has_image 
                    FROM lost_items WHERE id = :id
                """, {'id': item_id})
                has_image = cursor.fetchone()[0]
                
                if has_image:
                    # Get the BLOB data directly
                    cursor.execute("""
                        SELECT item_image FROM lost_items 
                        WHERE id = :id
                    """, {'id': item_id})
                    blob_data = cursor.fetchone()[0]
                    
                    if blob_data:
                        try:
                            # Convert BLOB to image
                            image = Image.open(io.BytesIO(blob_data.read()))
                            image.thumbnail((250, 250))
                            photo = ImageTk.PhotoImage(image)
                            
                            self.lost_item_image_label.config(
                                image=photo,
                                text=""
                            )
                            self.lost_item_image_label.image = photo
                        except Exception as img_error:
                            print(f"Image error: {img_error}")
                            self.lost_item_image_label.config(
                                image=None,
                                text="Image format not supported"
                            )
                    else:
                        self.lost_item_image_label.config(
                            image=None,
                            text="No image available"
                        )
                else:
                    self.lost_item_image_label.config(
                        image=None,
                        text="No image available"
                    )
                    
        except Exception as e:
            print(f"Database error: {e}")
            self.lost_item_image_label.config(
                image=None,
                text="Error loading image"
            )
        finally:
            if conn:
                conn.close()
    
    def show_all_found_items(self):
        # Clear right panel
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        
        # Create container frame with 70%-30% split
        container = tk.Frame(self.right_panel, bg='#f5f5f5')
        container.pack(fill='both', expand=True)
        
        # Left panel (70%) for table
        left_panel = tk.Frame(container, bg='#f5f5f5')
        left_panel.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
        # Right panel (30%) for image display
        right_panel = tk.Frame(container, bg='#ffffff', width=300, relief='groove', bd=1)
        right_panel.pack(side='right', fill='y', padx=10, pady=10)
        right_panel.pack_propagate(False)
        
        # Image display area
        image_frame = tk.Frame(right_panel, bg='#ffffff')
        image_frame.pack(pady=20)
        
        self.found_item_image_label = tk.Label(
            image_frame,
            text="Select an item to view image",
            bg='#ffffff',
            fg='#666666',
            wraplength=250
        )
        self.found_item_image_label.pack()
        
        # Title
        title_frame = tk.Frame(left_panel, bg='#f5f5f5')
        title_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="All Found Items",
            font=('Helvetica', 18, 'bold'),
            fg='#1a2c56',
            bg='#f5f5f5'
        ).pack(side='left')
        
        # Refresh button
        refresh_btn = tk.Button(
            title_frame,
            text="Refresh",
            font=('Helvetica', 10),
            bg='#1a2c56',
            fg='white',
            command=self.show_all_found_items
        )
        refresh_btn.pack(side='right')
        
        # Treeview frame
        tree_frame = tk.Frame(left_panel, bg='#f5f5f5')
        tree_frame.pack(fill='both', expand=True)
        
        # Create Treeview
        tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'item_name', 'found_date', 'location', 'status'),
            show='headings',
            selectmode='browse'
        )
        
        # Define columns
        tree.heading('id', text='ID')
        tree.heading('item_name', text='Item Name')
        tree.heading('found_date', text='Found Date')
        tree.heading('location', text='Location')
        tree.heading('status', text='Status')
        
        # Set column widths
        tree.column('id', width=50, anchor='center')
        tree.column('item_name', width=150)
        tree.column('found_date', width=100)
        tree.column('location', width=120)
        tree.column('status', width=80, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)
        
        # Bind selection event
        tree.bind('<<TreeviewSelect>>', lambda e: self.show_selected_found_item_image(tree))
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background='#1a2c56', foreground='white')
        style.configure("Treeview", font=('Helvetica', 10), rowheight=25)
        style.map("Treeview", background=[('selected', '#2d3e76')])
        
        # Fetch data from database
        try:
            found_items = self.get_found_items_from_db()
            
            # Insert data into treeview
            for item in found_items:
                tree.insert('', 'end', values=item)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load found items: {str(e)}")
    
    def show_selected_found_item_image(self, tree):
        selected_item = tree.focus()
        if not selected_item:
            return
        
        item_data = tree.item(selected_item)
        item_id = item_data['values'][0]
        
        conn = None
        try:
            conn = DBConfig.get_connection()
            if conn:
                cursor = conn.cursor()
                
                # First check if image exists
                cursor.execute("""
                    SELECT CASE WHEN item_image IS NULL THEN 0 ELSE 1 END as has_image 
                    FROM found_items WHERE id = :id
                """, {'id': item_id})
                has_image = cursor.fetchone()[0]
                
                if has_image:
                    # Get the BLOB data directly
                    cursor.execute("""
                        SELECT item_image FROM found_items 
                        WHERE id = :id
                    """, {'id': item_id})
                    blob_data = cursor.fetchone()[0]
                    
                    if blob_data:
                        try:
                            # Convert BLOB to image
                            image = Image.open(io.BytesIO(blob_data.read()))
                            image.thumbnail((250, 250))
                            photo = ImageTk.PhotoImage(image)
                            
                            self.found_item_image_label.config(
                                image=photo,
                                text=""
                            )
                            self.found_item_image_label.image = photo
                        except Exception as img_error:
                            print(f"Image error: {img_error}")
                            self.found_item_image_label.config(
                                image=None,
                                text="Image format not supported"
                            )
                    else:
                        self.found_item_image_label.config(
                            image=None,
                            text="No image available"
                        )
                else:
                    self.found_item_image_label.config(
                        image=None,
                        text="No image available"
                    )
                    
        except Exception as e:
            print(f"Database error: {e}")
            self.found_item_image_label.config(
                image=None,
                text="Error loading image"
            )
        finally:
            if conn:
                conn.close()
    def get_lost_items_from_db(self):
        """Fetch lost items from database"""
        conn = None
        try:
            conn = DBConfig.get_connection()
            if conn:
                cursor = conn.cursor()
                
                query = """
                SELECT id, item_name, 
                    TO_CHAR(date_lost, 'YYYY-MM-DD'), 
                    location, status 
                FROM lost_items
                ORDER BY date_lost DESC
                """
                
                cursor.execute(query)
                return cursor.fetchall()
            else:
                messagebox.showerror("Error", "Could not connect to database")
                return []
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching lost items: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def get_found_items_from_db(self):
        """Fetch found items from database"""
        conn = None
        try:
            conn = DBConfig.get_connection()
            if conn:
                cursor = conn.cursor()
                
                query = """
                SELECT id, item_name, 
                    TO_CHAR(date_found, 'YYYY-MM-DD'), 
                    location, status 
                FROM found_items
                ORDER BY date_found DESC
                """
                
                cursor.execute(query)
                return cursor.fetchall()
            else:
                messagebox.showerror("Error", "Could not connect to database")
                return []
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Error fetching found items: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def logout(self):
        self.master.destroy()
        self.login_master.deiconify()
    
    def on_close(self):
        """Handle window close event"""
        self.logout()