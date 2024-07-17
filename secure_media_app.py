import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import vlc
from encryption_utils import encrypt_file, decrypt_file

class SecureMediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Media App")
        self.root.geometry("1000x600")  # Set initial window size
        
        self.password = tk.StringVar()

        # Left Panel for Encryption Options
        self.left_panel = tk.Frame(root, width=200, bg="#f0f0f0")
        self.left_panel.pack(side=tk.LEFT, fill=tk.Y)

        self.label = tk.Label(self.left_panel, text="Enter Password", font=("Arial", 12), bg="#f0f0f0")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.left_panel, textvariable=self.password, show='*', font=("Arial", 12), width=20)
        self.entry.pack(pady=10)

        self.encrypt_video_button = tk.Button(self.left_panel, text="Encrypt Video File", command=self.encrypt_video_file,
                                              font=("Arial", 12), bg="#4CAF50", fg="white")
        self.encrypt_video_button.pack(pady=10, fill=tk.X)

        self.decrypt_video_button = tk.Button(self.left_panel, text="Decrypt and Play Video File",
                                              command=self.decrypt_and_play_video_file, font=("Arial", 12),
                                              bg="#2196F3", fg="white")
        self.decrypt_video_button.pack(pady=10, fill=tk.X)

        self.encrypt_image_button = tk.Button(self.left_panel, text="Encrypt Image File", command=self.encrypt_image_file,
                                              font=("Arial", 12), bg="#4CAF50", fg="white")
        self.encrypt_image_button.pack(pady=10, fill=tk.X)

        self.decrypt_image_button = tk.Button(self.left_panel, text="Decrypt and View Image File",
                                              command=self.decrypt_and_view_image_file, font=("Arial", 12),
                                              bg="#2196F3", fg="white")
        self.decrypt_image_button.pack(pady=10, fill=tk.X)

        # Right Panel for Media Display
        self.right_panel = tk.Frame(root, bg="black")
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.media_display_frame = tk.Frame(self.right_panel, bg="black")
        self.media_display_frame.pack(expand=True, fill=tk.BOTH)

        self.media_label = tk.Label(self.media_display_frame, bg="black")
        self.media_label.pack(expand=True, fill=tk.BOTH)

        # Control Frame for Media Player Buttons
        self.control_frame = tk.Frame(self.right_panel, bg="#333333")
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_media, font=("Arial", 12),
                                     bg="#FF9800", fg="white")
        self.play_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause_media, font=("Arial", 12),
                                      bg="#FF9800", fg="white")
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.forward_button = tk.Button(self.control_frame, text="Forward 10s", command=self.forward_media,
                                        font=("Arial", 12), bg="#FF9800", fg="white")
        self.forward_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.backward_button = tk.Button(self.control_frame, text="Backward 10s", command=self.backward_media,
                                         font=("Arial", 12), bg="#FF9800", fg="white")
        self.backward_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.mute_button = tk.Button(self.control_frame, text="Mute", command=self.mute_media, font=("Arial", 12),
                                     bg="#FF9800", fg="white")
        self.mute_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.unmute_button = tk.Button(self.control_frame, text="Unmute", command=self.unmute_media, font=("Arial", 12),
                                       bg="#FF9800", fg="white")
        self.unmute_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.close_button = tk.Button(self.control_frame, text="Close Media", command=self.close_media,
                                      font=("Arial", 12), bg="#F44336", fg="white")
        self.close_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.media_player = vlc.MediaPlayer()

        self.root.bind("<Configure>", self.resize_media)

        self.decrypted_image_path = None
        self.current_media = None

    def encrypt_video_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
        if not file_path:
            return
        if not self.password.get():
            messagebox.showwarning("Password Required", "Please enter a password to encrypt the file.")
            return
        try:
            encrypt_file(file_path, self.password.get())
            messagebox.showinfo("Success", "Video file encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt_and_play_video_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if not file_path:
            return
        if not self.password.get():
            messagebox.showwarning("Password Required", "Please enter a password to decrypt the file.")
            return
        try:
            decrypted_path = decrypt_file(file_path, self.password.get())
            if decrypted_path:
                self.play_media(decrypted_path)
            else:
                messagebox.showerror("Decryption Failed", "Incorrect password or corrupted file.")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

    def encrypt_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return
        if not self.password.get():
            messagebox.showwarning("Password Required", "Please enter a password to encrypt the file.")
            return
        try:
            encrypt_file(file_path, self.password.get())
            messagebox.showinfo("Success", "Image file encrypted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Encryption failed: {e}")

    def decrypt_and_view_image_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
        if not file_path:
            return
        if not self.password.get():
            messagebox.showwarning("Password Required", "Please enter a password to decrypt the file.")
            return
        try:
            self.decrypted_image_path = decrypt_file(file_path, self.password.get())
            if self.decrypted_image_path:
                self.display_image(self.decrypted_image_path)
            else:
                messagebox.showerror("Decryption Failed", "Incorrect password or corrupted file.")
        except Exception as e:
            messagebox.showerror("Error", f"Decryption failed: {e}")

    def display_image(self, image_path):
        image = Image.open(image_path)
        self.current_media = image
        self.display_media()

    def display_video(self, video_path):
        self.current_media = vlc.Media(video_path)
        self.display_media()

    def display_media(self):
        if isinstance(self.current_media, Image.Image):
            self.media_label.config(image=None)  # Clear previous video display
            self.photo_image = ImageTk.PhotoImage(self.current_media)
            self.media_label.config(image=self.photo_image)
        elif isinstance(self.current_media, vlc.Media):
            self.media_player.set_media(self.current_media)
            self.media_player.set_hwnd(self.media_label.winfo_id())
            self.media_player.play()

    def resize_media(self, event):
        if self.current_media and isinstance(self.current_media, Image.Image):
            self.display_media()  # Refresh image display on resize

    def play_media(self, media_path=None):
        if media_path:
            self.current_media = vlc.Media(media_path)
            self.display_media()
        elif isinstance(self.current_media, vlc.Media):
            self.media_player.play()

    def pause_media(self):
        self.media_player.pause()

    def forward_media(self):
        current_time = self.media_player.get_time()
        self.media_player.set_time(current_time + 10000)  # Forward 10 seconds

    def backward_media(self):
        current_time = self.media_player.get_time()
        self.media_player.set_time(max(0, current_time - 10000))  # Backward 10 seconds

    def mute_media(self):
        self.media_player.audio_set_mute(True)

    def unmute_media(self):
        self.media_player.audio_set_mute(False)

    def close_media(self):
        self.media_player.stop()
        self.current_media = None
        self.media_label.config(image=None)

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureMediaApp(root)
    root.mainloop()
