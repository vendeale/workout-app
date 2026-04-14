import streamlit as st
import subprocess
import sys

# --- FORZATURA INSTALLAZIONE (Soluzione per Python 3.14) ---
try:
    from st_gsheets_connection import GSheetsConnection
except ImportError:
    # Se non lo trova, lo installiamo noi manualmente "al volo"
    subprocess.check_call([sys.executable, "-m", "pip", "install", "st-gsheets-connection==0.1.0"])
    from st_gsheets_connection import GSheetsConnection

import pandas as pd

# 1. Configurazione della pagina
st.set_page_config(page_title="Workout Cloud Manager", page_icon="🏋️‍♂️", layout="wide")
st.title("🏋️‍♂️ Registro Allenamenti Condiviso")

# 2. Connessione a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Connessione fallita. Verifica i Secrets (il link del foglio).")
    st.stop()

# --- FUNZIONE PER LEGGERE I DATI ---
def load_data():
    return conn.read(ttl=0)

# Carichiamo i dati
df = load_data()
colonne = df.columns.tolist()

# --- INTERFACCIA ---
tab1, tab2 = st.tabs(["➕ Inserimento Rapido", "📊 Storico Cloud"])

with tab1:
    st.subheader("Nuovo inserimento (Sede 1 e 2)")
    with st.form("form_inserimento", clear_on_submit=True):
        nuovi_dati = {}
        n_cols = 4 if len(colonne) > 8 else 3
        cols = st.columns(n_cols)
        
        for i, col_name in enumerate(colonne):
            with cols[i % n_cols]:
                if col_name == 'Data Pedalata':
                    data_scelta = st.date_input("Data Pedalata", format="DD/MM/YYYY")
                    nuovi_dati[col_name] = data_scelta.strftime("%d/%m/%Y")
                else:
                    nuovi_dati[col_name] = st.text_input(f"{col_name}")

        if st.form_submit_button("Invia al Cloud"):
            new_row = pd.DataFrame([nuovi_dati])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("✅ Dati inviati!")
            st.rerun()

with tab2:
    st.subheader("Dati in tempo reale")
    st.dataframe(df, use_container_width=True)
    if st.button("Aggiorna"):
        st.rerun()
