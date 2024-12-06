import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del Dashboard
st.title("Dashboard de Cumplimiento por Feriado, Programa y Docente")

# Cargar el archivo Excel directamente desde el repositorio
DATA_URL = "https://raw.githubusercontent.com/WeTALKUPC/App_recuperaciones/main/RECUPERACIONES%20FERIADOS%20V1.xlsx"
df = pd.read_excel(DATA_URL, engine="openpyxl")

# Mostrar vista previa de los datos
st.subheader("Vista previa de los datos")
st.write(df.head())

# Filtro por nombre de docente
docente = st.text_input("Ingresa el nombre del docente para buscar:", "")
if docente:
    df = df[df["INSTRUCTOR"].str.contains(docente, case=False, na=False)]

# Lista de feriados
feriados = df.columns[2:-1]  # Excluir columnas no relacionadas con feriados
feriado = st.selectbox("Selecciona un feriado (o TODOS):", ["TODOS"] + list(feriados))

# Limpiar los datos en las columnas seleccionadas
for col in df.columns[2:]:
    df[col] = df[col].str.strip().str.upper()
    df[col] = df[col].replace({
        "NO TENIA CLASES": "NO TENÍA CLASES",
        "NO TENÍA CLASES ": "NO TENÍA CLASES"
    })

# Lista de programas
programas = df["PROGRAMA"].unique()
programa = st.selectbox("Selecciona un programa:", ["TODOS"] + list(programas))

# Filtrar por programa si se selecciona uno específico
if programa != "TODOS":
    df = df[df["PROGRAMA"] == programa]

# Si un feriado específico es seleccionado
if feriado != "TODOS":
    # Calcular el porcentaje de cumplimiento para el feriado seleccionado
    cumplimiento = df[feriado].value_counts(normalize=True) * 100

    # Mostrar gráfico
    st.subheader(f"Cumplimiento para {feriado} ({programa})")
    st.bar_chart(cumplimiento)
else:
    # Mostrar tabla de cumplimiento para todos los feriados
    st.subheader(f"Cumplimiento para todos los feriados ({programa})")
    st.write(df)

# Descargar datos filtrados
st.subheader("Descargar datos filtrados")
csv = df.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv,
    file_name="datos_filtrados.csv",
    mime="text/csv",
)
