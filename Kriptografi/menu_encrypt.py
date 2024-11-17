import streamlit as st
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Fungsi Caesar Cipher (Enkripsi)
def caesar_cipher(text, shift, decrypt=False):
    if decrypt:
        shift = -shift
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

# Fungsi AES Enkripsi
def aes_encrypt(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

# Fungsi AES Dekripsi
def aes_decrypt(iv, ct, key):
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return pt

# Fungsi Super Enkripsi
def super_encrypt(text, shift, aes_key):
    # Langkah 1: Enkripsi menggunakan Caesar Cipher
    caesar_encrypted = caesar_cipher(text, shift)
    # Langkah 2: Enkripsi menggunakan AES
    iv, aes_encrypted = aes_encrypt(caesar_encrypted, aes_key)
    return iv, aes_encrypted

# Fungsi Dekripsi Super Enkripsi
def super_decrypt(iv, aes_encrypted, shift, aes_key):
    # Langkah 1: Dekripsi AES
    decrypted_text = aes_decrypt(iv, aes_encrypted, aes_key)
    # Langkah 2: Dekripsi Caesar Cipher
    return caesar_cipher(decrypted_text, shift, decrypt=True)

# Menu Enkripsi & Dekripsi
def encrypt_menu():
    st.title("Enkripsi uraian Perkara")
    operation = st.radio("Operasi", ["Enkripsi", "Dekripsi"])
    text = st.text_area("Masukkan Uraian Perkara")
    shift = st.number_input("Masukkan Shift (Caesar Cipher)", min_value=1, max_value=25, value=3)
    key = st.text_input("Masukkan Kunci AES (16, 24, atau 32 karakter)", type="password")

    if len(key) not in [16, 24, 32]:
        st.warning("Panjang kunci AES harus 16, 24, atau 32 karakter.")
    else:
        if operation == "Enkripsi":
            if st.button("Proses"):
                iv, result = super_encrypt(text, shift, key.encode())
                st.session_state.iv = iv  # Simpan IV ke session state untuk digunakan saat dekripsi
                st.session_state.aes_encrypted = result  # Simpan ciphertext untuk dekripsi nanti
                st.success(f"Hasil Enkripsi (Caesar dan Ciphertext AES): {result}")
        
        elif operation == "Dekripsi":
            # Pastikan IV dan ciphertext yang telah disimpan di session_state digunakan saat dekripsi
            if hasattr(st.session_state, "iv") and hasattr(st.session_state, "aes_encrypted"):
                iv = st.session_state.iv
                aes_encrypted = st.session_state.aes_encrypted
                if st.button("Proses"):
                    try:
                        decrypted_result = super_decrypt(iv, aes_encrypted, shift, key.encode())
                        st.success(f"Hasil Dekripsi: {decrypted_result}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan saat dekripsi: {e}")
            else:
                st.error("Pastikan Anda sudah melakukan enkripsi terlebih dahulu.")

