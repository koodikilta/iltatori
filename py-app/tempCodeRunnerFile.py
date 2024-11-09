import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from skimage.feature import graycomatrix, graycoprops
from scipy.stats import skew
import os
import csv
from datetime import datetime
import logging
import shutil
import pytesseract


# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ImageAnalysisApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.canvas = tk.Canvas(window, width=800, height=600)
        self.canvas.pack()

        self.btn_frame = tk.Frame(window)
        self.btn_frame.pack(fill=tk.X, padx=5, pady=5)

        self.btn_load = tk.Button(self.btn_frame, text="Load Image", width=20, command=self.load_image)
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_ocr = tk.Button(self.btn_frame, text="OCR", width=20, command=self.perform_ocr)
        self.btn_ocr.pack(side=tk.LEFT, padx=5)

        self.btn_texture = tk.Button(self.btn_frame, text="Analyze Texture", width=20, command=self.analyze_texture)
        self.btn_texture.pack(side=tk.LEFT, padx=5)

        self.btn_color = tk.Button(self.btn_frame, text="Analyze Color", width=20, command=self.analyze_color)
        self.btn_color.pack(side=tk.LEFT, padx=5)

        self.btn_edge = tk.Button(self.btn_frame, text="Detect Edges", width=20, command=self.detect_edges)
        self.btn_edge.pack(side=tk.LEFT, padx=5)

        self.btn_guess = tk.Button(self.btn_frame, text="Guess Image", width=20, command=self.guess_image)
        self.btn_guess.pack(side=tk.LEFT, padx=5)

        self.lbl_result = tk.Label(window, text="No image loaded", wraplength=780)
        self.lbl_result.pack()

        self.guess_frame = tk.Frame(window)
        self.lbl_guess = tk.Label(self.guess_frame, text="")
        self.btn_yes = tk.Button(self.guess_frame, text="Yes", command=self.guess_correct)
        self.btn_no = tk.Button(self.guess_frame, text="No", command=self.guess_incorrect)

        self.type_var = tk.StringVar(value="object")
        self.type_frame = tk.Frame(window)
        self.type_label = tk.Label(self.type_frame, text="Type:")
        self.type_label.pack(side=tk.LEFT)
        self.type_object = tk.Radiobutton(self.type_frame, text="Object", variable=self.type_var, value="object")
        self.type_object.pack(side=tk.LEFT)
        self.type_text = tk.Radiobutton(self.type_frame, text="Text", variable=self.type_var, value="text")
        self.type_text.pack(side=tk.LEFT)
        self.type_frame.pack()

        self.image = None
        self.photo = None
        self.original_image = None
        self.current_guess = None
        self.collectables = self.load_collectables()

    # Check if Tesseract is available
        self.tesseract_available = self.check_tesseract()
        if not self.tesseract_available:
            self.btn_ocr.config(state=tk.DISABLED)
            logging.warning("Tesseract OCR is not available. OCR button disabled.")

    def check_tesseract(self):
            try:
                import pytesseract
                tesseract_cmd = shutil.which('tesseract')
                if tesseract_cmd is None:
                    logging.warning("Tesseract executable not found in PATH")
                    print("Tesseract executable not found in PATH")
                    return False
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
                print(f"Tesseract found at: {tesseract_cmd}")
                # Test Tesseract
                test_string = pytesseract.get_tesseract_version()
                print(f"Tesseract version: {test_string}")
                return True
            except ImportError as e:
                logging.warning(f"pytesseract module not installed: {str(e)}")
                print(f"pytesseract module not installed: {str(e)}")
                return False
            except Exception as e:
                logging.warning(f"Error checking Tesseract: {str(e)}")
                print(f"Error checking Tesseract: {str(e)}")
                return False
        
    def perform_ocr(self):
        if not self.tesseract_available:
            messagebox.showinfo("Error", "Tesseract OCR is not available. Please install Tesseract and add it to your PATH.")
            return
        if self.image is None:
            messagebox.showinfo("Error", "Please load an image first.")
            return

        try:
            gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            text = pytesseract.image_to_string(gray)
            if text.strip():
                self.lbl_result.config(text="OCR Result:\n" + text)
            else:
                self.lbl_result.config(text="OCR Result: No text detected in the image.")
        except Exception as e:
            error_message = str(e)
            print(f"OCR Error: {error_message}")
            logging.error(f"OCR Error: {error_message}")
            if "tesseract is not installed" in error_message.lower():
                message = "Tesseract is not installed or not in your PATH. Please install Tesseract and add it to your PATH."
            else:
                message = f"OCR failed: {error_message}"
            messagebox.showerror("Error", message)


    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.image = cv2.imread(file_path)
                if self.image is None:
                    raise ValueError("Image could not be read")
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
                self.original_image = self.image.copy()
                self.display_image(self.image)
                self.lbl_result.config(text="Image loaded. Choose an analysis method.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {str(e)}")
                logging.error(f"Failed to load image: {str(e)}")
                self.image = None

    def display_image(self, image):
        if image is not None:
            height, width = image.shape[:2]
            max_height = 600
            max_width = 800
            scale = min(max_height/height, max_width/width)
            new_width = int(width * scale)
            new_height = int(height * scale)
            self.image_display = cv2.resize(image, (new_width, new_height))
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(self.image_display))
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def analyze_texture(self):
        if self.image is None:
            messagebox.showinfo("Error", "Please load an image first.")
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        glcm = graycomatrix(gray, [1], [0], symmetric=True, normed=True)
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        correlation = graycoprops(glcm, 'correlation')[0, 0]

        self.lbl_result.config(text=f"Texture Analysis Results:\nContrast: {contrast:.2f}\n"
                                    f"Homogeneity: {homogeneity:.2f}\nEnergy: {energy:.2f}\n"
                                    f"Correlation: {correlation:.2f}")

    def analyze_color(self):
        if self.image is None:
            messagebox.showinfo("Error", "Please load an image first.")
            return

        channels = cv2.split(self.image)
        colors = ('Red', 'Green', 'Blue')
        results = []
        for channel, color in zip(channels, colors):
            mean = np.mean(channel)
            std = np.std(channel)
            skewness = skew(channel.ravel())
            results.append(f"{color}: Mean: {mean:.2f}, Std: {std:.2f}, Skewness: {skewness:.2f}")

        self.lbl_result.config(text="Color Analysis Results:\n" + "\n".join(results))

    def detect_edges(self):
        if self.image is None:
            messagebox.showinfo("Error", "Please load an image first.")
            return

        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        self.image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        self.display_image(self.image)
        self.lbl_result.config(text="Edge detection completed. Edges are shown in white.")

    def guess_image(self):
        if self.image is None:
            messagebox.showinfo("Error", "Please load an image first.")
            return

        # Simple guessing logic (replace with more sophisticated method later)
        if not self.collectables:
            self.current_guess = "Unknown object"
        else:
            self.current_guess = np.random.choice(list(self.collectables.keys()))

        self.lbl_guess.config(text=f"Is it a {self.current_guess}?")
        self.lbl_guess.pack()
        self.btn_yes.pack(side=tk.LEFT, padx=5)
        self.btn_no.pack(side=tk.LEFT, padx=5)
        self.guess_frame.pack()

    def guess_correct(self):
        if self.current_guess and self.image is not None:
            try:
                self.save_image(self.current_guess)
                self.lbl_result.config(text=f"Great! The image has been saved as a {self.current_guess}.")
                logging.info(f"Image saved as {self.current_guess}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
                logging.error(f"Failed to save image: {str(e)}")
        self.reset_guess()

    def guess_incorrect(self):
        new_name = simpledialog.askstring("Input", "What is this object?")
        if new_name:
            try:
                self.save_image(new_name)
                self.add_to_collectables(new_name)
                self.lbl_result.config(text=f"Thank you! The image has been saved as a {new_name}.")
                logging.info(f"New item added: {new_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image or update collectables: {str(e)}")
                logging.error(f"Failed to save image or update collectables: {str(e)}")
        self.reset_guess()

    def reset_guess(self):
        self.lbl_guess.pack_forget()
        self.btn_yes.pack_forget()
        self.btn_no.pack_forget()
        self.guess_frame.pack_forget()
        self.current_guess = None
        self.image = self.original_image.copy()
        self.display_image(self.image)

    def save_image(self, name):
        if not os.path.exists('training'):
            os.makedirs('training')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"training/{name}_{timestamp}.png"
        cv2.imwrite(filename, cv2.cvtColor(self.original_image, cv2.COLOR_RGB2BGR))

    def load_collectables(self):
        collectables = {}
        if os.path.exists('training/collectables.csv'):
            with open('training/collectables.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    collectables[row[0]] = {'category': row[1], 'type': row[2], 'filters': row[3:]}
        return collectables

    def add_to_collectables(self, name, category=""):
        item_type = self.type_var.get()
        if name not in self.collectables:
            self.collectables[name] = {'category': category, 'type': item_type, 'filters': []}
            self.save_collectables()

    def save_collectables(self):
        with open('training/collectables.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for name, data in self.collectables.items():
                writer.writerow([name, data['category'], data['type']] + data['filters'])

# Create a window and pass it to the Application object
root = tk.Tk()
app = ImageAnalysisApp(root, "Advanced Image Analysis App")
print("Starting main loop...")  # Add this line
root.mainloop()