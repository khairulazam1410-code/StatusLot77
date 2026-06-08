import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Debug Tahap 2", layout="wide")
st.title("Debug Akses Google Sheets")

try:
    # Buat sambungan
    conn = st.connection("gsheets", type=GSheetsConnection)
    client = conn.client # Panggil klien gspread secara terus
    
    # Semak e-mel Service Account yang sedang digunakan
    if hasattr(client.auth, 'signer') and hasattr(client.auth.signer, 'email'):
        st.success(f"Log masuk berjaya! E-mel yang digunakan: {client.auth.signer.email}")
    else:
        st.success("Log masuk berjaya menggunakan Service Account.")
        
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1hb9sbIXB7PSlFNe57l1stMFyXat55Mw88cWfQJy99kc/edit"
    st.write(f"Cuba membuka fail Google Sheets...")
    
    # Cuba buka fail secara langsung
    spreadsheet = client.open_by_url(SHEET_URL)
    st.info(f"Akses Dibenarkan! Nama fail anda ialah: **{spreadsheet.title}**")
    
    # Cuba baca helaian Lot77
    worksheet = spreadsheet.worksheet("Lot77")
    data = worksheet.get_all_records()
    
    st.write("Jadual berjaya dibaca:")
    st.dataframe(data)

except Exception as e:
    st.error(f"Akses Ditolak: {e}")
    st.write("Sila pastikan e-mel Service Account telah dimasukkan ke dalam butang 'Share' di Google Sheets.")
