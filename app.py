import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del Dashboard
st.title("Dashboard de Cumplimiento por Feriado, Programa e Instructor")

# Cargar el archivo Excel directamente desde el repositorio
DATA_URL = "https://raw.githubusercontent.com/WeTALKUPC/App_recuperaciones/main/RECUPERACIONES%20FERIADOS%20V1.xlsx"
df = pd.read_excel(DATA_URL, engine="openpyxl")

# Limpiar los datos en las columnas seleccionadas
for col in df.columns[2:]:
    df[col] = df[col].str.strip().str.upper()
    df[col] = df[col].replace({
        "NO TENIA CLASES": "NO TENÍA CLASES",
        "NO TENÍA CLASES ": "NO TENÍA CLASES"
    })

# Sección: Selector para filtrar por cumplimiento
st.subheader("Filtrar por estado de cumplimiento")

# Selector para elegir estado
estado = st.selectbox("Selecciona un estado de cumplimiento:", ["SI", "NO", "NO TENÍA CLASES"])

# Filtrar los datos según el estado seleccionado
if estado == "NO":
    # Mostrar instructores y observaciones para "NO"
    st.write(f"Instructores que no recuperaron clases:")
    filtro_no = df.loc[df.iloc[:, 2:-1].eq(estado).any(axis=1), ["INSTRUCTOR", "PROGRAMA"]]
    filtro_no["Observaciones"] = df.loc[df.iloc[:, 2:-1].eq(estado).any(axis=1), "OBSERVACIÓN"]
    st.dataframe(filtro_no)

    # Mostrar observaciones específicas
    st.subheader("Observaciones")
    observaciones = filtro_no["Observaciones"].dropna().unique()
    for obs in observaciones:
        st.write(f"- {obs}")

else:
    # Mostrar instructores según el estado seleccionado
    st.write(f"Instructores con estado '{estado}':")
    filtro_estado = df.loc[df.iloc[:, 2:-1].eq(estado).any(axis=1), ["INSTRUCTOR", "PROGRAMA"]]
    st.dataframe(filtro_estado)

# Descargar los datos filtrados
st.subheader("Descargar resultados filtrados")
csv_estado = filtro_no.to_csv(index=False) if estado == "NO" else filtro_estado.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv_estado,
    file_name=f"instructores_{estado.lower()}.csv",
    mime="text/csv",
)

# Continuar con funcionalidades adicionales
# (gráficas, consultas previas, etc.)
