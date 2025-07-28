import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Pengecekan Midtrans")

# Upload file
xl_file = st.file_uploader("Upload file xl", type=["csv"])
midtrans_df = st.file_uploader("Upload file midtrans", type=["csv"])

if xl_file and midtrans_df:
    try:
        # Baca file
        xl_df = pd.read_csv(xl_file, delimiter=';')
        midtrans_df = pd.read_csv(midtrans_df)

        # Tampilkan nama kolom agar user tahu format
        st.subheader("Nama kolom file xl.csv:")
        st.write(xl_df.columns.tolist())
        st.subheader("Nama kolom file xendit.csv:")
        st.write(midtrans_df.columns.tolist())

        # Jalankan perbandingan saat tombol ditekan
        if st.button("Jalankan Perbandingan"):
            # Normalisasi nama kolom (hilangkan spasi sebelum/sesudah)
            midtrans_df.columns = midtrans_df.columns.str.strip()

            # Cek apakah kolom 'Order Id' dan 'Transaction Status' ada
            if "Order Id" in midtrans_df.columns and "Transaction Status" in midtrans_df.columns:
                # Buat mapping
                orderid_status = midtrans_df.set_index("Order Id")["Transaction Status"].to_dict()

                # Tambahkan kolom baru ke xl_df
                xl_df["Settlement_Status"] = xl_df["transactionid"].map(orderid_status)

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
                    file_name="hasil_perbandingan_midtrans.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("Kolom 'Order Id' atau 'Status' tidak ditemukan di file xendit.csv.")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
