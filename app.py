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

# Sección: Mostrar instructores que no recuperaron clases
st.subheader("Instructores que no recuperaron clases")

# Filtrar los instructores con al menos un "NO"
instructores_no = df.loc[df.iloc[:, 2:-1].eq("NO").any(axis=1), ["INSTRUCTOR", "PROGRAMA"]]

# Agregar observaciones específicas para estos instructores
instructores_no["Observaciones"] = df.loc[df.iloc[:, 2:-1].eq("NO").any(axis=1), "OBSERVACIÓN"]

# Mostrar tabla interactiva con instructores y observaciones
st.write("A continuación, se muestran los instructores que no recuperaron clases en algún feriado:")
st.dataframe(instructores_no)

# Filtro adicional por programa
programa_filtro = st.selectbox("Filtrar por programa:", ["TODOS"] + list(df["PROGRAMA"].unique()))
if programa_filtro != "TODOS":
    instructores_no = instructores_no[instructores_no["PROGRAMA"] == programa_filtro]
    st.write(f"Instructores filtrados por programa: {programa_filtro}")
    st.dataframe(instructores_no)

# Descarga de la tabla filtrada
st.subheader("Descargar lista de instructores que no recuperaron clases")
csv_no = instructores_no.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv_no,
    file_name="instructores_no_recuperaron.csv",
    mime="text/csv",
)

# Incluir la funcionalidad anterior (cumplimiento por instructor y feriado)
# Lista de instructores
st.subheader("Consulta por instructor, feriado y programa")
instructores = df["INSTRUCTOR"].unique()
instructor = st.selectbox("Selecciona un instructor:", ["TODOS"] + list(instructores))

# Lista de feriados
feriados = df.columns[2:-1]  # Excluir columna de observaciones
feriado = st.selectbox("Selecciona un feriado (o TODOS):", ["TODOS"] + list(feriados))

# Lista de programas
programas = df["PROGRAMA"].unique()
programa = st.selectbox("Selecciona un programa:", ["TODOS"] + list(programas))

# Aplicar filtros y mostrar resultados como en la implementación previa
if instructor != "TODOS":
    df_instructor = df[df["INSTRUCTOR"] == instructor]
else:
    df_instructor = df

if programa != "TODOS":
    df_instructor = df_instructor[df_instructor["PROGRAMA"] == programa]

if feriado != "TODOS":
    cumplimiento = df_instructor[feriado].value_counts(normalize=True) * 100
    colors = ["red" if index == "NO" else "blue" if index == "SI" else "gray" for index in cumplimiento.index]
    st.subheader(f"Cumplimiento para {feriado} ({programa}, {instructor})")
    fig, ax = plt.subplots()
    cumplimiento.plot(kind="bar", color=colors, ax=ax)
    ax.set_title(f"Cumplimiento para {feriado}")
    ax.set_ylabel("Porcentaje")
    ax.set_xlabel("Estado")
    st.pyplot(fig)

    if "NO" in cumplimiento.index:
        st.subheader("Observaciones")
        observaciones = df_instructor.loc[df_instructor[feriado] == "NO", "OBSERVACIÓN"].dropna().unique()
        for obs in observaciones:
            st.write(f"- {obs}")
else:
    st.subheader(f"Cumplimiento total por feriado ({programa}, {instructor})")
    if instructor != "TODOS":
        cumplimiento_total = pd.DataFrame(index=["SI", "NO", "NO TENÍA CLASES"])
        for fer in feriados:
            values = df_instructor[fer].value_counts(normalize=True) * 100
            cumplimiento_total[fer] = values.reindex(cumplimiento_total.index, fill_value=0)

        cumplimiento_total = cumplimiento_total.transpose()
        colors = ["blue" if index == "SI" else "red" if index == "NO" else "gray" for index in cumplimiento_total.columns]
        cumplimiento_total.plot(kind="bar", stacked=True, color=colors, figsize=(10, 6))
        plt.title(f"Cumplimiento total por feriado para {instructor}")
        plt.xlabel("Feriados")
        plt.ylabel("Porcentaje")
        plt.legend(title="Estado", bbox_to_anchor=(1.05, 1), loc="upper left")
        st.pyplot(plt)

        st.subheader("Observaciones")
        observaciones = df_instructor["OBSERVACIÓN"].dropna().unique()
        for obs in observaciones:
            st.write(f"- {obs}")
    else:
        st.write("Selecciona un instructor o un programa específico para más detalles.")
