import streamlit as st
import pandas as pd

# Seitenkonfiguration
st.set_page_config(
    page_title="OncoDictate AI - Onkologischer Arztbrief-Assistent",
    page_icon="🧬",
    layout="wide"
)

# Sicheres CSS-Styling (Korrektur: Jetzt vollständig in st.markdown eingeschlossen)
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #1f77b4;
        font-weight: 700;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Passwort-Prüfung gegen st.secrets
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets.get("password", "KlinikumKassel2026!"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Bitte geben Sie das Praxis-/Klinik-Passwort ein:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Bitte geben Sie das Praxis-/Klinik-Passwort ein:", type="password", on_change=password_entered, key="password")
        st.error("😕 Das eingegebene Passwort ist leider falsch.")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- HAUPTAPP: OncoDictate AI für Onkologie ---
st.markdown('<p class="main-header">🧬 OncoDictate AI – Onkologischer Arztbrief-Assistent</p>', unsafe_allow_html=True)
st.markdown("KI-gestützte Erstellung von Verlaufs- und Entlassbriefen für die Hämatologie & Onkologie.")

# Sidebar für Patientendaten & Parameter
with st.sidebar:
    st.header("Patienten- & Falldaten")
    pat_name = st.text_input("Patientenname, Vorname", "Mustermann, Max")
    pat_dob = st.date_input("Geburtsdatum")
    tumor_entitaet = st.selectbox("Tumorentität", ["Mammakarzinom", "Kolorektales Karzinom", "Bronchialkarzinom (NSCLC/SCLC)", "AML / Leukämie", "Lymphom", "Gastrointestinaler Tumor (GI)"])
    tnm_stadium = st.text_input("TNM-Stadium / Grading", "cT2 N1 M0, G2")
    ecog = st.selectbox("ECOG Performance Status", ["ECOG 0", "ECOG 1", "ECOG 2", "ECOG 3", "ECOG 4"])

# Tabs für verschiedene Arbeitsbereiche
tab1, tab2, tab3 = st.tabs(["📝 Arztbrief-Generator", "📊 Therapieprotokoll & Marker", "⚙️ Einstellungen"])

with tab1:
    st.subheader("Automatisierte Arztbrieferstellung")
    
    col1, col2 = st.columns(2)
    with col1:
        anlass = st.selectbox("Anlass", ["Chemotherapie-Zyklus (Stationär/Tagesklinik)", "Tumorboard-Vorstellung", "Staging & Verlauf", "Entlassungsbericht"])
        chemo_protokoll = st.text_input("Verwendetes Protokoll / Medikation", "z.B. FOLFOX, R-CHOP, Pembrolizumab")
    with col2:
        klinischer_verlauf = st.text_area("Klinischer Befund & Verlauf", "Guter Allgemeinzustand, keine akuten Nebenwirkungen, Bilanzierung stabil.")

    if st.button("Arztbrief generieren"):
        with st.spinner("Generiere onkologischen Arztbrief..."):
            brief_text = f"""
KLINIKUM KASSEL
Klinik für Hämatologie, Onkologie und Immunologie
Chefärztin: Dr. med. Daniela Dörfel

ARZTBRIEF / THERAPIEBERICHT

Patient: {pat_name}, geb. am {pat_dob.strftime('%d.%m.%Y')}
Diagnose: {tumor_entitaet} ({tnm_stadium})
ECOG-Status: {ecog}

Anlass: {anlass}
Therapie / Protokoll: {chemo_protokoll}

Klinischer Befund & Verlauf:
{klinischer_verlauf}

Epikrise & Empfehlungen:
Es erfolgt die Fortführung des Therapieregimes im Rahmen der interdisziplinären Behandlungsplanung. Wiedervorstellung zur nächsten Zyklusgabe bzw. zum Kontroll-Staging.

Mit freundlichen kollegialen Grüßen,
Ihr Behandlungsteam
            """
            st.success("Arztbrief erfolgreich generiert!")
            st.text_area("Vorschau:", brief_text, height=300)

with tab2:
    st.subheader("Tumormarker & Laborverläufe")
    st.info("Hier können laborchemische Verläufe und Tumormarker (z.B. CEA, CA 15-3, CA 19-9) dokumentiert werden.")
    df = pd.DataFrame({
        "Datum": ["10.01.2026", "10.02.2026", "10.03.2026"],
        "Tumormarker (U/ml)": [24.5, 18.2, 12.1],
        "Leukozyten (/nl)": [4.5, 3.8, 5.1],
        "Hb (g/dl)": [12.1, 11.8, 12.5]
    })
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("Systemeinstellungen")
    st.write("Verbundene Fachabteilung: Hämatologie, Onkologie und Immunologie")
    st.write("KI-Modell: OncoDictate LLM Engine v2.4")
