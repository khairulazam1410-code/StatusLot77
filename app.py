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

# Fungsi untuk menukar data asal Google Sheets kepada format visual
def format_status(val):
    val_str = str(val).strip().upper()
    if pd.isna(val) or val_str in ["FALSE", "", "NONE", "NAN"]:
        return "❌ Belum"
    elif val_str in ["TRUE", "☑", "1"]:
        return "✅ Selesai"
    elif "TIADA KAVEAT" in val_str:
        return "TIADA KAVEAT"
    elif "N/A" in val_str:
        return "N/A"
    else:
        return str(val).strip()

try:
    st.cache_resource.clear()
    conn = st.connection("gsheets", type=GSheetsConnection)
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1hb9sbIXB7PSlFNe57l1stMFyXat55Mw88cWfQJy99kc/edit"

    df = conn.read(
        spreadsheet=SHEET_URL,
        worksheet="Lot77",
        ttl=0 
    )

    # Aplikasikan fungsi format kepada kolum yang berkaitan
    status_cols = ['Tarik Kaveat', 'Bayaran SPA', 'Bayaran POT']
    for col in status_cols:
        if col in df.columns:
            df[col] = df[col].apply(format_status)

    st.write("Sila kemas kini status pada ruang yang disediakan di bawah:")

    # Konfigurasi Dropdown untuk paparan data_editor
    kolum_konfig = {}
    for col in status_cols:
        kolum_konfig[col] = st.column_config.SelectboxColumn(
            col,
            help="Pilih status terkini",
            options=["✅ Selesai", "❌ Belum", "TIADA KAVEAT", "N/A"],
            required=True
        )

    # Paparkan jadual interaktif
    edited_df = st.data_editor(
        df,
        hide_index=True,
        disabled=["Plot", "Nama"], # Kunci kolum utama
        column_config=kolum_konfig, # Gunakan konfigurasi dropdown
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
