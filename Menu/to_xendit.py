import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Perbandingan Transaction ID dengan Reference")

# Upload file
xl_file = st.file_uploader("Upload file xl.csv, dengan delimiter ;", type=["csv"])
xendit_file = st.file_uploader("Upload file xendit.csv, tanpa tanda \"", type=["csv"])

if xl_file and xendit_file:
    try:
        # Baca file
        xl_df = pd.read_csv(xl_file, delimiter=';')
        xendit_df = pd.read_csv(xendit_file)

        # Normalisasi nama kolom xl_df
        xl_df = xl_df.columns.str.strip().str.lower()  # ubah semua nama kolom ke lowercase
        xendit_df = xendit_df.columns.str.strip()


        # Tampilkan nama kolom agar user tahu format
        st.subheader("Nama kolom file xl.csv:")
        st.write(xl_df.columns.tolist())
        st.subheader("Nama kolom file xendit.csv:")
        st.write(xendit_df.columns.tolist())

        # Jalankan perbandingan saat tombol ditekan
        if st.button("Jalankan Perbandingan"):
            # Normalisasi nama kolom (hilangkan spasi sebelum/sesudah)
            xendit_df.columns = xendit_df.columns.str.strip()

            # Cek apakah kolom 'reference' dan 'Settlement Status' ada
            if "Reference" in xendit_df.columns and "Status" in xendit_df.columns:
                # Buat mapping
                reference_status = xendit_df.set_index("Reference")["Status"].to_dict()

                # Tambahkan kolom baru ke xl_df
                xl_df["Settlement_Status"] = xl_df["transactionid"].map(reference_status)

                # Tampilkan hasil
                st.success("Perbandingan selesai!")
                st.dataframe(xl_df.head())

                # Simpan ke Excel (in-memory)
                output = BytesIO()
                xl_df.to_excel(output, index=False)
                output.seek(0)

                # Tombol download
                st.download_button(
                    label="Download hasil sebagai Excel",
                    data=output,
                    file_name="hasil_perbandingan.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Kolom 'Reference' atau 'Status' tidak ditemukan di file xendit.csv.")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
