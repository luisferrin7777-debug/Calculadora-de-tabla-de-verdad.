import streamlit as st
import pandas as pd
from truth_table import generate_truth_table

st.set_page_config(page_title="Calculadora de Tabla de Verdad")

# ------------------ ESTILO ------------------
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        font-size: 16px;
        color: gray;
        margin-bottom: 20px;
    }
    .stButton>button {
        width: 100%;
        height: 50px;
        font-size: 16px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ TITULO ------------------
st.markdown('<div class="title">🔢 Calculadora de Tabla de la Verdad</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Construye tu expresión haciendo clic. El resultado se mostrará exclusivamente en 0 y 1.</div>', unsafe_allow_html=True)

# ------------------ ESTADO ------------------
if "expr" not in st.session_state:
    st.session_state.expr = ""

# ------------------ FUNCION PARA BOTONES ------------------
def add_to_expression(value):
    st.session_state.expr += value

def clear_expression():
    st.session_state.expr = ""

# ------------------ CONSTRUCTOR ------------------
st.subheader("🛠️ Constructor de Expresión")

# FILA 1 (variables)
cols = st.columns(6)
variables = ["A", "B", "C", "D", "E", "F"]
for i, var in enumerate(variables):
    if cols[i].button(var):
        add_to_expression(var + " ")

# FILA 2 (operadores)
cols = st.columns(6)
ops = ["AND", "OR", "NOT", "XOR", "(", ")"]
for i, op in enumerate(ops):
    if cols[i].button(op):
        add_to_expression(op + " ")

# ------------------ MOSTRAR EXPRESION ------------------
st.text_input("Expresión:", value=st.session_state.expr, key="input_expr")

# ------------------ BOTONES DE ACCION ------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Limpiar"):
        clear_expression()

with col2:
    if st.button("⚡ Generar Tabla"):
        if st.session_state.expr.strip() == "":
            st.error("⚠️ Ingresa una expresión")
        else:
            try:
                variables, table = generate_truth_table(st.session_state.expr)

                df = pd.DataFrame(table, columns=variables + ["Resultado"])
                st.success("✅ Tabla generada")

                st.dataframe(df)

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Descargar CSV",
                    csv,
                    "tabla_verdad.csv",
                    "text/csv"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")
