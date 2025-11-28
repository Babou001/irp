# document_mining.py  ── version stable ─────────────────────
import os, requests, streamlit as st
from streamlit_pdf_viewer import pdf_viewer   # ou votre composant maison

FASTAPI_URL = "http://127.0.0.1:8000"

# ---------- 1. session_state safe defaults -----------------
ss = st.session_state
ss.setdefault("pdf_refs", [])
ss.setdefault("metadatas", [])
ss.setdefault("selected_pdf", None)
ss.setdefault("selected_meta", {})

# ---------- 2. Barre latérale : options -------------------
st.sidebar.header("Options")
show_meta = st.sidebar.checkbox("Afficher les métadonnées", value=False)


# ---------- 2b.  Mode de recherche ------------------------
mode = None 

# ---------- 3. Zone de requête ------------------------------
st.page_link("streamlit_pages/home.py", label="Home", icon="🏠")
query = st.text_input("Entrez votre requête")

if st.button("Chercher") and query.strip():
    payload = {"query": query}  # 'mode' retiré

    try:
        r = requests.post(f"{FASTAPI_URL}/retrieve", json=payload, timeout=15)
    except requests.RequestException as e:
        st.error(f"Erreur de connexion à l'API /retrieve : {e}")
        st.stop()

    if not r.ok:
        # On affiche un aperçu de la réponse pour debug sans casser l'UI
        preview = (r.text or "")[:300]
        st.error(f"API /retrieve a échoué ({r.status_code}). Détails: {preview}")
        st.stop()

    try:
        data = r.json()
    except ValueError:
        st.error("La réponse de l'API /retrieve n'est pas un JSON valide.")
        st.stop()

    ss.pdf_refs   = data.get("documents", []) or []
    ss.metadatas  = data.get("metadatas", []) or []
    ss.selected_pdf  = None
    ss.selected_meta = {}
    st.rerun()  # relance pour afficher les résultats


# ---------- 4. Affichage des résultats ----------------------
st.subheader("Documents trouvés")

if not ss.pdf_refs:
    st.info("Aucun document pour ces filtres.")
else:
    for i, path in enumerate(ss.pdf_refs):
        name = os.path.basename(path) or f"doc_{i}"
        if st.button(name, key=f"btn_{i}"):
            ss.selected_pdf  = path
            ss.selected_meta = ss.metadatas[i] if i < len(ss.metadatas) else {}
            st.rerun()

# ---------- 5. Visionneuse PDF + métadonnées ----------------
if ss.selected_pdf:
    st.markdown("### Visionneuse PDF")
    with open(ss.selected_pdf, "rb") as f:
        pdf_viewer(input=f.read(), width=700, height=900)

    if show_meta and ss.selected_meta:
        st.markdown("#### Métadonnées")
        st.json(ss.selected_meta)
