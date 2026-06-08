import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Tetapan Halaman
st.set_page_config(page_title="Status Lot 77", layout="wide")
st.title("Pengurusan Status Lot 77")

# Maklumat Pembayaran (Rujukan viewer)
st.info("""
**Panduan Rujukan Pembayaran:**
* **Bayaran SPA:** Gunakan rujukan `SPA77/Plot No.` (contoh: SPA77/23). Bayaran ke Akaun Maybank 112214001910 Noraini Safian.
* **Bayaran POT:** Gunakan rujukan `POT77/Plot No.` (contoh: POT77/23). Bayaran ke akaun Ambank Shamsul Rijal & Associates.
""")

# Hubungkan ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Baca data dari Google Sheets
df = conn.read(
    spreadsheet="https://docs.google.com/spreadsheets/d/1hb9sbIXB7PSlFNe57l1stMFyXat55Mw88cWfQJy99kc/edit", 
    worksheet="Lot77", 
    usecols=[0, 1, 2, 3, 4]
)

# Pastikan kolum checkbox dibaca sebagai boolean (True/False)
checkbox_cols = ['Tarik Kaveat', 'Bayaran SPA', 'Bayaran POT']
for col in checkbox_cols:
    df[col] = df[col].astype(bool)

st.write("Sila tanda (tick) pada ruang yang berkaitan di bawah:")

# Paparkan jadual interaktif (st.data_editor)
edited_df = st.data_editor(
    df,
    hide_index=True,
    disabled=["Plot", "Nama"], # Kunci kolum Plot dan Nama dari disunting
    use_container_width=True
)

# Butang untuk simpan perubahan ke Google Sheets
if st.button("Simpan Perubahan"):
    # Kemas kini data di Google Sheets
    conn.update(worksheet="Lot77", data=edited_df)
    st.success("Data berjaya dikemas kini di Google Sheets!")
    st.cache_data.clear() # Bersihkan cache supaya data terbaru dimuat pada sesi seterusnya
