import streamlit as st
else:
try:
row = {
"timestamp": datetime.now().isoformat(timespec="seconds"),
"alumne": alumne,
"grup": grup,
"professor": professor.strip(),
"area": area,
"categoria": categoria,
"comentari": comentari.strip(),
"accio": accio.strip(),
"visibilitat": visibilitat
}
append_row(sh, row)
st.success(f"Observació desada per a {alumne}.")
st.toast("Guardat!", icon="✅")
st.experimental_rerun()
except Exception as e:
st.error(f"No s'ha pogut desar: {e}")


# ------------------ Consultar ------------------
else:
st.subheader("🔎 Consulta del progrés")
if df_obs.empty:
st.info("Encara no hi ha observacions.")
st.stop()


# Protecció bàsica per a vista tutor
pin_tutor = st.text_input("PIN tutor (requerit per consultar)", type="password")
if pin_tutor != st.secrets.get("PIN_TUTOR",""):
st.warning("Introdueix el PIN tutor per veure dades.")
st.stop()


# Uneix tutor si existeix
if "tutor" in df_alumnes.columns:
df_obs = df_obs.merge(df_alumnes[["alumne","grup","tutor"]], on=["alumne","grup"], how="left")


# Filtres
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
alumne_f = st.selectbox("Alumne", ["(tots)"] + sorted(df_obs["alumne"].dropna().unique().tolist()))
with c2:
grup_f = st.selectbox("Grup", ["(tots)"] + sorted(df_obs["grup"].dropna().unique().tolist()))
with c3:
cat_f = st.selectbox("Categoria", ["(totes)"] + sorted(df_obs["categoria"].dropna().unique().tolist()))
with c4:
area_f = st.selectbox("Àrea", ["(totes)"] + sorted(df_obs["area"].dropna().unique().tolist()))
with c5:
prof_f = st.selectbox("Professor/a", ["(tots)"] + sorted(df_obs["professor"].dropna().unique().tolist()))


filt = df_obs.copy()
if alumne_f != "(tots)": filt = filt[filt["alumne"] == alumne_f]
if grup_f != "(tots)": filt = filt[filt["grup"] == grup_f]
if cat_f != "(totes)": filt = filt[filt["categoria"] == cat_f]
if area_f != "(totes)": filt = filt[filt["area"] == area_f]
if prof_f != "(tots)": filt = filt[filt["professor"] == prof_f]


k1, k2, k3 = st.columns(3)
with k1: st.metric("Observacions", len(filt))
with k2: st.metric("Àrees implicades", filt["area"].nunique())
with k3: st.metric("Docents", filt["professor"].nunique())


cols = ["timestamp","alumne","grup","professor","area","categoria","comentari","accio","visibilitat"]
st.dataframe(filt[cols].sort_values("timestamp", ascending=False),
use_container_width=True, height=520)
