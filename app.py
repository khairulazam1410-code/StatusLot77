import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import traceback

st.set_page_config(page_title="Status Lot 77", layout="wide")
st.title("Pengurusan Status Lot 77")

st.info("""
**Panduan Rujukan Pembayaran:**
* **Bayaran SPA:** Gunakan rujukan `SPA77/Plot No.` (contoh: SPA77/23). Bayaran ke Akaun Maybank 112214001910 Noraini Safian.
* **Bayaran POT:** Gunakan rujukan `POT77/Plot No.` (contoh: POT77/23). Bayaran ke akaun Ambank Shamsul Rijal & Associates.
""")

try:
    # Bersihkan cache sambungan yang mungkin tersangkut pada sesi lama
    st.cache_resource.clear()
    
    # Hubungkan ke Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1hb9sbIXB7PSlFNe57l1stMFyXat55Mw88cWfQJy99kc/edit"

    # Baca jadual
    df = conn.read(
        spreadsheet=SHEET_URL,
        worksheet="Lot77",
        ttl=0 
    )

    checkbox_cols = ['Tarik Kaveat', 'Bayaran SPA', 'Bayaran POT']
    for col in checkbox_cols:
        if col in df.columns:
            df[col] = df[col].astype(bool)

    st.write("Sila tanda (tick) pada ruang yang berkaitan di bawah:")

    edited_df = st.data_editor(
        df,
        hide_index=True,
        disabled=["Plot", "Nama"], 
        use_container_width=True
    )

    if st.button("Simpan Perubahan"):
        conn.update(
            worksheet="Lot77", 
            data=edited_df,
            spreadsheet=SHEET_URL
        )
        st.success("Data berjaya dikemas kini di Google Sheets!")
        st.cache_data.clear()

except Exception as e:
    st.error("Sistem mengesan ralat. Sila semak butiran teknikal di bawah:")
    st.code(traceback.format_exc())
