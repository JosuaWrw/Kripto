import streamlit as st
from cryptography.fernet import Fernet

# Fungsi untuk mengenkripsi file
def encrypt_file(file, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(file.read())
    return encrypted_data

# Fungsi untuk membuat kunci baru
def generate_key():
    return Fernet.generate_key()

# Menu Kunci File
def file_lock_menu():
    st.title("Menu Kunci File")
    operation = st.radio("Operasi", ["Kunci File", "Buat Kunci Baru"])
    if operation == "Buat Kunci Baru":
        key = generate_key()
        st.success(f"Kunci Baru: {key.decode()}")
        st.download_button("Download Kunci", data=key, file_name="file_key.key")
    elif operation == "Kunci File":
        file = st.file_uploader("Upload File untuk Dikunci")
        key = st.text_input("Masukkan Kunci")
        if file and key:
            try:
                encrypted_data = encrypt_file(file, key.encode())
                st.success("File berhasil dikunci!")
                st.download_button("Download File Terkunci", data=encrypted_data, file_name=f"{file.name}.locked")
            except Exception:
                st.error("Kunci tidak valid atau file gagal dikunci.")
