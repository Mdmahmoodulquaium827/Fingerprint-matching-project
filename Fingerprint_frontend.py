import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, END, Text
import cv2
import os

# ------------------------------------------------------------------------- frontend -------------------------------------------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1350x700+0+0")
app.title("Fingerprint Matching")

label = ctk.CTkLabel(app, text="Matching Result", font=("Arial", 16))
label.place(x=880, y=30)

label = ctk.CTkLabel(app, text="Best Match & Score", font=("Arial", 16))
label.place(x=860, y=500)

image_refs = []
selected_image_path = None # store selected fingerprint path


input_textBox1 = Text(app, width=50, height=25, bg="gray14", bd=2)
input_textBox1.place(x=110, y=60)
input_textBox1.config(state="disabled")


input_textBox2 = Text(app, width=50, height=25, bg="gray14", bd=2)
input_textBox2.place(x=730, y=60)
input_textBox2.config(state="disabled")


input_textBox3 = Text(app, width=50, height=5, bg="gray14", bd=2,foreground="white")
input_textBox3.place(x=730, y=530)
input_textBox3.config(state="disabled")



# ----------------------------------------------------------------------- INSERT IMAGE --------------------------------------------------------------------
def insert_image():
    global selected_image_path

    file_path = filedialog.askopenfilename(
        title="Select Fingerprint",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    if not file_path:
        return

    selected_image_path = file_path

    img = Image.open(file_path)
    img = img.resize((400, 400))
    photo = ImageTk.PhotoImage(img)

    input_textBox1.config(state="normal")
    input_textBox1.delete("1.0", END)
    input_textBox1.image_create(END, image=photo)
    input_textBox1.config(state="disabled")

    image_refs.append(photo)


# --------------------------------------------------------------------------- MATCH FINGERPRINT -----------------------------------------------------------
def match_fingerprint():
    if selected_image_path is None:
        print("No fingerprint selected!")
        return

    sample = cv2.imread(selected_image_path, cv2.IMREAD_GRAYSCALE)
    if sample is None:
        print("Failed to load sample image")
        return

    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(sample, None)

    best_accuracy = 0
    best_image_path = None

    dataset_path = "I:\SOCOFing\Real"

    for file in os.listdir(dataset_path):
        path = os.path.join(dataset_path, file)
        fingerprint = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if fingerprint is None:
            continue

        kp2, des2 = sift.detectAndCompute(fingerprint, None)
        if des1 is None or des2 is None:
            continue

        matcher = cv2.FlannBasedMatcher(
            dict(algorithm=1, trees=10), dict()
        )
        matches = matcher.knnMatch(des1, des2, k=2)

        good_matches = []
        for p, q in matches:
            if p.distance < 0.7 * q.distance:
                good_matches.append(p)

        keypoints = min(len(kp1), len(kp2))
        if keypoints == 0:
            continue

        accuracy = (len(good_matches) / keypoints) * 100

        if accuracy > best_accuracy:
            if accuracy > 100:
                best_accuracy = 100
                best_image_path = path
            else:
                best_accuracy = accuracy
                best_image_path = path

    if best_image_path is None:
        print("No match found")
        return

    # ---------------------------------------------------------------- Show matched image ---------------------------------------------------------------
    
    img = Image.open(best_image_path) 
    img = img.resize((400, 400)) 
    photo = ImageTk.PhotoImage(img) 
    
    input_textBox2.config(state="normal") 
    input_textBox2.delete("1.0", END) 
    input_textBox2.image_create(END, image=photo) 
    input_textBox2.config(state="disabled") 
    
    image_refs.append(photo) 

    # ----------------------------------------------------------- Show accuracy & error rate ------------------------------------------------------------
    error_rate = 100 - best_accuracy

    input_textBox3.config(state="normal")
    input_textBox3.delete("1.0", END)
    input_textBox3.insert(
        END,f"Best Match File:\t{os.path.basename(best_image_path)}\n"f"Matching Accuracy: {best_accuracy:.2f}%\n"f"Error Rate: {error_rate:.2f}%"
    )
    input_textBox3.config(state="disabled")

    #print("Best Match:", + best_image_path)
    #print(f"Accuracy: {best_accuracy:.2f}%")



# ------------------------------------------------------------------------ BUTTONS ---------------------------------------------------------------------
image_button1 = ctk.CTkButton(
    app,
    text="Insert Fingerprint",
    font=("Arial", 15),
    corner_radius=30,
    command=insert_image
)
image_button1.place(x=110, y=520)

image_button2 = ctk.CTkButton(
    app,
    text="Confirm Match",
    font=("Arial", 15),
    corner_radius=30,
    command=match_fingerprint
)
image_button2.place(x=370, y=520)

app.mainloop()

