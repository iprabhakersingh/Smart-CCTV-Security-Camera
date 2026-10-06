import tkinter as tk
from tkinter import messagebox, font
from PIL import Image, ImageTk
import time
from in_out import in_out
from motion import noise
from rect_noise import rect_noise
from record import record
from find_motion import find_motion
from identify import maincall

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

# Modern color scheme
COLORS = {
    'dark_bg': '#1e1e2d',
    'darker_bg': '#161622',
    'accent': '#4e7cff',
    'light_accent': '#6d8eff',
    'text': '#ffffff',
    'secondary_text': '#b8b8b8',
    'card_bg': '#2a2a3a',
    'success': '#4caf50',
    'error': '#f44336'
}

# Animation settings
ANIMATION_SPEED = 0.15  # seconds for animations

class SmoothButton(tk.Button):
    """Custom button class with smooth hover effects"""
    def __init__(self, master=None, **kwargs):
        self.default_bg = kwargs.pop('bg', COLORS['card_bg'])
        self.hover_bg = kwargs.pop('hover_bg', COLORS['accent'])
        self.active_bg = kwargs.pop('active_bg', COLORS['light_accent'])
        
        super().__init__(master, **kwargs)
        
        self['bg'] = self.default_bg
        self['fg'] = COLORS['text']
        self['borderwidth'] = 0
        self['relief'] = 'flat'
        self['activebackground'] = self.active_bg
        self['activeforeground'] = COLORS['text']
        
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        
    def on_enter(self, e):
        self['bg'] = self.hover_bg
        self.animate_scale(1.05)
        
    def on_leave(self, e):
        self['bg'] = self.default_bg
        self.animate_scale(1.0)
        
    def animate_scale(self, target_scale):
        current_scale = float(self['width']) / 160  # 160 is default width
        steps = 10
        delay = int(ANIMATION_SPEED * 1000 / steps)
        
        for i in range(steps + 1):
            scale = current_scale + (target_scale - current_scale) * (i / steps)
            new_width = int(160 * scale)
            new_height = int(80 * scale)
            self.after(i * delay, lambda w=new_width, h=new_height: 
                       self.config(width=w, height=h))

def validate_login():
    """Validate admin credentials with smooth transition"""
    username = entry_username.get()
    password = entry_password.get()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Animate login window closing
        for i in range(10, 0, -1):
            alpha = i/10
            login_window.attributes('-alpha', alpha)
            login_window.update()
            time.sleep(ANIMATION_SPEED/10)
        
        login_window.destroy()
        open_main_application()
    else:
        # Shake animation for invalid login
        x = login_window.winfo_x()
        for _ in range(3):
            for dx in [10, -10, 10, -10, 0]:
                login_window.geometry(f"+{x + dx}+{login_window.winfo_y()}")
                login_window.update()
                time.sleep(0.03)
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_application():
    """Main application window with modern UI"""
    main_window = tk.Tk()
    main_window.title("Smart AI CCTV Control Panel")
    main_window.iconphoto(False, tk.PhotoImage(file='mn.png'))
    main_window.geometry('1280x720')
    main_window.configure(bg=COLORS['dark_bg'])
    main_window.attributes('-alpha', 0)  # Start transparent for fade-in
    
    # Fade in animation
    for i in range(1, 11):
        alpha = i/10
        main_window.attributes('-alpha', alpha)
        main_window.update()
        time.sleep(ANIMATION_SPEED/10)
    
    # Header frame
    header_frame = tk.Frame(main_window, bg=COLORS['darker_bg'])
    header_frame.pack(fill='x', padx=10, pady=10)
    
    # App title with subtle shadow
    title_font = font.Font(size=24, weight='bold', family='Segoe UI')
    title_label = tk.Label(
        header_frame, 
        text="Smart AI CCTV Control Panel", 
        bg=COLORS['darker_bg'], 
        fg=COLORS['text'],
        font=title_font
    )
    title_label.pack(side='left', padx=20, pady=15)
    
    # Status bar
    status_var = tk.StringVar(value="System Ready")
    status_bar = tk.Label(
        header_frame, 
        textvariable=status_var,
        bg=COLORS['darker_bg'], 
        fg=COLORS['secondary_text'],
        font=('Segoe UI', 10)
    )
    status_bar.pack(side='right', padx=20)
    
    # Main content area
    content_frame = tk.Frame(main_window, bg=COLORS['dark_bg'])
    content_frame.pack(expand=True, fill='both', padx=20, pady=(0, 20))
    
    # Load button icons
    def load_icon(path, size=(40, 40)):
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    
    icons = {
        'monitor': load_icon('icons/lamp.png'),
        'rectangle': load_icon('icons/rectangle-of-cutted-line-geometrical-shape.png'),
        'noise': load_icon('icons/security-camera.png'),
        'record': load_icon('icons/recording.png'),
        'exit': load_icon('icons/exit.png'),
        'in_out': load_icon('icons/incognito.png'),
        'identify': load_icon('icons/identify.png')
    }
    
    # Button descriptions
    buttons = [
        {'text': 'Motion Monitor', 'icon': icons['monitor'], 'command': find_motion, 
         'description': 'Monitor for motion detection and alerts'},
        {'text': 'Rectangle Zone', 'icon': icons['rectangle'], 'command': rect_noise, 
         'description': 'Define rectangular monitoring zones'},
        {'text': 'Noise Detection', 'icon': icons['noise'], 'command': noise, 
         'description': 'Detect and analyze audio anomalies'},
        {'text': 'Record Feed', 'icon': icons['record'], 'command': record, 
         'description': 'Start/stop video recording'},
        {'text': 'Entry/Exit Logs', 'icon': icons['in_out'], 'command': in_out, 
         'description': 'View people entry and exit records'},
        {'text': 'Identify Faces', 'icon': icons['identify'], 'command': maincall, 
         'description': 'Run facial recognition system'},
        {'text': 'Exit System', 'icon': icons['exit'], 'command': main_window.quit, 
         'description': 'Safely close the application'}
    ]
    
    # Create a grid of feature cards
    for i, btn in enumerate(buttons):
        # Card frame
        card = tk.Frame(
            content_frame, 
            bg=COLORS['card_bg'],
            highlightbackground=COLORS['accent'],
            highlightthickness=0,
            bd=0,
            relief='raised'
        )
        card.grid(row=i//3, column=i%3, padx=15, pady=15, sticky='nsew')
        content_frame.grid_columnconfigure(i%3, weight=1)
        
        # Button with icon and text
        button = SmoothButton(
            card,
            text=f"  {btn['text']}",
            image=btn['icon'],
            compound='left',
            command=btn['command'],
            bg=COLORS['card_bg'],
            hover_bg=COLORS['accent'],
            font=('Segoe UI', 12, 'bold')
        )
        button.pack(fill='x', padx=10, pady=(10, 5))
        
        # Description label
        desc = tk.Label(
            card,
            text=btn['description'],
            bg=COLORS['card_bg'],
            fg=COLORS['secondary_text'],
            font=('Segoe UI', 9),
            wraplength=200,
            justify='left'
        )
        desc.pack(fill='x', padx=10, pady=(0, 10))
        
        # Add subtle animation to cards
        card.bind('<Enter>', lambda e, c=card: e.widget.config(highlightthickness=1))
        card.bind('<Leave>', lambda e, c=card: e.widget.config(highlightthickness=0))
    
    # Configure rows and columns for responsive layout
    for i in range((len(buttons)+2)//3):
        content_frame.grid_rowconfigure(i, weight=1)
    
    # Footer
    footer = tk.Frame(main_window, bg=COLORS['darker_bg'], height=30)
    footer.pack(fill='x', side='bottom', padx=10, pady=(0, 10))
    
    # Copyright label
    tk.Label(
        footer,
        text="© 2023 Smart AI CCTV System | Version 2.0",
        bg=COLORS['darker_bg'],
        fg=COLORS['secondary_text'],
        font=('Segoe UI', 8)
    ).pack(side='right', padx=20)
    
    # System time display
    time_var = tk.StringVar()
    time_label = tk.Label(
        footer,
        textvariable=time_var,
        bg=COLORS['darker_bg'],
        fg=COLORS['secondary_text'],
        font=('Segoe UI', 8)
    )
    time_label.pack(side='left', padx=20)
    
    def update_time():
        """Update the time display every second"""
        time_var.set(time.strftime('%Y-%m-%d %H:%M:%S'))
        main_window.after(1000, update_time)
    
    update_time()
    
    # Handle window closing
    def on_closing():
        """Smooth fade-out animation when closing"""
        for i in range(10, 0, -1):
            alpha = i/10
            main_window.attributes('-alpha', alpha)
            main_window.update()
            time.sleep(ANIMATION_SPEED/10)
        main_window.destroy()
    
    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.mainloop()

# Create the login window with modern styling
login_window = tk.Tk()
login_window.title("Secure Login - AI CCTV System")
login_window.geometry('400x500')
login_window.configure(bg=COLORS['dark_bg'])
login_window.resizable(False, False)

# Center the window
screen_width = login_window.winfo_screenwidth()
screen_height = login_window.winfo_screenheight()
x = (screen_width - 400) // 2
y = (screen_height - 500) // 2
login_window.geometry(f'+{x}+{y}')

# Login container
login_container = tk.Frame(login_window, bg=COLORS['dark_bg'])
login_container.pack(expand=True, fill='both', padx=40, pady=60)

# App logo/icon
logo_img = Image.open('mn.png').resize((120, 120), Image.Resampling.LANCZOS)
logo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(login_container, image=logo, bg=COLORS['dark_bg'])
logo_label.pack(pady=(0, 30))

# Login title
login_title = tk.Label(
    login_container,
    text="SECURE LOGIN",
    bg=COLORS['dark_bg'],
    fg=COLORS['text'],
    font=('Segoe UI', 18, 'bold')
)
login_title.pack(pady=(0, 30))

# Username field
username_frame = tk.Frame(login_container, bg=COLORS['dark_bg'])
username_frame.pack(fill='x', pady=(0, 15))

tk.Label(
    username_frame,
    text="Username:",
    bg=COLORS['dark_bg'],
    fg=COLORS['text'],
    font=('Segoe UI', 10),
    anchor='w'
).pack(fill='x')

entry_username = tk.Entry(
    username_frame,
    bg=COLORS['card_bg'],
    fg=COLORS['text'],
    insertbackground=COLORS['text'],
    relief='flat',
    font=('Segoe UI', 11),
    bd=0,
    highlightthickness=1,
    highlightcolor=COLORS['accent'],
    highlightbackground='#555555'
)
entry_username.pack(fill='x', ipady=5)

# Password field
password_frame = tk.Frame(login_container, bg=COLORS['dark_bg'])
password_frame.pack(fill='x', pady=(0, 30))

tk.Label(
    password_frame,
    text="Password:",
    bg=COLORS['dark_bg'],
    fg=COLORS['text'],
    font=('Segoe UI', 10),
    anchor='w'
).pack(fill='x')

entry_password = tk.Entry(
    password_frame,
    bg=COLORS['card_bg'],
    fg=COLORS['text'],
    show='•',
    insertbackground=COLORS['text'],
    relief='flat',
    font=('Segoe UI', 11),
    bd=0,
    highlightthickness=1,
    highlightcolor=COLORS['accent'],
    highlightbackground='#555555'
)
entry_password.pack(fill='x', ipady=5)

# Login button
login_btn = SmoothButton(
    login_container,
    text="LOGIN",
    command=validate_login,
    bg=COLORS['accent'],
    hover_bg=COLORS['light_accent'],
    active_bg=COLORS['light_accent'],
    font=('Segoe UI', 12, 'bold'),
    width=20
)
login_btn.pack(pady=(10, 0))

# Bind Enter key to login
entry_password.bind('<Return>', lambda e: validate_login())

# Focus username field by default
entry_username.focus_set()

login_window.mainloop()