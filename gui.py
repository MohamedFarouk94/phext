import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser

from phext import PhextSearcher


class PhextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Search Your Gallery with Text")
        self.root.geometry("900x900")
        self.root.configure(bg="white")

        self.searcher = None
        self.image_path = None
        self.loaded_images = {}

        self._build_ui()

    def _build_ui(self):
        # --- Banner with logo and title ---
        banner_frame = tk.Frame(self.root, bg="white")
        banner_frame.pack(pady=10, fill="x")

        try:
            logo_img = Image.open("logo.png").resize((80, 80), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(banner_frame, image=self.logo, bg="white")
            logo_label.pack(side="left", padx=100)
        except Exception:
            logo_label = tk.Label(banner_frame, text="[Logo]", font=("Arial", 20), bg="white")
            logo_label.pack(side="left", padx=100)

        title_label = tk.Label(
            banner_frame,
            text="Search your gallery with text!",
            font=("Arial", 20, "bold"),
            bg="white",
        )
        title_label.pack(side="left", padx=10)

        # --- Path chooser ---
        path_frame = tk.Frame(self.root, bg="white")
        path_frame.pack(pady=10, fill="x")

        self.path_entry = tk.Entry(path_frame, width=50, font=("Arial", 12))
        self.path_entry.pack(side="left", padx=50)

        browse_btn = tk.Button(
            path_frame,
            text="Browse",
            command=self.browse_folder,
            font=("Arial", 12),
            bg="#f0f0f0",
        )
        browse_btn.pack(side="left", padx=5)

        fit_btn = tk.Button(
            path_frame,
            text="Load Gallery",
            command=self.load_gallery,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
        )
        fit_btn.pack(side="left", padx=5)

        # --- Search bar ---
        search_frame = tk.Frame(self.root, bg="white")
        search_frame.pack(pady=10, fill="x")

        self.search_entry = tk.Entry(search_frame, width=50, font=("Arial", 14))
        self.search_entry.pack(side="left", padx=80)

        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=self.run_search,
            font=("Arial", 12, "bold"),
            bg="#2196F3",
            fg="white",
        )
        search_btn.pack(side="left", padx=5)

        # --- Result area ---
        self.result_frame = tk.Frame(self.root, bg="white")
        self.result_frame.pack(pady=20, fill="both", expand=True)

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def load_gallery(self):
        path = self.path_entry.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Error", "Please select a valid folder.")
            return

        self.searcher = PhextSearcher(path)
        self.searcher.fit()
        self.image_path = path
        messagebox.showinfo("Gallery Loaded", "Image gallery loaded successfully!")

    def run_search(self):
        if not self.searcher:
            messagebox.showerror("Error", "Please load a gallery first.")
            return

        query = self.search_entry.get().strip()
        if not query:
            messagebox.showerror("Error", "Please enter a search query.")
            return

        best_fit, results = self.searcher.search(query, N=5)
        self.display_results(best_fit, results)

    def display_results(self, best_fit, results):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not results:
            tk.Label(
                self.result_frame,
                text="No results found.",
                font=("Arial", 14),
                bg="white",
            ).pack()
            return

        # --- Best match (big image) ---
        best_img_path = os.path.join(self.image_path, best_fit)
        self.show_clickable_image(best_img_path, size=(400, 400), parent=self.result_frame).pack(
            pady=10
        )

        # --- Thumbnails for the rest ---
        thumbs_frame = tk.Frame(self.result_frame, bg="white")
        thumbs_frame.pack(pady=10)

        for img_name in list(results.keys())[1:]:  # skip the best_fit (already shown)
            img_path = os.path.join(self.image_path, img_name)
            self.show_clickable_image(img_path, size=(100, 100), parent=thumbs_frame).pack(
                side="left", padx=10
            )

    def show_clickable_image(self, path, size, parent):
        try:
            img = Image.open(path).resize(size, Image.LANCZOS)
            tk_img = ImageTk.PhotoImage(img)
            self.loaded_images[path] = tk_img  # Keep reference
            label = tk.Label(parent, image=tk_img, bg="white", cursor="hand2")
            label.bind("<Button-1>", lambda e, p=path: self.open_image(p))
            return label
        except Exception:
            return tk.Label(parent, text="[Image Error]", bg="white")

    def open_image(self, path):
        if os.path.exists(path):
            webbrowser.open(path)
        else:
            messagebox.showerror("Error", f"File not found: {path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhextApp(root)
    root.mainloop()
