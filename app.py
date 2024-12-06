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

# Mostrar resultados
if feriado != "TODOS":
    # Calcular el porcentaje de cumplimiento para el feriado seleccionado
    cumplimiento = df_instructor[feriado].value_counts(normalize=True) * 100

    # Crear colores dinámicos
    colors = ["red" if index == "NO" else "blue" for index in cumplimiento.index]

    # Mostrar gráfico
    st.subheader(f"Cumplimiento para {feriado} ({programa}, {instructor})")
    fig, ax = plt.subplots()
    cumplimiento.plot(kind="bar", color=colors, ax=ax)
    ax.set_title(f"Cumplimiento para {feriado}")
    ax.set_ylabel("Porcentaje")
    ax.set_xlabel("Estado")
    st.pyplot(fig)

    # Mostrar observaciones si hay "NO"
    if "NO" in cumplimiento.index:
        st.subheader("Observaciones")
        observaciones = df_instructor.loc[df_instructor[feriado] == "NO", "OBSERVACIÓN"].dropna().unique()
        for obs in observaciones:
            st.write(f"- {obs}")

else:
    # Mostrar un único gráfico para todos los feriados si se selecciona "TODOS"
    st.subheader(f"Cumplimiento total por feriado ({programa}, {instructor})")
    
    if instructor != "TODOS":
        cumplimiento_total = pd.DataFrame(index=["SI", "NO"])
        for fer in feriados:
            values = df_instructor[fer].value_counts(normalize=True) * 100
            cumplimiento_total[fer] = values.reindex(cumplimiento_total.index, fill_value=0)

        cumplimiento_total = cumplimiento_total.transpose()
        colors = ["blue" if index == "SI" else "red" for index in cumplimiento_total.columns]
        cumplimiento_total.plot(kind="bar", stacked=True, color=colors, figsize=(10, 6))
        
        plt.title(f"Cumplimiento total por feriado para {instructor}")
        plt.xlabel("Feriados")
        plt.ylabel("Porcentaje")
        plt.legend(title="Estado", bbox_to_anchor=(1.05, 1), loc="upper left")
        st.pyplot(plt)
        
        # Mostrar observaciones si hay "NO"
        st.subheader("Observaciones")
        observaciones = df_instructor.loc[:, "OBSERVACIÓN"].dropna().unique()
        for obs in observaciones:
            st.write(f"- {obs}")
    else:
        st.write("Selecciona un instructor o un programa específico para más detalles.")

# Descargar datos filtrados
st.subheader("Descargar datos filtrados")
csv = df_instructor.to_csv(index=False)
st.download_button(
    label="Descargar CSV",
    data=csv,
    file_name="datos_filtrados.csv",
    mime="text/csv",
)
