import streamlit as st
import pandas as pd
from truth_table import generate_truth_table

st.set_page_config(page_title="Tabla de Verdad", page_icon="🧠")

st.title("Generador de Tablas de Verdad")

# Entrada de la expresión lógica
expression = st.text_input(
    "Ingresa una expresión lógica:",
    placeholder="Ejemplo: A AND B OR NOT C"
)

# Botón para generar tabla
if st.button("Generar Tabla"):
    if expression.strip() == "":
        st.error("⚠️ Por favor ingresa una expresión lógica.")
    else:
        try:
            variables, table = generate_truth_table(expression)

            # Convertir a DataFrame
            df = pd.DataFrame(table, columns=variables + [expression])

            st.success("✅ Tabla generada correctamente")
            st.dataframe(df)

            # Descargar CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Descargar como CSV",
                data=csv,
                file_name="tabla_verdad.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ Error en la expresión: {e}")