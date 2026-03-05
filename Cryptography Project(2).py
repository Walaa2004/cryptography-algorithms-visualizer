import tkinter as tk
from tkinter import ttk, messagebox
import onetimepad
import math
import random
import pyDes
import base64 
alphabet = "abcdefghijklmnopqrstuvwxyz"
def caesar_encrypt(plaintext, key):           
    ciphertext = ""                  
    for p_ch in plaintext:            
       p_index = alphabet.index(p_ch)
       c_index = (p_index + key) % 26
       c_ch = alphabet[c_index]
       ciphertext+=c_ch
    return ciphertext

def caesar_decrypt(ciphertext, key):
    return caesar_encrypt(ciphertext, -key)

def caesar_brute_force(text):
    possibilities = ""
    for key in range(1, 26):        # key value from 1 to 25
        decrypted = caesar_decrypt(text, key)
        possibilities += f"Key {key}: {decrypted}\n"
    return possibilities

def affine_encrypt(text, key1, key2):
    ciphertext = "" 
    for p_ch in text:
        if p_ch.isalpha():
           p_val = alphabet.index(p_ch)
           c_val = (key1 * p_val + key2) % 26
           c_ch = alphabet[c_val]
           ciphertext += c_ch
        else: 
            ciphertext += p_ch
    return ciphertext
def mod_inverse(a, m):
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None
def affine_decrypt(text, key1, key2):
    a_inv = mod_inverse(key1, 26)
    if a_inv is None:
        return "Invalid Key1: No Modular Inverse"
    
    return ''.join(alphabet[(a_inv * (alphabet.index(c.lower()) - key2)) % 26] if c.isalpha() else c for c in text)
def generate_key (text,key):
    
    if len(text) == len(key) :
        return key 
    
    elif len(text) < len(key) :
        key = key[:len(text)]
        return key
    
    elif len(text) > len(key):
        for i in range(len(text)- len(key)):
            key += key[i % len(key)]
        return key
def vigenere_encrypt(text, key):
     ciphertext = ""
     key = generate_key(text,key)
     for i in range(len(text)):
        p_value = alphabet.index(text[i])
        k_value = alphabet.index(key[i])
        c_value = (p_value + k_value)%26
        c_ch = alphabet[c_value]
        ciphertext += c_ch 
     return ciphertext
def vigenere_decrypt (text,key):
    plaintext = ""
    key = generate_key(text,key)
    for i in range(len(text)):
        c_value = alphabet.index(text[i])
        k_value = alphabet.index(key[i])
        p_value = (c_value - k_value)%26
        p_ch = alphabet[p_value]
        plaintext += p_ch 
    return plaintext
def rail_fence_encrypt(text, key):
    text = text.replace(' ','')
    cipherText = [""] * key 
    for row in range(key):
        pointer = row
        while pointer < len(text):
            cipherText[row] += text[pointer] 
            pointer += key
    return "".join(cipherText)
def rail_fence_decrypt(ciphertext, key):
    num_of_cols = len(ciphertext) // key
    num_of_remainder = len(ciphertext) % key
    rows = ['' for _ in range(key)]
    pointer = 0
    for r in range(key):
        if r < num_of_remainder:
            rows[r] = ciphertext[pointer:pointer + num_of_cols + 1]
            pointer += num_of_cols + 1
        else:
            rows[r] = ciphertext[pointer:pointer + num_of_cols]
            pointer += num_of_cols
    plaintext = ''
    for i in range(num_of_cols + 1):
        for r in range(key):
            if i < len(rows[r]):
                plaintext += rows[r][i]
    return plaintext
def otp_encrypt(text, key):
    cipher_text = onetimepad.encrypt(text, 'key')
    return cipher_text
def otp_decrypt(text, key):
    return onetimepad.decrypt(text, 'key')

def columnar_encrypt(plain_text, key):
    cols = len(key)
    rows = math.ceil(len(plain_text) / cols)
    fill_null = (rows * cols) - len(plain_text)
    plain_text += '_' * fill_null
    matrix = ['' for _ in range(cols)]
    for idx in range(len(plain_text)):
        column = idx % cols
        matrix[column] += plain_text[idx]
    sorted_key = sorted(list(key))
    result = ''
    for k in sorted_key:
        col_index = key.index(k)
        result += matrix[col_index]
    return result

def columnar_decrypt(cipher_text, key):
    cols = len(key)
    rows = math.ceil(len(cipher_text) / cols)
    sorted_key = sorted(list(key))
    key_index = [key.index(k) for k in sorted_key]
    total_cells = rows * cols
    extra = total_cells - len(cipher_text)
    col_lengths = [rows] * cols
    for i in range(extra):
        col_lengths[key_index[-(i + 1)]] -= 1
    arr = [['' for _ in range(cols)] for _ in range(rows)]
    pointer = 0
    for i in range(cols):
        col = key_index[i]
        for row in range(col_lengths[col]):
            arr[row][col] = cipher_text[pointer]
            pointer += 1
    plain_text = ""
    for row in arr:
        for ch in row:
            if ch != '' and ch != '_':
                plain_text += ch
    return plain_text

def playfair_generate_matrix(key):
    key = key.lower().replace("j", "i")
    matrix = []
    used = set()
    for char in key:
        if char.isalpha() and char not in used:
            matrix.append(char)
            used.add(char)
    for char in 'abcdefghiklmnopqrstuvwxyz':
        if char not in used:
            matrix.append(char)
            used.add(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)
    return -1, -1

def playfair_encrypt(text, key):
    matrix = playfair_generate_matrix(key)
    text = text.lower().replace("j", "i").replace(" ", "")
    i = 0
    pairs = []
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'x'
        if a == b:
            b = 'x'
            i += 1
        else:
            i += 2
        pairs.append((a, b))
    result = ''
    for a, b in pairs:
        r1, c1 = playfair_find_position(matrix, a)
        r2, c2 = playfair_find_position(matrix, b)
        if r1 == r2:
            result += matrix[r1][(c1 + 1) % 5]
            result += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 + 1) % 5][c1]
            result += matrix[(r2 + 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]
    return result

def playfair_decrypt(text, key):


    matrix = playfair_generate_matrix(key)
    i = 0
    result = ''
    while i < len(text):
        a = text[i]
        b = text[i+1]
        r1, c1 = playfair_find_position(matrix, a)
        r2, c2 = playfair_find_position(matrix, b)
        if r1 == r2:
            result += matrix[r1][(c1 - 1) % 5]
            result += matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 - 1) % 5][c1]
            result += matrix[(r2 - 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]
        i += 2
    return result 
def mod_inverse(e, phi):
    d_old, d = 0, 1
    r_old, r = phi, e
    while r != 0:
        quotient = r_old // r
        d_old, d = d, d_old - quotient * d
        r_old, r = r, r_old - quotient * r
    return d_old % phi
def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    for e in range(2, phi):
        if math.gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)

    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key
p = 17
q = 11
public_key, private_key = generate_keys(p, q)
e, n = public_key
d, _ = private_key
print("Public Key (e, n):", public_key)
print("Private Key (d, n):", private_key)
def RSA_encrypt(m, e, n):
    if m >= n:  
        raise ValueError("Message must be smaller than n")
    return pow(m, e, n)  
def RSA_decrypt(c, d, n):
    return pow(c, d, n)  
DES_KEY = b"DESCRYPT"                    
DES_IV = b"\0\0\0\0\0\0\0\0"              
des_obj = pyDes.des(DES_KEY, pyDes.CBC, DES_IV, pad=None, padmode=pyDes.PAD_PKCS5)
def DES_encrypt(data):
    if isinstance(data, str):
        data = data.encode()  
    encrypted = des_obj.encrypt(data)
    return base64.b64encode(encrypted).decode()
def DES_decrypt(cipher):
    if isinstance(cipher, str):
        data = base64.b64decode(cipher)  
    decrypted = des_obj.decrypt(data)
    return decrypted.decode()        
root = tk.Tk()
root.title("Encryption & Decryption Techniques")
root.geometry("500x500")
root.configure(bg="pink")
frame = tk.Frame(root)
frame.pack(pady=10)
frame.configure(bg="pink")
tk.Label(frame, text="Welcome to our Cryptography Project", font=("Helvetica", 16, "bold") , bg = "pink").pack(pady=10)
tk.Label(frame, text="Enter Text:" , font = ("Helvetica", 9, "bold") , bg = "pink").pack(pady =0)
entry_text = tk.StringVar()
text_entry = tk.Entry(frame, textvariable=entry_text, width=30)
text_entry.pack(pady=2)
algorithms = [
    'Select Algorithm',
    'Caesar Cipher', 'Caesar Cipher Brute Force', 'Affine Cipher',
    'Vigenere Cipher', 'Rail Fence Cipher',
    'One Time Pad', 'Columnar Transposition Cipher', 'Playfair Cipher' , 'RSA Cipher' , 'DES Cipher'
]
selected_algo = tk.StringVar(value='Select Algorithm')
combo = ttk.Combobox(frame, textvariable=selected_algo, values=algorithms, state="readonly" , width = 27)
combo.pack(pady=25)

key1_var = tk.StringVar()
key2_var = tk.StringVar()
output_text = tk.StringVar()
key_frame = tk.Frame(frame)
key_frame.pack(pady=5)

def update_fields(*args):
    for widget in key_frame.winfo_children():
        widget.destroy()
    algo = selected_algo.get()
    if algo in ['Caesar Cipher', 'Rail Fence Cipher', 'Vigenere Cipher', 'Columnar Transposition Cipher', 'Playfair Cipher']:
        tk.Label(key_frame, text="Key 1:").pack()
        tk.Entry(key_frame, textvariable=key1_var).pack()
    elif algo == 'Affine Cipher':
        tk.Label(key_frame, text="Key 1:").pack()
        tk.Entry(key_frame, textvariable=key1_var).pack()
        tk.Label(key_frame, text="Key 2:").pack()
        tk.Entry(key_frame, textvariable=key2_var).pack()

def on_algorithm_selected(event):
    if selected_algo.get() == "Select Algorithm":
        pass
    else:
        update_fields()

combo.bind('<<ComboboxSelected>>', on_algorithm_selected)

def encrypt():
    algo = selected_algo.get()
    text = entry_text.get()
    k1 = key1_var.get()
    k2 = key2_var.get()
    try:
        if algo == 'Caesar Cipher':
            result = caesar_encrypt(text, int(k1))
        elif algo == 'Affine Cipher':
            result = affine_encrypt(text, int(k1), int(k2))
        elif algo == 'Vigenere Cipher':
            result = vigenere_encrypt(text, k1)
        elif algo == 'Rail Fence Cipher':
            result = rail_fence_encrypt(text, int(k1))
        elif algo == 'One Time Pad':
            result = otp_encrypt(text, 'key')
        elif algo == 'Columnar Transposition Cipher':
            result = columnar_encrypt(text, k1)
        elif algo == 'Playfair Cipher':
            result = playfair_encrypt(text, k1)
        elif algo == 'RSA Cipher':
            public_key, private_key = generate_keys(p, q)
            e, n = public_key
            d, _ = private_key
            m = int(text)
            result = str(RSA_encrypt(m , e , n))
        elif algo == 'DES Cipher':
            result = DES_encrypt(text)
        
        else:
            result = 'Cannot encrypt with this algorithm.'
        output_text.set(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def decrypt():
    algo = selected_algo.get()
    text = entry_text.get()
    k1 = key1_var.get()
    k2 = key2_var.get()
    try:
        if algo == 'Caesar Cipher':
            result = caesar_decrypt(text, int(k1))
        elif algo == 'Affine Cipher':
            if mod_inverse(int(k1), 26) is None:
                messagebox.showerror("Invalid Key", "Invalid Key1: No Modular Inverse")
                return
            result = affine_decrypt(text, int(k1), int(k2))
        elif algo == 'Vigenere Cipher':
            result = vigenere_decrypt(text, k1)
        elif algo == 'Rail Fence Cipher':
            result = rail_fence_decrypt(text, int(k1))
        elif algo == 'One Time Pad':
            result = otp_decrypt(text, 'key')
        elif algo == 'Caesar Cipher Brute Force':
            result = caesar_brute_force(text)
        elif algo == 'Columnar Transposition Cipher':
            result = columnar_decrypt(text, k1)
        elif algo == 'Playfair Cipher':
            result = playfair_decrypt(text, k1)
        elif algo == 'RSA Cipher':
            public_key, private_key = generate_keys(p, q)
            e, n = public_key
            d, _ = private_key
            c = int(text)
            result = str(RSA_decrypt(c , d , n))
        elif algo == 'DES Cipher':
            result = DES_decrypt(text)
        else:
            result = 'Cannot decrypt with this algorithm.'
        output_text.set(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def reset_fields():
    text_entry.delete(0, tk.END)
    output_label.config(text="")
    key1_var.set('')
    key2_var.set('')
    selected_algo.set('Select Algorithm')
    for widget in key_frame.winfo_children():
        widget.destroy()

button_frame = tk.Frame(frame , borderwidth = 0 , highlightthickness = 0)
button_frame.pack(pady=15)
tk.Button(button_frame , text="Encrypt", command=encrypt , bg = 'pink').grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Decrypt", command=decrypt , bg = 'pink').grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="Reset", command=reset_fields , bg = 'pink').grid(row=0, column=2, padx=5)
output_label = tk.Label(frame, textvariable=output_text, wraplength=500, justify='left' , bg = "pink")
output_label.pack(pady=10)
root.mainloop()
