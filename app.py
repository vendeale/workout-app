import streamlit as st
from st_gsheets_connection import GSheetsConnection  # <--- Modifica questa riga
import pandas as pd

# 1. Configurazione della pagina (Titolo e Icona nella scheda del browser)
st.set_page_config(page_title="Workout Cloud Manager", page_icon="🏋️‍♂️", layout="wide")
st.title("🏋️‍♂️ Registro Allenamenti Condiviso")

# 2. Connessione a Google Sheets (usa i parametri salvati nei Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNZIONE PER LEGGERE I DATI ---
def load_data():
    # ttl=0 assicura che l'app scarichi i dati freschi dal cloud ogni volta
    return conn.read(ttl=0)

# Carichiamo i dati attuali
df = load_data()
colonne = df.columns.tolist()

# Creazione dei Tab (Sottopagine)
tab1, tab2 = st.tabs(["➕ Inserimento Rapido", "📊 Storico Cloud"])

with tab1:
    st.subheader("Nuovo inserimento (Sede 1 e 2)")
    with st.form("form_inserimento", clear_on_submit=True):
        nuovi_dati = {}
        
        # Organizziamo i campi in colonne per non rendere il modulo troppo lungo
        n_cols = 4 if len(colonne) > 8 else 3
        cols = st.columns(n_cols)
        
        for i, col_name in enumerate(colonne):
            with cols[i % n_cols]:
                if col_name == 'Data Pedalata':
                    # Campo speciale per la data con calendario
                    data_scelta = st.date_input("Data Pedalata", format="DD/MM/YYYY")
                    nuovi_dati[col_name] = data_scelta.strftime("%d/%m/%Y")
                else:
                    # Campo di testo normale per tutte le altre colonne
                    nuovi_dati[col_name] = st.text_input(f"{col_name}")

        # Pulsante di invio
        if st.form_submit_button("Invia al Cloud"):
            # Crea una nuova riga con i dati inseriti
            new_row = pd.DataFrame([nuovi_dati])
            
            # Unisce i vecchi dati con i nuovi
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Sovrascrive il foglio Google con la tabella aggiornata
            conn.update(data=updated_df)
            
            st.success("✅ Dati inviati! Entrambe le sedi ora vedranno l'aggiornamento.")
            
            # Ricarica l'app per mostrare subito la nuova riga nello storico
            st.rerun()

with tab2:
    st.subheader("Dati in tempo reale su Google Sheets")
    # Mostra la tabella completa
    st.dataframe(df, use_container_width=True)
    
    # Pulsante manuale per aggiornare se necessario
    if st.button("Aggiorna Tabella"):
        st.rerun()
