import streamlit as st
from streamlit_gsheetsconnection import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Workout Cloud Manager", page_icon="🏋️‍♂️", layout="wide")
st.title("🏋️‍♂️ Registro Allenamenti Condiviso")

# Connessione a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNZIONE PER LEGGERE I DATI ---
def load_data():
    return conn.read(ttl=0) # ttl=0 serve per avere dati sempre aggiornati

df = load_data()
colonne = df.columns.tolist()

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
            # Aggiunge la riga al dataframe esistente
            new_row = pd.DataFrame([nuovi_dati])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Scrive tutto su Google Sheets
            conn.update(data=updated_df)
            st.success("✅ Dati inviati! Entrambe le sedi ora vedranno l'aggiornamento.")
            st.rerun()

with tab2:
    st.subheader("Dati in tempo reale su Google Sheets")
    st.dataframe(df, use_container_width=True)
    
    if st.button("Aggiorna Tabella"):
        st.rerun()