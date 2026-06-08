import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Status Lot 77 Debug", layout="wide")
st.title("Debug Status Lot 77")

# Hubungkan ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1hb9sbIXB7PSlFNe57l1stMFyXat55Mw88cWfQJy99kc/edit"

# Arahan bacaan langsung tanpa try-except untuk memaksa ralat merah keluar
df = conn.read(
    spreadsheet=SHEET_URL,
    worksheet="Lot77"
)

st.write("Jika jadual ini keluar, bermakna sambungan berjaya!")
st.write(df)
