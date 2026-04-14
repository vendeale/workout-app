import streamlit as st
import pandas as pd

# --- LOGICA DI IMPORTAZIONE ROBUSTA ---
# Questo blocco prova ogni possibile nome con cui la libreria viene registrata
try:
    from st_gsheets_connection import GSheetsConnection
except ImportError:
    try:
        from streamlit_gsheetsconnection import GSheetsConnection
    except ImportError:
        try:
            # Tentativo estremo per versioni Python sperimentali
            import importlib
            mod = importlib.import_module("st_gsheets_connection")
            GSheetsConnection = mod.GSheetsConnection
        except Exception as e:
            st.error(f"Errore critico di importazione: {e}")
            st.info("Consiglio: Assicurati che nel file requirements.txt ci sia 'st-gsheets-connection'")
            st.stop()

# --- CONFIGURAZIONE INTERFACCIA ---
st.set_page_config(page_title="Workout Cloud Manager", page_icon="🏋️‍♂️", layout="wide")
st.title("🏋️‍♂️ Registro Allenamenti Condiviso")

# Connessione a Google Sheets (usa i Secrets configurati su Streamlit Cloud)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Non riesco a stabilire la connessione con Google Sheets.")
    st.info("Verifica di aver inserito correttamente i [connections.gsheets] nei Secrets.")
    st.stop()

# --- FUNZIONE PER LEGGERE I DATI ---
def load_data():
    # ttl=0 per bypassare la cache e avere dati sempre freschi
    return conn.read(ttl=0)

# Caricamento iniziale
df = load_data()
colonne = df.columns.tolist()

# --- STRUTTURA A TAB ---
tab1, tab2 = st.tabs(["➕ Inserimento Rapido", "📊 Storico Cloud"])

with tab1:
    st.subheader("Nuovo inserimento (Sede 1 e 2)")
    with st.form("form_inserimento", clear_on_submit=True):
        nuovi_dati = {}
        
        # Griglia dinamica basata sulle colonne del foglio
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
            # Creazione nuovo dataframe e concatenazione
            new_row = pd.DataFrame([nuovi_dati])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            
            # Invio al Cloud
            conn.update(data=updated_df)
            st.success("✅ Dati inviati! Aggiornamento completato.")
            st.rerun()

with tab2:
    st.subheader("Dati in tempo reale su Google Sheets")
    st.dataframe(df, use_container_width=True)
    
    if st.button("🔄 Forza Aggiornamento Tabella"):
        st.cache_data.clear()
        st.rerun()
