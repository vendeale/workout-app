import streamlit as st
import pandas as pd
from st_gsheets_connection import GSheetsConnection

# 1. Configurazione della pagina
st.set_page_config(page_title="Workout Cloud Manager", page_icon="🏋️‍♂️", layout="wide")
st.title("🏋️‍♂️ Registro Allenamenti Condiviso")

# 2. Connessione a Google Sheets
# Assicurati di aver configurato i Secrets su Streamlit Cloud!
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNZIONE PER LEGGERE I DATI ---
def load_data():
    # ttl=0 serve per avere dati sempre aggiornati ad ogni refresh
    return conn.read(ttl=0)

# Caricamento dati
try:
    df = load_data()
    colonne = df.columns.tolist()
except Exception as e:
    st.error("Errore nella connessione al foglio. Controlla i Secrets!")
    st.stop()

# 3. Interfaccia a Tab
tab1, tab2 = st.tabs(["➕ Inserimento Rapido", "📊 Storico Cloud"])

with tab1:
    st.subheader("Nuovo inserimento (Sede 1 e 2)")
    with st.form("form_inserimento", clear_on_submit=True):
        nuovi_dati = {}
        
        # Griglia dinamica per i campi di input
        n_cols = 4 if len(colonne) > 8 else 3
        cols = st.columns(n_cols)
        
        for i, col_name in enumerate(colonne):
            with cols[i % n_cols]:
                if col_name == 'Data Pedalata':
                    data_scelta = st.date_input("Data Pedalata", format="DD/MM/YYYY")
                    nuovi_dati[col_name] = data_scelta.strftime("%d/%m/%Y")
                else:
                    nuovi_dati[col_name] = st.text_input(f"{col_name}")

        # Pulsante di invio
        if st.form_submit_button("Invia al Cloud"):
            if not nuovi_dati:
                st.warning("Inserisci almeno un dato.")
            else:
                # Crea la nuova riga e aggiorna il foglio
                new_row = pd.DataFrame([nuovi_dati])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                
                conn.update(data=updated_df)
                st.success("✅ Dati inviati con successo!")
                st.rerun()

with tab2:
    st.subheader("Dati in tempo reale su Google Sheets")
    st.dataframe(df, use_container_width=True)
    
    if st.button("🔄 Aggiorna Tabella"):
        st.cache_data.clear()
        st.rerun()
