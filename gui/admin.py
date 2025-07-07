import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from email.message import EmailMessage
import smtplib
import csv
from PIL import Image, ImageTk 
import io
from datetime import datetime
from db.db_config import DBConfig

class AdminDashboard:
    def __init__(self, master, return_to_login):
        self.master = master
        self.return_to_login = return_to_login
        self.conn = DBConfig.get_connection()
         
        self.cursor = self.conn.cursor()
        
        # Window setup
        self.master.title("Admin Dashboard")
        self.master.geometry("1200x700")
        self.master.resizable(False, False)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Main UI
        self.setup_ui()
        self.load_initial_data()
        
    def setup_ui(self):
        """Initialize all UI components"""
        # Main container
        self.main_frame = tk.Frame(self.master, bg='#f5f5f5')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        self.header_panel = tk.Frame(self.main_frame, bg='#1a2c56', height=80)
        self.header_panel.pack(fill=tk.X)
        
        # Title
        tk.Label(
            self.header_panel,
            text="Admin Dashboard",
            font=('Helvetica', 20, 'bold'),
            fg='white',
            bg='#1a2c56'
        ).pack(side=tk.LEFT, padx=20)
        ttk.Button(
    self.header_panel,
    text="🔄 Refresh All Data",
    command=self.load_initial_data,
    style='Admin.TButton'
).pack(side=tk.RIGHT, padx=10)
        # Logout button
        ttk.Button(
            self.header_panel,
            text="Logout",
            command=self.logout,
            style='Admin.TButton'
        ).pack(side=tk.RIGHT, padx=20)
        
        # Tab control
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tabs = {
            'matching': tk.Frame(self.tab_control, bg='#f5f5f5'),
            'reports': tk.Frame(self.tab_control, bg='#f5f5f5'),
            'stats': tk.Frame(self.tab_control, bg='#f5f5f5'),
            'email': tk.Frame(self.tab_control, bg='#f5f5f5'),
            'users': tk.Frame(self.tab_control, bg='#f5f5f5') 
        }
        
        
        for name, frame in self.tabs.items():
            self.tab_control.add(frame, text=name.capitalize())
        
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Admin.TButton', 
                          borderwidth=0,
                          relief="flat",
                          background='#003366',
                          foreground='white',
                          font=('Helvetica', 10),
                          padding=8)
        self.style.map('Admin.TButton',
                     background=[('active', 'white')],
                     foreground=[('active', 'black')])
        
        # Setup each tab
        self.setup_matching_tab()
        self.setup_reports_tab()
        self.setup_stats_tab()
        self.setup_email_tab()
        self.setup_users_tab()
    
    def setup_matching_tab(self):
        """Dual-pane matching interface"""
        tab = self.tabs['matching']
        
        # Main frame
        match_frame = tk.Frame(tab, bg='#f5f5f5')
        match_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left pane - Lost Items
        lost_frame = tk.Frame(match_frame, bg='white', bd=2, relief=tk.GROOVE)
        lost_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(
            lost_frame,
            text="Lost Items (Pending)",
            font=('Helvetica', 12, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        self.lost_tree = ttk.Treeview(lost_frame, columns=('id', 'user', 'item', 'date', 'location'), show='headings')
        for col, text in [('id', 'ID'), ('user', 'User Email'), ('item', 'Item Name'), ('date', 'Date Lost'), ('location', 'Location')]:
            self.lost_tree.heading(col, text=text)
            self.lost_tree.column(col, width=100)
        self.lost_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right pane - Found Items
        found_frame = tk.Frame(match_frame, bg='white', bd=2, relief=tk.GROOVE)
        found_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tk.Label(
            found_frame,
            text="Found Items (Pending)",
            font=('Helvetica', 12, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        self.found_tree = ttk.Treeview(found_frame, columns=('id', 'user', 'item', 'date', 'location'), show='headings')
        for col, text in [('id', 'ID'), ('user', 'User Email'), ('item', 'Item Name'), ('date', 'Date Found'), ('location', 'Location')]:
            self.found_tree.heading(col, text=text)
            self.found_tree.column(col, width=100)
        self.found_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control buttons
        ctrl_frame = tk.Frame(match_frame, bg='#f5f5f5')
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(
            ctrl_frame,
            text="Match Selected",
            command=self.match_items,
            style='Admin.TButton'
        ).pack(pady=20)
        
        ttk.Button(
            ctrl_frame,
            text="Reject Match",
            command=self.reject_match,
            style='Admin.TButton'
        ).pack(pady=10)
    
    def setup_reports_tab(self):
        """Report management interface with guaranteed image/description display"""
        tab = self.tabs['reports']
        
        # Main container (70% table, 30% details)
        main_frame = tk.Frame(tab, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel (Table)
        left_frame = tk.Frame(main_frame, bg='#f5f5f5')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right panel (Details) - Fixed width
        self.details_frame = tk.Frame(main_frame, bg='white', width=350, bd=2, relief=tk.GROOVE)
        self.details_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        self.details_frame.pack_propagate(False)
        
        # Details title
        tk.Label(
            self.details_frame,
            text="Item Details",
            font=('Helvetica', 12, 'bold'),
            bg='white'
        ).pack(pady=10)
        
        # Image display
        self.detail_image = tk.Label(
            self.details_frame,
            text="Select item to view image",
            bg='white',
            fg='#666666',
            wraplength=320
        )
        self.detail_image.pack(pady=10)
        
        # Description label
        tk.Label(
            self.details_frame,
            text="Description:",
            font=('Helvetica', 10, 'bold'),
            bg='white'
        ).pack(pady=(5, 0), padx=10, anchor='w')
        
        # Scrollable description area
        desc_frame = tk.Frame(self.details_frame, bg='white')
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(desc_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.detail_desc = tk.Text(
            desc_frame,
            height=6,
            wrap=tk.WORD,
            bg='#f9f9f9',
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED
        )
        self.detail_desc.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.detail_desc.yview)
        
        # Search controls
        search_frame = tk.Frame(left_frame, bg='#f5f5f5')
        search_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(search_frame, text="Search:", bg='#f5f5f5').pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(
            search_frame,
            text="Search",
            command=self.search_reports,
            style='Admin.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        # Treeview
        tree_frame = tk.Frame(left_frame, bg='white', bd=2, relief=tk.GROOVE)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        self.report_tree = ttk.Treeview(
            tree_frame,
            columns=('id', 'type', 'item', 'date', 'location', 'reported'),
            show='headings'
        )
        
        # Configure columns
        for col, text in [('id', 'ID'), ('type', 'Type'), ('item', 'Item Name'),
                        ('date', 'Date'), ('location', 'Location'), ('reported', 'Reported On')]:
            self.report_tree.heading(col, text=text)
            self.report_tree.column(col, width=100)
        
        self.report_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Bind selection event
        self.report_tree.bind('<<TreeviewSelect>>', self.show_item_details)
        
        # Action buttons
        btn_frame = tk.Frame(left_frame, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X, pady=5)
        
        actions = [
            ('Approve', self.approve_report),
            ('Reject', self.reject_report),
            ('Edit', self.edit_report),
            ('Delete', self.delete_report)
        ]
        
        for text, cmd in actions:
            ttk.Button(
                btn_frame,
                text=text,
                command=cmd,
                style='Admin.TButton'
            ).pack(side=tk.LEFT, padx=5)
    
    def setup_stats_tab(self):
        """Statistics dashboard"""
        tab = self.tabs['stats']
        
        stats_frame = tk.Frame(tab, bg='#f5f5f5')
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.stat_labels = []
        stats = [
            "Total Lost Reports",
            "Total Found Reports",
            "Pending Matches",
            "Approved Matches",
            "Rejected Matches"
        ]
        
        for i, title in enumerate(stats):
            card = tk.Frame(stats_frame, bg='white', bd=2, relief=tk.GROOVE)
            card.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="nsew")
            
            tk.Label(
                card,
                text=title,
                font=('Helvetica', 10),
                bg='white'
            ).pack(pady=(10, 0))
            
            lbl = tk.Label(
                card,
                text="0",
                font=('Helvetica', 24, 'bold'),
                bg='white'
            )
            lbl.pack(pady=(0, 10))
            self.stat_labels.append(lbl)
        
        # Configure grid
        for i in range(3):
            stats_frame.columnconfigure(i, weight=1)
        for i in range(2):
            stats_frame.rowconfigure(i, weight=1)
    
    def setup_email_tab(self):
        """Email log viewer"""
        tab = self.tabs['email']
        
        email_frame = tk.Frame(tab, bg='white', bd=2, relief=tk.GROOVE)
        email_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.email_tree = ttk.Treeview(
            email_frame,
            columns=('id', 'recipient', 'subject', 'timestamp'),
            show='headings'
        )
        for col, text in [('id', 'ID'), ('recipient', 'Recipient'), 
                          ('subject', 'Subject'), ('timestamp', 'Timestamp')]:
            self.email_tree.heading(col, text=text)
        self.email_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Button(
            tab,
            text="Export to CSV",
            command=self.export_emails,
            style='Admin.TButton'
        ).pack(pady=10)
    def setup_users_tab(self):
        """Displays registered users in the 'Users' tab"""
        tab = self.tabs['users']
        
        user_frame = tk.Frame(tab, bg='white', bd=2, relief=tk.GROOVE)
        user_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.user_tree = ttk.Treeview(
            user_frame,
            columns=('id', 'name', 'email', 'phone', 'login_time'),
            show='headings'
        )
        for col, text in [
            ('id', 'ID'),
            ('name', 'Name'),
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('login_time', 'Login Time')
        ]:
            self.user_tree.heading(col, text=text)
            self.user_tree.column(col, width=150 if col != 'id' else 60)
        btn_frame = tk.Frame(tab, bg='#f5f5f5')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(
            btn_frame,
            text="Delete Selected User",
            command=self.delete_selected_user,
            style='Admin.TButton'
        ).pack(side=tk.LEFT, padx=10)    
        
        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        ttk.Button(
        btn_frame,
        text="Edit Selected User",
        command=self.edit_selected_user,
        style='Admin.TButton'
    ).pack(side=tk.LEFT, padx=10)
        ttk.Button(
        btn_frame,
        text="Send Email to User",
        command=self.send_email_to_user,
        style='Admin.TButton'
    ).pack(side=tk.LEFT, padx=10)
        
    def load_initial_data(self):
        """Load all initial data from database"""
        self.load_pending_items()
        self.load_all_reports()
        self.load_statistics()
        self.load_email_logs()
        self.load_user_data()
    
    def load_pending_items(self):
            try:
                # Clear trees
                for tree in [self.lost_tree, self.found_tree]:
                    tree.delete(*tree.get_children())
                
                # Load available lost items
                self.cursor.execute("""
                    SELECT id, user_email, item_name, 
                        TO_CHAR(date_lost, 'DD-MON-YYYY'), 
                        location
                    FROM lost_items
                    WHERE (matched_item_id IS NULL OR matched_item_id = 0)
                    AND id NOT IN (
                        SELECT lost_id FROM matches 
                        WHERE status = 'approved' AND lost_id IS NOT NULL
                    )
                    ORDER BY reported_on DESC
                """)
                for row in self.cursor:
                    self.lost_tree.insert('', 'end', values=row)
                
                # Load available found items
                self.cursor.execute("""
                    SELECT id, user_email, item_name, 
                        TO_CHAR(date_found, 'DD-MON-YYYY'), 
                        location
                    FROM found_items
                    WHERE (matched_item_id IS NULL OR matched_item_id = 0)
                    AND id NOT IN (
                        SELECT found_id FROM matches 
                        WHERE status = 'approved' AND found_id IS NOT NULL
                    )
                    ORDER BY reported_on DESC
                """)
                for row in self.cursor:
                    self.found_tree.insert('', 'end', values=row)
                    
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load items:\n{str(e)}")
    
    def load_all_reports(self):
        """Load all reports with description and image info"""
        try:
            self.report_tree.delete(*self.report_tree.get_children())
            
            # Load lost items WITH description
            self.cursor.execute("""
                SELECT ID, 'Lost', ITEM_NAME, 
                    TO_CHAR(DATE_LOST, 'DD-MON-YYYY'), 
                    LOCATION,
                    TO_CHAR(REPORTED_ON, 'DD-MON-YYYY HH24:MI:SS'),
                    DESCRIPTION,
                    CASE WHEN ITEM_IMAGE IS NULL THEN 0 ELSE 1 END AS HAS_IMAGE
                FROM lost_items 
                ORDER BY REPORTED_ON DESC
            """)
            for row in self.cursor:
                # Keep first 6 columns as before, add description and has_image
                self.report_tree.insert('', 'end', values=row[:6], 
                                    tags=(row[6], row[7]))  # description and has_image as tags
            
            # Load found items WITH description
            self.cursor.execute("""
                SELECT ID, 'Found', ITEM_NAME, 
                    TO_CHAR(DATE_FOUND, 'DD-MON-YYYY'), 
                    LOCATION,
                    TO_CHAR(REPORTED_ON, 'DD-MON-YYYY HH24:MI:SS'),
                    DESCRIPTION,
                    CASE WHEN ITEM_IMAGE IS NULL THEN 0 ELSE 1 END AS HAS_IMAGE
                FROM found_items 
                ORDER BY REPORTED_ON DESC
            """)
            for row in self.cursor:
                self.report_tree.insert('', 'end', values=row[:6], 
                                    tags=(row[6], row[7]))  # description and has_image as tags
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load reports:\n{str(e)}")
    
    def load_statistics(self):
        """Update statistics dashboard"""
        try:
            # Get counts from database
            self.cursor.execute("SELECT COUNT(*) FROM lost_items")
            total_lost = self.cursor.fetchone()[0]
            
            self.cursor.execute("SELECT COUNT(*) FROM found_items")
            total_found = self.cursor.fetchone()[0]
            
            self.cursor.execute("""
                SELECT COUNT(*) FROM matches 
                WHERE STATUS = 'pending'
            """)
            pending_matches = self.cursor.fetchone()[0]
            
            self.cursor.execute("""
                SELECT COUNT(*) FROM matches 
                WHERE STATUS = 'approved'
            """)
            approved_matches = self.cursor.fetchone()[0]
            
            self.cursor.execute("""
                SELECT COUNT(*) FROM matches 
                WHERE STATUS = 'rejected'
            """)
            rejected_matches = self.cursor.fetchone()[0]
            
            # Update UI labels
            stats = [
                f"Total Lost Reports\n{total_lost}",
                f"Total Found Reports\n{total_found}",
                f"Pending Matches\n{pending_matches}",
                f"Approved Matches\n{approved_matches}",
                f"Rejected Matches\n{rejected_matches}"
            ]
            
            for i, stat in enumerate(stats):
                self.stat_labels[i].config(text=stat)
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load stats:\n{str(e)}")
    
    def load_email_logs(self):
        """Sare emails database se load karo"""
        try:
            # Purane data clear karo
            self.email_tree.delete(*self.email_tree.get_children())
            
            # Database se emails fetch karo
            self.cursor.execute("""
                SELECT LOG_ID, TO_ADDRESS, SUBJECT, 
                    TO_CHAR(SENT_TIME, 'DD-MON-YYYY HH24:MI:SS')
                FROM mail_logs 
                ORDER BY SENT_TIME DESC
            """)
            
            # Treeview mein add karo
            for row in self.cursor:
                self.email_tree.insert('', 'end', values=row)
                
        except Exception as e:
            messagebox.showerror("Error", f"Emails load nahi ho paye:\n{str(e)}")
    def load_user_data(self):
        """Fetches all users from login_users table"""
        try:
            self.user_tree.delete(*self.user_tree.get_children())
            
            self.cursor.execute("""
                SELECT ID, NAME, EMAIL, PHONE, TO_CHAR(LOGIN_TIME, 'DD-MON-YYYY HH24:MI:SS')
                FROM login_users
                ORDER BY LOGIN_TIME DESC
            """)
            
            for row in self.cursor:
                self.user_tree.insert('', 'end', values=row)
        except Exception as e:
            messagebox.showerror("User Load Error", f"Failed to load users:\n{str(e)}")
    def match_items(self):
            """Fixed version handling the FK_ADMIN_EMAIL constraint"""
            try:
                # Get selections
                lost_selection = self.lost_tree.selection()
                found_selection = self.found_tree.selection()
                
                if not lost_selection or not found_selection:
                    messagebox.showwarning("Selection Error", "Please select one lost AND one found item")
                    return
                    
                lost_id = self.lost_tree.item(lost_selection[0])['values'][0]
                found_id = self.found_tree.item(found_selection[0])['values'][0]
                
                # Get a valid admin email (replace with your actual query)
                self.cursor.execute("SELECT email FROM admin_users WHERE ROWNUM = 1")
                admin_email = self.cursor.fetchone()[0]
                
                # Start transaction
                self.conn.begin()
                
                # 1. Verify both items exist and are available
                self.cursor.execute("""
                    SELECT 1 FROM lost_items 
                    WHERE id = :lost_id 
                    AND (matched_item_id IS NULL OR matched_item_id = 0)
                    AND id NOT IN (
                        SELECT lost_id FROM matches 
                        WHERE status = 'approved' AND lost_id IS NOT NULL
                    )
                """, {'lost_id': lost_id})
                if not self.cursor.fetchone():
                    raise ValueError("Lost item is either invalid or already matched")
                    
                self.cursor.execute("""
                    SELECT 1 FROM found_items 
                    WHERE id = :found_id 
                    AND (matched_item_id IS NULL OR matched_item_id = 0)
                    AND id NOT IN (
                        SELECT found_id FROM matches 
                        WHERE status = 'approved' AND found_id IS NOT NULL
                    )
                """, {'found_id': found_id})
                if not self.cursor.fetchone():
                    raise ValueError("Found item is either invalid or already matched")
                    
                # 2. Insert with valid admin email
                self.cursor.execute("""
                    INSERT INTO matches (lost_id, found_id, status, admin_email, match_time)
                    VALUES (:lost_id, :found_id, 'approved', :admin_email, CURRENT_TIMESTAMP)
                """, {
                    'lost_id': lost_id,
                    'found_id': found_id,
                    'admin_email': admin_email  # Now using validated email
                })
                
                # 3. Update original records
                self.cursor.execute("""
                    UPDATE lost_items 
                    SET matched_item_id = :found_id,
                        status = 'matched'
                    WHERE id = :lost_id
                """, {'found_id': found_id, 'lost_id': lost_id})
                
                self.cursor.execute("""
                    UPDATE found_items 
                    SET matched_item_id = :lost_id,
                        status = 'matched'
                    WHERE id = :found_id
                """, {'lost_id': lost_id, 'found_id': found_id})
                
                self.conn.commit()
                messagebox.showinfo("Success", "Items matched successfully!")
                self.load_pending_items()
                self.load_statistics()
                self.send_match_notification(lost_id, found_id)
                
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Matching Error", 
                    f"Failed to match items:\n{str(e)}\n"
                    f"Lost ID: {lost_id}\n"
                    f"Found ID: {found_id}")
    def get_valid_admin_email(self):
        """Returns a valid admin email from database"""
        try:
            self.cursor.execute("""
                SELECT email FROM users 
                WHERE role = 'admin' AND ROWNUM = 1
            """)
            result = self.cursor.fetchone()
            return result[0] if result else "system@default.com"
        except:
            return "system@default.com"
    def send_match_notification(self, lost_id, found_id):
        """Send email notifications for matched items"""
        try:
            # Get user emails and item details
            self.cursor.execute("""
                SELECT USER_EMAIL, ITEM_NAME 
                FROM lost_items 
                WHERE ID = :lost_id
            """, {'lost_id': lost_id})
            lost_user_email, item_name = self.cursor.fetchone()
            
            self.cursor.execute("""
                SELECT USER_EMAIL 
                FROM found_items 
                WHERE ID = :found_id
            """, {'found_id': found_id})
            found_user_email = self.cursor.fetchone()[0]
            
            # Prepare emails
            lost_msg = EmailMessage()
            lost_msg.set_content(f"""
                Your lost item '{item_name}' has been matched with a found item!
                Please contact the finder at: {found_user_email}
            """)
            lost_msg['Subject'] = "Your Lost Item Has Been Matched!"
            lost_msg['From'] = "noreply@lostandfound.com"
            lost_msg['To'] = lost_user_email
            
            found_msg = EmailMessage()
            found_msg.set_content(f"""
                The item you found '{item_name}' has been matched with a lost item!
                The owner may contact you at this email address.
            """)
            found_msg['Subject'] = "Found Item Matched!"
            found_msg['From'] = "noreply@lostandfound.com"
            found_msg['To'] = found_user_email
            
            # Send emails (configure your SMTP settings)
            with smtplib.SMTP('localhost') as server:
                server.send_message(lost_msg)
                server.send_message(found_msg)
            
            # Log emails
            self.log_email(lost_user_email, lost_msg['Subject'], lost_msg.get_content())
            self.log_email(found_user_email, found_msg['Subject'], found_msg.get_content())
            
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send notifications:\n{str(e)}")

    def log_email(self, recipient, subject, body):
        """Log email to database"""
        try:
            self.cursor.execute("""
                INSERT INTO mail_logs (TO_ADDRESS, SUBJECT, BODY)
                VALUES (:recipient, :subject, :body)
            """, {'recipient': recipient, 'subject': subject, 'body': body})
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Failed to log email: {str(e)}")
    
    def search_reports(self):
        """Search reports based on search term"""
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.load_all_reports()
            return
            
        try:
            self.report_tree.delete(*self.report_tree.get_children())
            
            query = """
                SELECT ID, 'Lost', ITEM_NAME, 
                       TO_CHAR(DATE_LOST, 'DD-MON-YYYY'), 
                       LOCATION,
                       TO_CHAR(REPORTED_ON, 'DD-MON-YYYY HH24:MI:SS')
                FROM lost_items 
                WHERE LOWER(ITEM_NAME) LIKE LOWER(:term) OR LOWER(LOCATION) LIKE LOWER(:term)
                UNION ALL
                SELECT ID, 'Found', ITEM_NAME, 
                       TO_CHAR(DATE_FOUND, 'DD-MON-YYYY'), 
                       LOCATION,
                       TO_CHAR(REPORTED_ON, 'DD-MON-YYYY HH24:MI:SS')
                FROM found_items
                WHERE LOWER(ITEM_NAME) LIKE LOWER(:term) OR LOWER(LOCATION) LIKE LOWER(:term)
                ORDER BY 6 DESC
            """
            
            self.cursor.execute(query, {'term': f'%{search_term}%'})
            for row in self.cursor:
                self.report_tree.insert('', 'end', values=row)
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search reports:\n{str(e)}")
    
    def approve_report(self):
        """Approve selected report"""
        self.update_report_status('approved')
    
    def reject_report(self):
        """Reject selected report"""
        self.update_report_status('rejected')
    def show_item_details(self, event):
        """Guaranteed to show image and description from database"""
        selected = self.report_tree.focus()
        if not selected:
            return
        
        item_data = self.report_tree.item(selected)
        item_id = item_data['values'][0]
        item_type = item_data['values'][1].lower()  # 'lost' or 'found'
        
        try:
            # Fetch description and image from database
            self.cursor.execute(f"""
                SELECT description, item_image 
                FROM {item_type}_items 
                WHERE id = :id
            """, {'id': item_id})
            
            result = self.cursor.fetchone()
            
            # Update description
            description = result[0] if result and result[0] else "No description available"
            self.detail_desc.config(state=tk.NORMAL)
            self.detail_desc.delete('1.0', tk.END)
            self.detail_desc.insert('1.0', description)
            self.detail_desc.config(state=tk.DISABLED)
            
            # Update image
            if result and result[1]:  # If image exists
                try:
                    # For Oracle BLOB data
                    blob_data = result[1].read()
                    image = Image.open(io.BytesIO(blob_data))
                    image.thumbnail((300, 300))
                    photo = ImageTk.PhotoImage(image)
                    
                    self.detail_image.config(image=photo, text="")
                    self.detail_image.image = photo  # Keep reference
                except Exception as img_error:
                    print(f"Image error: {img_error}")
                    self.detail_image.config(
                        image=None,
                        text="Image format not supported"
                    )
            else:
                self.detail_image.config(
                    image=None,
                    text="No image available"
                )
                
        except Exception as e:
            print(f"Database error: {e}")
            self.detail_desc.config(state=tk.NORMAL)
            self.detail_desc.delete('1.0', tk.END)
            self.detail_desc.insert('1.0', "Error loading details")
            self.detail_desc.config(state=tk.DISABLED)
            self.detail_image.config(
                image=None,
                text="Error loading image"
            )
    def show_selected_item_image(self, event):
        """Show image when item is selected"""
        selected = self.report_tree.focus()
        if not selected:
            return
        
        item_data = self.report_tree.item(selected)
        item_id = item_data['values'][0]
        item_type = item_data['values'][1].lower()  # 'lost' or 'found'
        
        try:
            # Check if image exists
            self.cursor.execute(f"""
                SELECT item_image FROM {item_type}_items 
                WHERE id = :id AND item_image IS NOT NULL
            """, {'id': item_id})
            blob_data = self.cursor.fetchone()
            
            if blob_data and blob_data[0]:
                # Read BLOB data
                image = Image.open(io.BytesIO(blob_data[0].read()))
                image.thumbnail((280, 280))  # Resize
                
                # Display image
                photo = ImageTk.PhotoImage(image)
                self.img_label.config(image=photo, text="")
                self.img_label.image = photo  # Keep reference
            else:
                self.img_label.config(image=None, text="No image available")
                
        except Exception as e:
            print(f"Error loading image: {e}")
            self.img_label.config(image=None, text="Error loading image")
    def delete_selected_user(self):
        """Delete selected user from login_users table"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a user to delete.")
            return

        user_id = self.user_tree.item(selection[0])['values'][0]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete user ID {user_id}?")
        if not confirm:
            return

        try:
            self.cursor.execute("DELETE FROM login_users WHERE ID = :id", {'id': user_id})
            self.conn.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            self.load_user_data()  # Refresh the table
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Delete Error", f"Failed to delete user:\n{str(e)}")
    def edit_selected_user(self):
        """Open edit popup for selected user"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a user to edit.")
            return

        user_data = self.user_tree.item(selection[0])['values']
        user_id, name, email, phone, _ = user_data

        edit_win = tk.Toplevel(self.master)
        edit_win.title("Edit User Info")
        edit_win.geometry("400x300")

        # Form
        tk.Label(edit_win, text="Name:").pack(pady=(10,0))
        name_entry = ttk.Entry(edit_win)
        name_entry.insert(0, name)
        name_entry.pack(fill=tk.X, padx=10)

        tk.Label(edit_win, text="Email:").pack(pady=(10,0))
        email_entry = ttk.Entry(edit_win)
        email_entry.insert(0, email)
        email_entry.pack(fill=tk.X, padx=10)

        tk.Label(edit_win, text="Phone:").pack(pady=(10,0))
        phone_entry = ttk.Entry(edit_win)
        phone_entry.insert(0, phone)
        phone_entry.pack(fill=tk.X, padx=10)

        def save_changes():
            try:
                self.cursor.execute("""
                    UPDATE login_users
                    SET NAME = :name, EMAIL = :email, PHONE = :phone
                    WHERE ID = :id
                """, {
                    'name': name_entry.get(),
                    'email': email_entry.get(),
                    'phone': phone_entry.get(),
                    'id': user_id
                })
                self.conn.commit()
                messagebox.showinfo("Success", "User updated successfully.")
                edit_win.destroy()
                self.load_user_data()
            except Exception as e:
                self.conn.rollback()
                messagebox.showerror("Update Error", f"Failed to update user:\n{str(e)}")

        ttk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=20)

    def update_report_status(self, status):
        """Generic method to update report status"""
        selection = self.report_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a report first")
            return
            
        item_id = self.report_tree.item(selection[0])['values'][0]
        report_type = self.report_tree.item(selection[0])['values'][1]
        
        try:
            table = 'lost_items' if report_type == 'Lost' else 'found_items'
            self.cursor.execute(f"""
                UPDATE {table} 
                SET status = :status 
                WHERE ID = :item_id
            """, {'status': status, 'item_id': item_id})
            
            self.conn.commit()
            messagebox.showinfo("Success", f"Report {status} successfully!")
            self.load_all_reports()
            self.load_statistics()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Database Error", f"Failed to update status:\n{str(e)}")
    
    def edit_report(self):
        """Edit selected report"""
        selection = self.report_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a report first")
            return
            
        item_id = self.report_tree.item(selection[0])['values'][0]
        report_type = self.report_tree.item(selection[0])['values'][1]
        
        # Create edit window
        edit_win = tk.Toplevel(self.master)
        edit_win.title(f"Edit {report_type} Report")
        edit_win.geometry("400x300")
        
        # Get current item details
        try:
            table = 'lost_items' if report_type == 'Lost' else 'found_items'
            date_col = 'DATE_LOST' if report_type == 'Lost' else 'DATE_FOUND'
            
            self.cursor.execute(f"""
                SELECT ITEM_NAME, DESCRIPTION, {date_col}, LOCATION 
                FROM {table} WHERE ID = :item_id
            """, {'item_id': item_id})
            item_data = self.cursor.fetchone()
            
            # Form fields
            tk.Label(edit_win, text="Item Name:").pack(pady=(10,0))
            name_entry = ttk.Entry(edit_win)
            name_entry.insert(0, item_data[0])
            name_entry.pack(fill=tk.X, padx=10)
            
            tk.Label(edit_win, text="Description:").pack(pady=(10,0))
            desc_entry = tk.Text(edit_win, height=5)
            desc_entry.insert('1.0', item_data[1] if item_data[1] else '')
            desc_entry.pack(fill=tk.X, padx=10)
            
            tk.Label(edit_win, text="Date:").pack(pady=(10,0))
            date_entry = ttk.Entry(edit_win)
            date_entry.insert(0, item_data[2].strftime('%Y-%m-%d') if item_data[2] else '')
            date_entry.pack(fill=tk.X, padx=10)
            
            tk.Label(edit_win, text="Location:").pack(pady=(10,0))
            loc_entry = ttk.Entry(edit_win)
            loc_entry.insert(0, item_data[3] if item_data[3] else '')
            loc_entry.pack(fill=tk.X, padx=10)
            
            def save_changes():
                try:
                    self.cursor.execute(f"""
                        UPDATE {table} 
                        SET ITEM_NAME = :name,
                            DESCRIPTION = :desc,
                            {date_col} = TO_DATE(:date, 'YYYY-MM-DD'),
                            LOCATION = :loc
                        WHERE ID = :item_id
                    """, {
                        'name': name_entry.get(),
                        'desc': desc_entry.get('1.0', tk.END).strip(),
                        'date': date_entry.get(),
                        'loc': loc_entry.get(),
                        'item_id': item_id
                    })
                    self.conn.commit()
                    messagebox.showinfo("Success", "Report updated successfully!")
                    edit_win.destroy()
                    self.load_all_reports()
                except Exception as e:
                    self.conn.rollback()
                    messagebox.showerror("Error", f"Failed to update report:\n{str(e)}")
            
            ttk.Button(
                edit_win,
                text="Save Changes",
                command=save_changes
            ).pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report details:\n{str(e)}")
            edit_win.destroy()
    def send_email_to_user(self):
        """Open popup to send email to selected user"""
        selection = self.user_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a user to email.")
            return

        user_data = self.user_tree.item(selection[0])['values']
        recipient_email = user_data[2]  # Email column

        win = tk.Toplevel(self.master)
        win.title("Send Email to User")
        win.geometry("500x400")

        # Subject
        tk.Label(win, text="Subject:").pack(pady=(10, 0))
        subject_entry = ttk.Entry(win)
        subject_entry.pack(fill=tk.X, padx=10)

        # Message
        tk.Label(win, text="Message:").pack(pady=(10, 0))
        message_text = tk.Text(win, height=12)
        message_text.pack(fill=tk.BOTH, expand=True, padx=10)

        def send():
            subject = subject_entry.get().strip()
            body = message_text.get("1.0", tk.END).strip()

            if not subject or not body:
                messagebox.showwarning("Validation Error", "Subject and message cannot be empty.")
                return

            try:
                # (1) Prepare email
                msg = EmailMessage()
                msg.set_content(body)
                msg['Subject'] = subject
                msg['From'] = "noreeynoor@gmail.com"
                msg['To'] = recipient_email

                # (2) Send email (original functionality remains)
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login("noreeynoor@gmail.com", "fpzbvlwykiiomdjg")
                    server.send_message(msg)

                # (3) Log to database (NEW but safe)
                self.log_email(recipient_email, subject, body)
                
                # (4) Refresh email logs display
                self.load_email_logs()

                # (5) Show success and close window
                messagebox.showinfo("Success", "Email sent successfully!")
                win.destroy()

            except smtplib.SMTPAuthenticationError:
                messagebox.showerror("Error", "Email login failed. Check credentials.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to send email: {str(e)}")

        ttk.Button(win, text="Send Email", command=send).pack(pady=10)
    def delete_report(self):
        """Delete selected report"""
        selection = self.report_tree.selection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a report first")
            return
            
        item_id = self.report_tree.item(selection[0])['values'][0]
        report_type = self.report_tree.item(selection[0])['values'][1]
        
        if not messagebox.askyesno("Confirm", f"Delete this {report_type} report permanently?"):
            return
            
        try:
            table = 'lost_items' if report_type == 'Lost' else 'found_items'
            self.cursor.execute(f"""
                DELETE FROM {table} 
                WHERE ID = :item_id
            """, {'item_id': item_id})
            
            self.conn.commit()
            messagebox.showinfo("Success", "Report deleted successfully!")
            self.load_all_reports()
            self.load_statistics()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Database Error", f"Failed to delete report:\n{str(e)}")
    
    def export_emails(self):
        """Export email logs to CSV"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                title="Save Email Logs"
            )
            
            if not file_path:
                return
                
            self.cursor.execute("""
                SELECT TO_ADDRESS, SUBJECT, 
                       TO_CHAR(SENT_TIME, 'DD-MON-YYYY HH24:MI:SS')
                FROM mail_logs ORDER BY SENT_TIME DESC
            """)
            
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Recipient', 'Subject', 'Timestamp'])
                writer.writerows(self.cursor)
                
            messagebox.showinfo("Success", f"Email logs exported to:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export emails:\n{str(e)}")
    
    def reject_match(self):
        """Reject selected match"""
        lost_selection = self.lost_tree.selection()
        found_selection = self.found_tree.selection()
        
        if not lost_selection and not found_selection:
            messagebox.showwarning("Selection Error", "Please select at least one item")
            return
            
        try:
            # Reject selected lost items
            if lost_selection:
                lost_id = self.lost_tree.item(lost_selection[0])['values'][0]
                self.cursor.execute("""
                    INSERT INTO matches (LOST_ID, FOUND_ID, STATUS, ADMIN_EMAIL)
                    VALUES (:lost_id, NULL, 'rejected', 'admin@system')
                """, {'lost_id': lost_id})
            
            # Reject selected found items
            if found_selection:
                found_id = self.found_tree.item(found_selection[0])['values'][0]
                self.cursor.execute("""
                    INSERT INTO matches (LOST_ID, FOUND_ID, STATUS, ADMIN_EMAIL)
                    VALUES (NULL, :found_id, 'rejected', 'admin@system')
                """, {'found_id': found_id})
            
            self.conn.commit()
            messagebox.showinfo("Success", "Items rejected successfully!")
            self.load_pending_items()
            self.load_statistics()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Database Error", f"Failed to reject items:\n{str(e)}")
    
    def logout(self):
        """Return to login screen"""
        self.on_close()
        self.return_to_login.deiconify()
    
    def on_close(self):
        """Clean up resources before closing"""
        if hasattr(self, 'cursor'):
            self.cursor.close()
        if hasattr(self, 'conn'):
            self.conn.close()
        self.master.destroy()
    
    def __del__(self):
        """Destructor for cleanup"""
        self.on_close()