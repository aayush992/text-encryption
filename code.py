import random
import tkinter as tk
from tkinter import messagebox

def encrypt_data(data_entry, result_label):
    data = data_entry.get()
    
    if not data:
        messagebox.showwarning("Empty Data", "Please enter data to encrypt.")
        return

    with open("dbms.txt", "w") as f, open("key_no.txt", "w") as kf:
        pkey = 0
        st = bytearray(data, "ascii")

        for _ in range(5):
            key = random.randint(10, 99)
            pkey = pkey * 100 + key

            for i, v in enumerate(st):
                st[i] = v ^ key

        encrypted_data = st.decode()
        f.write(encrypted_data)
        kf.write(str(pkey))

    messagebox.showinfo("Encryption Complete", "Your message is encrypted. Now your data is safe.")
    result_label.config(text="Encrypted Data: " + encrypted_data, fg="green", bg="lightyellow")
    data_entry.delete(0, tk.END) 

def decrypt_data(data_entry, result_label):
    try:
        with open("dbms.txt", "r") as f, open("key_no.txt", "r") as kf:
            encrypted_data = f.read()
            key_str = kf.read()
            key = int(key_str)
            st = bytearray(encrypted_data, "ascii")

            for _ in range(5):
                for i, v in enumerate(st):
                    st[i] = v ^ (key % 100)
                key = key // 100

            decrypted_data = st.decode()
            messagebox.showinfo("Decryption Complete", f"Decrypted Data:\n{decrypted_data}")
            result_label.config(text="Decrypted Data: " + decrypted_data, fg="blue", bg="lightyellow")
            data_entry.delete(0, tk.END)  

    except FileNotFoundError:
        messagebox.showwarning("File Not Found", "Encrypted data and key files not found. Please encrypt data first.")
    except ValueError:
        messagebox.showerror("Invalid Key", "Key file contains invalid data. Please check your files.")

# Create the main window
root = tk.Tk()
root.title("Data Encryption Program")

# Set background color for the entire window
root.configure(bg="lightblue")

# Create and place widgets in the window
label = tk.Label(root, text="Enter the data you want to encrypt or decrypt:", bg="lightblue")
label.pack(pady=10)

data_entry = tk.Entry(root, width=50, bg="lightyellow")
data_entry.pack(pady=10)

encrypt_button = tk.Button(root, text="Encrypt", command=lambda: encrypt_data(data_entry, result_label), bg="green", fg="white")
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(root, text="Decrypt", command=lambda: decrypt_data(data_entry, result_label), bg="blue", fg="white")
decrypt_button.pack(pady=10)

result_label = tk.Label(root, text="", fg="black", bg="lightyellow")
result_label.pack(pady=10)

root.mainloop()
