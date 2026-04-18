import streamlit as st
import pandas as pd
from truth_table import generate_truth_table

st.set_page_config(page_title="Tabla de Verdad", layout="centered")

# ------------------ CSS PRO ------------------
st.markdown("""
<style>

/* Fondo general */
.main {
    background-color: #f5f7fb;
}

/* Contenedor tipo card */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Título */
.title {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    margin-bottom: 5px;
}

/* Subtítulo */
.subtitle {
    text-align: center;
    color: gray;
    margin-bottom: 20px;
}

/* Input */
.stTextInput>div>div>input {
    text-align: center;
    font-size: 18px;
    border-radius: 10px;
}

/* Botones generales */
.stButton>button {
    width: 100%;
    height: 45px;
    border-radius: 10px;
    font-weight: bold;
}

/* Botón rojo principal */
div.stButton:nth-child(2) > button {
    background-color: #ff2d2d;
    color: white;
}

/* Botón limpiar */
div.stButton:nth-child(1) > button {
    background-color: #eaeaea;
}

/* Mensaje éxito */
.success-box {
    background-color: #d4edda;
    color: #155724;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
    text-align: center;
}

/* Tabla */
[data-testid="stDataFrame"] {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ ESTADO ------------------
if "expr" not in st.session_state:
    st.session_state.expr = ""

def add_to_expression(value):
    st.session_state.expr += value

def clear_expression():
    st.session_state.expr = ""

# ------------------ CARD PRINCIPAL ------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="title">🔢 Calculadora de Tabla de Verdad</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Construye tu expresión lógica fácilmente</div>', unsafe_allow_html=True)

# ------------------ CONSTRUCTOR ------------------
st.markdown("### 🛠️ Operadores")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Limpiar"):
        clear_expression()

with col2:
    if st.button("🚀 Generar Tabla"):
        generar = True
    else:
        generar = False

# Botones expresión
cols = st.columns(6)
for i, var in enumerate(["A", "B", "C", "D", "E", "F"]):
    if cols[i].button(var):
        add_to_expression(var + " ")

cols = st.columns(6)
for i, op in enumerate(["AND", "OR", "NOT", "XOR", "(", ")"]):
    if cols[i].button(op):
        add_to_expression(op + " ")

# Input centrado
st.text_input("", value=st.session_state.expr, key="input_expr")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ RESULTADO ------------------
if generar:
    if st.session_state.expr.strip() == "":
        st.error("⚠️ Ingresa una expresión")
    else:
        try:
            variables, table = generate_truth_table(st.session_state.expr)

            df = pd.DataFrame(table, columns=variables + ["Resultado"])

            # Card resultado
            st.markdown('<div class="card">', unsafe_allow_html=True)

            st.markdown(
                f'<div class="success-box">✅ Tabla generada para {len(variables)} variable(s)</div>',
                unsafe_allow_html=True
            )

            st.dataframe(df, use_container_width=True)

            # CSV compatible con Excel
            csv = df.to_csv(index=False, sep=";", encoding="utf-8-sig")

            st.download_button(
                "📥 Descargar CSV",
                csv,
                "tabla_verdad.csv",
                "text/csv"
            )

            st.markdown('</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")
