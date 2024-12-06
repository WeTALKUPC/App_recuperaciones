import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del Dashboard
st.title("Dashboard de Cumplimiento por Feriado y Programa")

# Cargar el archivo Excel directamente desde el repositorio
DATA_URL = "https://raw.githubusercontent.com/WeTALKUPC/App_recuperaciones/main/RECUPERACIONES%20FERIADOS%20V1.xlsx"
df = pd.read_excel(DATA_URL, engine="openpyxl")

# Limpiar los datos
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
df.replace("NO TENIA CLASES", "NO TENÍA CLASES", inplace=True)

# Mostrar vista previa de los datos
st.subheader("Vista previa de los datos")
st.write(df.head())

# Lista de feriados
feriados = df.columns[2:-1]
feriado = st.selectbox("Selecciona un feriado:", ["TODOS"] + list(feriados))

# Lista de instructores
instructores = df["INSTRUCTOR"].unique()
instructor = st.selectbox("Selecciona un instructor:", ["TODOS"] + list(instructores))

# Filtrar por instructor si se selecciona uno específico
if instructor != "TODOS":
    df_instructor = df[df["INSTRUCTOR"] == instructor]
else:
    df_instructor = df

# Mostrar resultados
if feriado == "TODOS":
    st.subheader(f"Cumplimiento total por feriado para {instructor}")
    cumplimiento_total = df_instructor[feriados].apply(pd.Series.value_counts, normalize=True).T * 100
    cumplimiento_total = cumplimiento_total.fillna(0)
    
    # Crear gráfico con colores y etiquetas
    fig, ax = plt.subplots(figsize=(10, 6))
    cumplimiento_total.plot(kind="bar", stacked=True, color=["blue", "red", "gray"], ax=ax)
    
    for p in ax.patches:
        if p.get_height() > 0:
            ax.annotate(
                f"{p.get_height():.1f}%",
                (p.get_x() + p.get_width() / 2., p.get_y() + p.get_height() / 2.),
                ha="center", va="center", fontsize=8, color="white"
            )
    
    ax.set_title(f"Cumplimiento total por feriado para {instructor}")
    ax.set_ylabel("Porcentaje")
    ax.set_xlabel("Feriados")
    ax.legend(title="Estado", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.subheader(f"Cumplimiento para {feriado} ({instructor})")
    cumplimiento = df_instructor[feriado].value_counts(normalize=True) * 100
    
    # Crear gráfico con colores y etiquetas
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"SI": "blue", "NO": "red", "NO TENÍA CLASES": "gray"}
    cumplimiento.plot(kind="bar", color=[colors.get(x, "gray") for x in cumplimiento.index], ax=ax)
    
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.1f}%",
            (p.get_x() + p.get_width() / 2., p.get_height() / 2.),
            ha="center", va="center", fontsize=10, color="white"
        )
    
    ax.set_title(f"Cumplimiento para {feriado} ({instructor})")
    ax.set_ylabel("Porcentaje")
    ax.set_xlabel("Estado")
    plt.xticks(rotation=0)
    st.pyplot(fig)

# Mostrar observaciones
st.subheader("Observaciones")
observaciones = df_instructor.loc[:, "OBSERVACIÓN"].dropna().unique()
if len(observaciones) > 0:
    for obs in observaciones:
        st.markdown(f"- **{obs}**")
else:
    st.write("No hay observaciones disponibles.")
