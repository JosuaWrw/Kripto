import streamlit as st
from login import login_page, register_page
from main_page import main_page
from menu_encrypt import encrypt_menu
from menu_steganografi import steganography_menu
from menu_kunci_file import file_lock_menu

# Inisialisasi Session State
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

# Routing
if st.session_state["logged_in"]:
    menu = st.sidebar.radio("Menu", ["Menu Utama", "Enkripsi & Dekripsi", "Steganografi", "Kunci File"])
    if menu == "Menu Utama":
        main_page()
    elif menu == "Enkripsi & Dekripsi":
        encrypt_menu()
    elif menu == "Steganografi":
        steganography_menu()
    elif menu == "Kunci File":
        file_lock_menu()
else:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login_page()
    elif choice == "Register":
        register_page()
