import streamlit as st
import pandas as pd

st.set_page_config(page_title="Workout Cloud Manager", page_icon="🏋️‍♂️", layout="wide")
st.title("🏋️‍♂️ Registro Allenamenti Condiviso")

# --- CONFIGURAZIONE ---
# Incolla qui il link che hai ottenuto dalla "Pubblicazione sul Web"
CSV_URL = "IL_TUO_LINK_CSV_PUBBLICATO_QUI"

def load_data():
    # Aggiungiamo un parametro casuale per evitare la cache del browser
    return pd.read_csv(f"{CSV_URL}")

try:
    df = load_data()
    
    tab1, tab2 = st.tabs(["➕ Visualizza Dati", "📊 Analisi"])

    with tab1:
        st.subheader("Dati dal Cloud (Sola Lettura via CSV)")
        st.dataframe(df, use_container_width=True)
        if st.button("Aggiorna"):
            st.rerun()
            
    with tab2:
        st.info("Nota: Per inserire dati, usa direttamente il foglio Google. Questa app li visualizzerà in tempo reale.")

except Exception as e:
    st.error(f"Errore nel caricamento: {e}")
    st.info("Assicurati di aver 'Pubblicato sul Web' il file come CSV.")
