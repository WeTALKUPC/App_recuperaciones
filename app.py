import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del Dashboard
st.title("Dashboard de Cumplimiento por Feriado, Programa e Instructor")

# Cargar el archivo Excel directamente desde el repositorio
DATA_URL = "https://raw.githubusercontent.com/WeTALKUPC/App_recuperaciones/main/RECUPERACIONES%20FERIADOS%20V1.xlsx"
df = pd.read_excel(DATA_URL, engine="openpyxl")

# Mostrar vista previa de los datos
st.subheader("Vista previa de los datos")
st.write(df.head())

# Lista de instructores
instructores = df["INSTRUCTOR"].unique()
instructor = st.selectbox("Selecciona un instructor:", ["TODOS"] + list(instructores))

# Lista de feriados
feriados = df.columns[2:-1]  # Excluir columnas no relacionadas con feriados
feriado = st.selectbox("Selecciona un feriado (o TODOS):", ["TODOS"] + list(feriados))

# Lista de programas
programas = df["PROGRAMA"].unique()
programa = st.selectbox("Selecciona un programa:", ["TODOS"] + list(programas))

# Limpiar los datos en las columnas seleccionadas
for col in df.columns[2:]:
    df[col] = df[col].str.strip().str.upper()
    df[col] = df[col].replace({
        "NO TENIA CLASES": "NO TENÍA CLASES",
        "NO TENÍA CLASES ": "NO TENÍA CLASES"
    })

# Aplicar filtro por instructor
if instructor != "TODOS":
    df = df[df["INSTRUCTOR"] == instructor]

# Aplicar filtro por programa
if programa != "TODOS":
    df = df[df["PROGRAMA"] == programa]

# Mostrar gráfico según el feriado seleccionado
if feriado != "TODOS":
    # Calcular el porcentaje de cumplimiento para el feriado seleccionado
    cumplimiento = df[feriado].value_counts(normalize=True) * 100

    # Mostrar gráfico
    st.subheader(f"Cumplimiento para {feriado} ({programa}, {instructor})")
    st.bar_chart(cumplimiento)
else:
    # Mostrar gráfico de cumplimiento para todos los feriados
    st.subheader(f"Cumplimiento total por feriado ({programa}, {instructor})")
    cumplimiento_total = {}
    for fer in feriados:
        cumplimiento_total[fer] = df[fer].value_counts(normalize=True) * 100

    for fer, data in cumplimiento_total.items():
        st.subheader(f"Cumplimiento para {fer}")
        st.bar_chart(data)

# Descargar datos filtrados
st.subheader("Descargar datos filtrados")
csv = df.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv,
    file_name="datos_filtrados.csv",
    mime="text/csv",
)
