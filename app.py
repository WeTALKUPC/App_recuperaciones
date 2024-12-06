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
st.dataframe(df.head(), use_container_width=True)

# Lista de instructores
instructores = df["INSTRUCTOR"].unique()
instructor = st.selectbox("Selecciona un instructor:", ["TODOS"] + list(instructores))

# Lista de feriados
feriados = df.columns[2:-2]  # Excluir columnas no relacionadas con feriados ni observaciones
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
    df_instructor = df[df["INSTRUCTOR"] == instructor]
else:
    df_instructor = df

# Aplicar filtro por programa
if programa != "TODOS":
    df_instructor = df_instructor[df_instructor["PROGRAMA"] == programa]

# Filtrar por estado de cumplimiento
st.subheader("Filtrar por estado de cumplimiento")
estado = st.selectbox("Selecciona un estado:", ["SI", "NO", "NO TENÍA CLASES"])

if estado == "SI":
    resultados = []
    for index, row in df_instructor.iterrows():
        fechas_si = [feriado for feriado in feriados if row[feriado] == "SI"]
        if fechas_si:
            resultados.append([row["INSTRUCTOR"], row["PROGRAMA"], ", ".join(fechas_si)])
    resultados_df = pd.DataFrame(resultados, columns=["INSTRUCTOR", "PROGRAMA", "Fechas de recuperación"])
    st.subheader("Instructores que recuperaron clases:")
    st.dataframe(resultados_df, use_container_width=True)

elif estado == "NO":
    resultados = []
    for index, row in df_instructor.iterrows():
        fechas_no = [feriado for feriado in feriados if row[feriado] == "NO"]
        observaciones = [row["OBSERVACIÓN"] if row[feriado] == "NO" else "" for feriado in feriados]
        if fechas_no:
            resultados.extend([[row["INSTRUCTOR"], row["PROGRAMA"], fecha, obs] for fecha, obs in zip(fechas_no, observaciones) if obs])
    resultados_df = pd.DataFrame(resultados, columns=["INSTRUCTOR", "PROGRAMA", "Feriado", "Observación"])
    st.subheader("Instructores que no recuperaron clases:")
    st.dataframe(resultados_df, use_container_width=True)

elif estado == "NO TENÍA CLASES":
    resultados = []
    for index, row in df_instructor.iterrows():
        fechas_no_clases = [feriado for feriado in feriados if row[feriado] == "NO TENÍA CLASES"]
        if fechas_no_clases:
            resultados.append([row["INSTRUCTOR"], row["PROGRAMA"], ", ".join(fechas_no_clases)])
    resultados_df = pd.DataFrame(resultados, columns=["INSTRUCTOR", "PROGRAMA", "Feriados sin clases"])
    st.subheader("Instructores que no tenían clases:")
    st.dataframe(resultados_df, use_container_width=True)

# Descargar datos filtrados
st.subheader("Descargar datos filtrados")
csv = df_instructor.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv,
    file_name="datos_filtrados.csv",
    mime="text/csv",
)
