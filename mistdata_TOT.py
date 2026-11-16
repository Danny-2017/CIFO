import streamlit as st
import pandas as pd
import plotly.express as px
@st.cache_data
# Bloc d'inicialització amb la carrega del fitxer CSV i els valors inicials de les variables---------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
def cargar_datos():
    df=pd.read_csv("./dat/Data_TOT_2025.csv", sep=";", encoding="UTF-8")
    df['PRODUCTO'] = df['PRODUCTO'].str.strip()
    df['ENTIDAD'] = df['ENTIDAD'].str.strip()
    st.session_state.df = df
    st.session_state.cargado=True
    return df

if "cargado" not in st.session_state:
    df= cargar_datos()
    st.session_state.selectl1 = "NACIONAL (G)"
    st.session_state.selectl2 = ["PROD5","PROD6","PROD7"]
    st.session_state.selectb1 = "TOT"
    st.session_state.selectp1 = "Año"
else:    
    df=st.session_state.df

if "selectl1" in st.session_state : selectl1 = st.session_state.selectl1;
if "selectl2" in st.session_state : selectl2 = st.session_state.selectl2;
if "selectb1" in st.session_state : selectb1 = st.session_state.selectb1;
if "selectp1" in st.session_state : selectp1 = st.session_state.selectp1;

# Creació de la jerarquía territorial per facilitar la selecció per nivells i no presentar sumas duplicades-------------------------
#-----------------------------------------------------------------------------------------------------------------------------------
df_nacional = df[df['ENTIDAD'] == 'NACIONAL (G)']
df_ccaa = df[df['ENTIDAD'].str.endswith('CCAA')]
df_provincies = df[~df['ENTIDAD'].str.endswith('CCAA') & (df['ENTIDAD'] != 'NACIONAL (G)')]
Entitats = df['ENTIDAD'].unique()
Prods = df['PRODUCTO'].unique()

# Preparació de la variable mesos per representar les columnes en pantalla en el seu ordre natural
mesos = ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 
         'Octubre', 'Noviembre', 'Diciembre']
mesosA = ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 
         'Octubre', 'Noviembre', 'Diciembre', 'Año']



# Filtre combinat per nivel territorial i producte
# productos_elegidos = ['PRESENTACIÓN2_2_2', 'PRESENTACIÓN2_2_3']
df_filtrado = df[
     (df['ENTIDAD'] == selectl1) & 
     (df['PRODUCTO'].isin(selectl2))
]

# Gráfic 11111111111111111111111111111 de la evolució mensual (Líneas)____________________________________________
#_________________________________________________________________________________________________________________
df_mesos = df_filtrado.melt(
    id_vars=['PRODUCTO', 'ENTIDAD'], 
    value_vars=mesos, 
    var_name='Mes', 
    value_name='Vendes en €'
)

fig1 = px.line(
    df_mesos, 
    x='Mes', 
    y='Vendes en €', 
    color='PRODUCTO', 
    markers=True,
    title=f'Gràfic 1: Evolució mensual a nivel {selectl1} per productes escollits'
)


# Gràfic 22222222222222222222222222222222comparativo del total anual (Barras) d'un producte concret.______________
#_________________________________________________________________________________________________________________
df_barres = df_ccaa[df_ccaa['PRODUCTO'] == st.session_state.selectb1].sort_values('Año', ascending=False)

fig2 = px.bar(
    df_barres, 
    x='ENTIDAD', 
    y='Año', 
    title=f'Gràfic 2: Total Anual por Comunitat Autònoma y producte {st.session_state.selectb1}',
    labels={'ENTIDAD': 'Comunidad Autónoma', 'Año': 'Total Anual en €'}
)
# Gràfic 33333333333333333333333333  pastís________________________________________________________________________
#__________________________________________________________________________________________________________________
df_pastel = df[
    (df['ENTIDAD'] == selectl1) & 
    (df['PRODUCTO'].str.startswith('PROD'))
]

# 3. Crear el gráfico de pastel usando la columna 'Año'
fig3 = px.pie(
    df_pastel, 
    values=selectp1, 
    names='PRODUCTO', 
    title=f'Gràfic 3: Cuota del periode {selectp1} per Producte a nivel {selectl1}'
)
# Opcional: Mostrar tanto el porcentaje como el nombre en cada porción
fig3.update_traces(textposition='inside', textinfo='percent+label')

# Gràfic 4444444444444444444444444444  heatmap_______________________________________________________________________
#____________________________________________________________________________________________________________________
#periodo = "Año"
df = df[df["PRODUCTO"].str.contains("PROD", case=False, na=False)]
df_filtrado = df[df["ENTIDAD"].str.endswith("CCAA")].copy()
df_filtrado["ENTIDAD"] = df_filtrado["ENTIDAD"].str.replace(" CCAA", "")

# Preparar la matriu per el Heatmap (Territorio en Y, Producto en X)
matriz = df_filtrado.pivot(index="ENTIDAD", columns="PRODUCTO", values=selectp1)


fig4 = px.imshow(
    matriz,
    labels=dict(x="Producte", y="Territori", color="Vendes en €"),
    x=matriz.columns,
    y=matriz.index,
    color_continuous_scale="YlOrRd",  # Escala de amarillo a rojo intenso
    text_auto=True,                   # Muestra los números dentro de cada celda
    aspect="auto"
)

# Ajustar el tamany del gràfic 
altura = 1100 
fig4.update_layout(height=altura, xaxis_side="top")



#----------------------------------------------------------------------------------------------------------
# Pantalal de streamlit------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------

st.title ("Informe producte TOT")
tab1, tab2 = st.tabs(
    ["📥 Gràfics de Vendes", "🔍 Estadístic de Vendes"]
    )

with st.sidebar:
    st.metric(label="Resum de vendes", value="Any 2025", delta="increment +2%")
    st.session_state.selectl1 = st.selectbox("Territori a seleccionar G1", Entitats, index=71)
    st.session_state.selectl2 = st.multiselect("Quins productes desitjeu G1", Prods, default=["PROD5","PROD6","PROD7"])
    st.session_state.selectb1 = st.selectbox("Quin producte escolliu G2", Prods, index=22)
    st.session_state.selectp1 = st.selectbox("Sobre quin periode calculem G3/G4:", mesosA, index=12)
    st.write("CIFO project @")
    selectl1 = st.session_state.selectl1;
    selectl2 = st.session_state.selectl2;
    selectb1 = st.session_state.selectb1;
    selectp1 = st.session_state.selectp1;
    
with tab1:
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
  

with tab2:
    st.text(f'Gràfic 4: Mapa de calor vendes per provincies y territori per el periode {selectp1}')
    st.plotly_chart(fig4)
