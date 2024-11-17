import streamlit as st
from PIL import Image
from stegano import lsb

# Menu Steganografi
def steganography_menu():
    st.title("Menu Steganografi")
    operation = st.radio("Operasi", ["Sisipkan Pesan", "Baca Pesan"])

    if operation == "Sisipkan Pesan":
        image_file = st.file_uploader("Upload Gambar", type=["png", "jpg", "jpeg"])
        message = st.text_area("Masukkan Pesan yang Ingin Disisipkan")

        if image_file and message:
            image = Image.open(image_file)
            secret_image = lsb.hide(image, message)
            secret_image.save("secret_image.png")
            st.success("Pesan berhasil disisipkan!")
            st.download_button("Download Gambar dengan Pesan", data=open("secret_image.png", "rb"), file_name="secret_image.png")
    elif operation == "Baca Pesan":
        image_file = st.file_uploader("Upload Gambar dengan Pesan", type=["png"])
        if image_file:
            image = Image.open(image_file)
            try:
                message = lsb.reveal(image)
                st.success(f"Pesan yang Disisipkan: {message}")
            except Exception:
                st.error("Tidak ada pesan yang ditemukan dalam gambar.")
