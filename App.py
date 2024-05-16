import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
import cv2
from pytube import YouTube
import os

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('YouTube Video Frame Extractor')

        # Set window size and position
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Create a frame for the GUI elements
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create entry for YouTube URL
        self.url_label = ttk.Label(self.frame, text="Enter YouTube URL:")
        self.url_label.pack(pady=5)
        self.url_entry = ttk.Entry(self.frame, width=50)
        self.url_entry.pack(pady=5)

        # Create entry for folder name
        self.folder_label = ttk.Label(self.frame, text="Enter folder name:")
        self.folder_label.pack(pady=5)
        self.folder_entry = ttk.Entry(self.frame, width=50)
        self.folder_entry.pack(pady=5)

        # Create button to extract frames
        self.extract_button = ttk.Button(self.frame, text="Extract Frames", command=self.extract_frames)
        self.extract_button.pack(pady=5)

        # Create a frame for displaying frames
        self.display_frame = tk.Frame(self.frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create canvas and scrollbars for displaying frames
        self.canvas = tk.Canvas(self.display_frame, bg='black')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.h_scrollbar = tk.Scrollbar(self.display_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scrollbar = tk.Scrollbar(self.display_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.root.mainloop()

    def extract_frames(self):
        # Get YouTube URL from the entry
        url = self.url_entry.get()
        folder_name = self.folder_entry.get()

        try:
            # Download the YouTube video
            yt = YouTube(url)
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            video_path = video.download()

            # Specify the directory path to save frames
            output_dir = os.path.join("D:\Youtube frames", folder_name)  # Change this to your desired directory path

            # Create the directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)

            # Read video using OpenCV
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Error opening video stream")

            # Extract frames and save them as image files
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Save frame as image file with highest quality
                frame_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
                cv2.imwrite(frame_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

                frame_count += 1

            # Display frames in canvas
            for i in range(frame_count):
                frame_path = os.path.join(output_dir, f"frame_{i}.jpg")
                frame_img = Image.open(frame_path)
                frame_img = ImageTk.PhotoImage(frame_img)
                self.canvas.create_image(i * frame_img.width(), 0, anchor=tk.NW, image=frame_img)

            # Release the video capture object
            cap.release()

        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == '__main__':
    App()
