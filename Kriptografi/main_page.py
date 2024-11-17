import streamlit as st

# Halaman Utama
def main_page():
    st.title("Sistem Pelaporan SPDP")
    if "username" in st.session_state:
        st.write(f"Selamat datang, {st.session_state['username']}!")
        st.write("Ini adalah halaman utama sistem pelaporan SPDP.")
        if st.button("Logout"):
            st.session_state["logged_in"] = False
            st.session_state["username"] = ""
            st.success("Anda telah logout. Silakan kembali ke halaman login.")
            st.rerun()
    else:
        st.error("Anda belum login. Silakan login terlebih dahulu.")
