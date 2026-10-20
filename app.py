import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Mentoring RIMAC", page_icon="⭐", layout="wide")
st.markdown("""<style>
.stApp{background:#fff}.block-container{max-width:1100px;padding-top:2rem}
.hero{background:#e30613;color:white;padding:2rem;border-radius:22px}.card{background:#f7f7f7;border:1px solid #eee;border-radius:18px;padding:1.2rem;min-height:145px}
[data-testid="stSidebar"]{background:#f7f7f7}
</style>""", unsafe_allow_html=True)

USERS=Path("usuarios.csv")
GUIDES={"mentor":Path("recursos/Guia_del_Mentor_Descargar.html"),"mentee":Path("recursos/Guia_del_Mentee_Descargar.html")}
@st.cache_data
def load_users():
    return pd.read_csv(USERS,dtype=str).fillna("")

def guide_button(path,label):
    if path.exists(): st.download_button(label,path.read_bytes(),file_name=path.name,mime="text/html",use_container_width=True)
    else: st.info(f"Sube {path} para activar la descarga.")

st.markdown('<div class="hero"><small>3.ª edición | Desarrollo del Talento</small><h1>Programa de Mentoring</h1><p>Experiencia que se convierte en aprendizaje, perspectiva y acción.</p></div>',unsafe_allow_html=True)
users=load_users()
if "person" not in st.session_state: st.session_state.person=None
if not st.session_state.person:
    st.subheader("Ingresa al portal")
    dni=st.text_input("DNI",max_chars=12)
    if st.button("Ingresar",type="primary",use_container_width=True):
        m=users[users.dni==dni.strip()]
        if m.empty: st.error("No encontramos este DNI.")
        else: st.session_state.person=m.iloc[0].to_dict(); st.rerun()
    st.caption("Usa solo datos de prueba mientras el repositorio sea público.")
    st.stop()

p=st.session_state.person
role=p["rol"].strip().lower()
with st.sidebar:
    st.header(f"Hola, {p['nombre']} 👋")
    st.caption(p["rol"])
    page=st.radio("Explora",["Inicio","Mi dupla","Guía","Bitácora","Territorios","Recursos"])
    if st.button("Cerrar sesión"): st.session_state.person=None; st.rerun()

if page=="Inicio":
    st.header("Tu experiencia de mentoring")
    cols=st.columns(3)
    items=[("1. Prepárate","Define un tema y una pregunta real."),("2. Conversa","Escucha, pregunta y conecta con el PDI."),("3. Actúa","Registra acuerdos y próximos pasos.")]
    for c,(t,d) in zip(cols,items): c.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>',unsafe_allow_html=True)
elif page=="Mi dupla":
    st.header("Mi dupla"); st.metric("Tu dupla",p.get("dupla") or "Por asignar")
elif page=="Guía":
    if role=="mentor":
        st.header("Guía del Mentor"); st.write("Rol del mentor | SER | Mentoring y PDI | Cinco territorios | Habilidades | Herramientas | Biblioteca | Situaciones difíciles")
        guide_button(GUIDES["mentor"],"Descargar Guía del Mentor")
    else:
        st.header("Guía del Mentee"); st.write("Tu rol | SER | PDI y 70-20-10 | Cinco territorios | Bitácora | Desafíos | Herramientas | Situaciones difíciles | Biblioteca")
        guide_button(GUIDES["mentee"],"Descargar Guía del Mentee")
elif page=="Bitácora":
    st.header("Bitácora"); st.info("Para datos reales, enlaza una bitácora segura de SharePoint. No guardes notas personales en un repositorio público.")
elif page=="Territorios":
    st.header("Cinco territorios")
    for x in ["Propósito y transformación","Liderazgo","Autoconocimiento","Networking e influencia","Carrera y empleabilidad"]:
        with st.expander(x): st.write("Usa este territorio para enfocar la conversación y definir una acción concreta.")
else:
    st.header("Recursos")
    st.markdown("""
- Revisión 70-20-10 del PDI
- DISC aplicado al mentoring
- Círculo de control e influencia
- Escalera de inferencias
- Mapa de stakeholders
- #LunesDeMentoría
""")
