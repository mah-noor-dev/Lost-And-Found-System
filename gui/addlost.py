import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk
import io
from db.db_config import DBConfig

class AddLostItem:
    def __init__(self, master, user_email):
        self.master = master
        self.user_email = user_email
        self.image_data = None
        
        self.create_form()
    
    def create_form(self):
        form_frame = tk.Frame(self.master, bg='#f5f5f5')
        form_frame.pack(pady=20)
        
        # Title
        tk.Label(
            form_frame,
            text="Report Lost Item",
            font=('Helvetica', 18, 'bold'),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Item Name
        tk.Label(
            form_frame,
            text="Item Name:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=1, column=0, padx=10, pady=10, sticky='e')
        
        self.item_name_entry = ttk.Entry(
            form_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.item_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')
        
        # Description
        tk.Label(
            form_frame,
            text="Description:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=2, column=0, padx=10, pady=10, sticky='ne')
        
        self.description_entry = tk.Text(
            form_frame,
            font=('Helvetica', 12),
            width=30,
            height=5
        )
        self.description_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        
        # Date Lost
        tk.Label(
            form_frame,
            text="Date Lost:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=3, column=0, padx=10, pady=10, sticky='e')
        
        self.date_lost_entry = ttk.Entry(
            form_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.date_lost_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        self.date_lost_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Location
        tk.Label(
            form_frame,
            text="Location:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=4, column=0, padx=10, pady=10, sticky='e')
        
        self.location_entry = ttk.Entry(
            form_frame,
            font=('Helvetica', 12),
            width=30
        )
        self.location_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
        # Image Upload
        tk.Label(
            form_frame,
            text="Item Image:",
            font=('Helvetica', 12),
            fg='#333333',
            bg='#f5f5f5'
        ).grid(row=5, column=0, padx=10, pady=10, sticky='e')
        
        self.image_frame = tk.Frame(
            form_frame,
            bg='#e6e6e6',
            width=200,
            height=150,
            relief='groove',
            bd=1
        )
        self.image_frame.grid(row=5, column=1, padx=10, pady=10, sticky='w')
        self.image_frame.grid_propagate(False)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="No image selected",
            bg='#e6e6e6',
            fg='#666666'
        )
        self.image_label.place(relx=0.5, rely=0.5, anchor='center')
        
        upload_btn = ttk.Button(
            form_frame,
            text="Upload Image",
            command=self.upload_image,
            style='Upload.TButton'
        )
        upload_btn.grid(row=6, column=1, pady=5, sticky='w')
        
        # Submit Button
        submit_btn = ttk.Button(
            form_frame,
            text="Submit Report",
            command=self.submit_lost_item,
            style='Custom.TButton'
        )
        submit_btn.grid(row=7, column=1, pady=20, sticky='w')
        
        # Configure styles
        style = ttk.Style()
        style.configure('Custom.TButton', 
                      borderwidth=0,
                      relief="flat",
                      background='#1a2c56',
                      foreground='#ffffff',
                      font=('Helvetica', 12),
                      padding=10)
        style.configure('Upload.TButton',
                      font=('Helvetica', 10),
                      padding=5)
    
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Item Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        
        if file_path:
            try:
                # First verify the image is valid
                with Image.open(file_path) as img:
                    img.verify()  # Verify it's a valid image
                    
                # Now open again for processing
                with Image.open(file_path) as img:
                    img.thumbnail((180, 140))
                    photo = ImageTk.PhotoImage(img)
                    
                    self.image_label.config(image=photo, text="")
                    self.image_label.image = photo
                    
                    # Read file in binary mode
                    with open(file_path, 'rb') as f:
                        self.image_data = f.read()
                        
            except Exception as e:
                messagebox.showerror("Error", f"Invalid image file: {str(e)}")
                self.image_data = None
    
    def clear_form(self):
        """Clear all form fields"""
        self.item_name_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.date_lost_entry.delete(0, tk.END)
        self.date_lost_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.location_entry.delete(0, tk.END)
        self.image_label.config(image=None, text="No image selected")
        self.image_data = None
    
    def submit_lost_item(self):
        item_name = self.item_name_entry.get().strip()
        description = self.description_entry.get("1.0", tk.END).strip()
        date_lost = self.date_lost_entry.get().strip()
        location = self.location_entry.get().strip()
        
        # Validate inputs
        if not item_name:
            messagebox.showerror("Error", "Please enter the item name")
            return
        
        if not description:
            messagebox.showerror("Error", "Please enter a description")
            return
        
        if not date_lost:
            messagebox.showerror("Error", "Please enter the date lost")
            return
        
        try:
            db = DBConfig()
            connection = db.get_connection()
            if connection is None:
                messagebox.showerror("Error", "Could not connect to database")
                return
                
            cursor = connection.cursor()
            
            # Insert into lost_items table
            cursor.execute("""
                INSERT INTO lost_items (
                    user_email, 
                    item_name, 
                    description, 
                    date_lost, 
                    location, 
                    status,
                    item_image
                ) VALUES (
                    :email, 
                    :item_name, 
                    :description, 
                    TO_DATE(:date_lost, 'YYYY-MM-DD'), 
                    :location, 
                    'Pending',
                    :image
                )
            """, {
                'email': self.user_email,
                'item_name': item_name,
                'description': description,
                'date_lost': date_lost,
                'location': location,
                'image': self.image_data if self.image_data else None
            })
            
            connection.commit()
            messagebox.showinfo("Success", "Lost item report submitted successfully!")
            
            # Clear form after successful submission
            self.clear_form()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit report: {str(e)}")
        finally:
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()