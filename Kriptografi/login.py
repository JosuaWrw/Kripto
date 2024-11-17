import mysql.connector
import bcrypt
import streamlit as st

# Fungsi untuk membuat koneksi ke database
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",            # Ganti dengan username database Anda
        password="",            # Ganti dengan password database Anda
        database="db_lapor"
    )

# Fungsi untuk Register
def register_user(username, plaintext_password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        hashed_password = bcrypt.hashpw(plaintext_password.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode("utf-8")))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Duplicate entry error
            return False
        raise err
    finally:
        cursor.close()
        conn.close()

# Fungsi untuk Login
def login_user(username, plaintext_password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0]
            if bcrypt.checkpw(plaintext_password.encode("utf-8"), stored_password.encode("utf-8")):
                return True
        return False
    finally:
        cursor.close()
        conn.close()

# Halaman Login
def login_page():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_button"):
        if login_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Username atau password salah!")

# Halaman Register
def register_page():
    st.subheader("Register")
    username = st.text_input("Buat Username", key="register_username")
    password = st.text_input("Buat Password", type="password", key="register_password")
    if st.button("Register", key="register_button"):
        if register_user(username, password):
            st.success("Pendaftaran berhasil! Silakan login.")
        else:
            st.error("Username sudah digunakan. Pilih username lain.")
