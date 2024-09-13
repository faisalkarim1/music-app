import tkinter as tk
import pygame
from tkinter import filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")

        # Create buttons
        self.play_button = tk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=5)

        # Create progress bar
        self.progress_bar = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
        self.progress_bar.pack(pady=10)
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0)

        # Initialize variables
        self.music_path = None
        self.is_playing = False

    def browse_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav;*.ogg")])
        if file_path:
            self.music_path = file_path
            self.play_music()

    def play_music(self):
        if self.music_path:
            if not self.is_playing:
                pygame.mixer.init()
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play()

                self.is_playing = True
                self.play_button.config(text="Pause")
                self.stop_button.config(state=tk.NORMAL)  # Enable stop button
                self.update_progress()

    def stop_music(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            self.is_playing = False
            self.play_button.config(text="Play")
            self.stop_button.config(state=tk.DISABLED)  # Disable stop button
            self.progress_var.set(0)  # Reset progress bar

    def update_progress(self):
        if self.is_playing:
            music_length = pygame.mixer.music.get_length()
            current_position = pygame.mixer.music.get_pos()
            progress = (current_position / music_length) * 100 if music_length else 0

            self.progress_var.set(progress)
            self.progress_bar.set(progress)

            self.root.after(100, self.update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Music Player")

    music_player = MusicPlayer(root)

    browse_button = tk.Button(root, text="Browse Music", command=music_player.browse_music)
    browse_button.pack(pady=10)

    root.mainloop()