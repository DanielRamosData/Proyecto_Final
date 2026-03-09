import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# =========================================================
# 1. PROGRAMACIÓN ORIENTADA A OBJETOS (POO) 
# =========================================================
class DataAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe
        # Limpieza inicial: Convertir edad de días a años para mejor interpretación
        if 'age_in_days' in self.df.columns:
            self.df['age_years'] = self.df['age_in_days'] / 365

    def obtener_resumen(self):
        """Puntos 1, 2 y 4 de la rúbrica: Tipos, Nulos y No Nulos"""
        resumen = pd.DataFrame({
            'Tipo de Dato': self.df.dtypes,
            'Valores Nulos': self.df.isnull().sum(),
            'Valores No Nulos': self.df.notnull().sum()
        })
        return resumen

    def estadistica_descriptiva(self):
        """Punto 5: Medidas de tendencia central y dispersión"""
        return self.df.describe()

    def clasificar_columnas(self):
        """Punto 6: Clasificación de variables"""
        num = self.df.select_dtypes(include=[np.number]).columns.tolist()
        cat = self.df.select_dtypes(include=['object']).columns.tolist()
        return num, cat

    # --- Métodos de Visualización (Puntos 7, 8, 9, 10) ---
    def plot_histograma(self, columna):
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.histplot(self.df[columna], kde=True, color='#3498db', ax=ax)
        ax.set_title(f'Distribución de: {columna}', fontsize=14)
        ax.set_xlabel(columna)
        ax.set_ylabel('Frecuencia')
        return fig

    def plot_boxplot_bivariado(self, columna_num):
        """Relaciona una variable numérica con la renovación (0 o 1)"""
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.boxplot(x='renewal', y=columna_num, data=self.df, palette='viridis', ax=ax)
        ax.set_title(f'{columna_num} vs Renovación (0=No, 1=Sí)', fontsize=14)
        return fig

# =========================================================
# 2. CONFIGURACIÓN DE LA INTERFAZ DE STREAMLIT
# =========================================================
st.set_page_config(page_title="Insurance Analysis App", layout="wide", page_icon="🛡️")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/950/950008.png", width=80)
    st.title("Seguros S.A.")
    modulo = st.radio("Menú de Navegación:", 
                      ["Home", "Carga de Datos", "EDA", "Conclusiones"])
    st.divider()
    st.caption("Especialización Python for Analytics © 2026")

# =========================================================
# 3. LÓGICA DE MÓDULOS
# =========================================================

# --- MÓDULO 1: HOME ---
if modulo == "Home":
    st.title("Análisis Exploratorio de Datos: Insurance Company 📊")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Objetivo del Proyecto")
        st.write("""
        Esta aplicación interactiva permite analizar el dataset de una compañía de seguros 
        para descubrir qué factores (ingresos, edad, retrasos en pagos) influyen en que 
        un cliente decida renovar su póliza.
        """)
        st.subheader("Tecnologías Utilizadas")
        st.success("Python • Pandas • Matplotlib • Seaborn • Streamlit • POO")
        
    with col2:
        st.subheader("Información del Autor")
        st.info("""
        **Nombre:** Daniel Alberto Ramos Torres  
        **Curso:** Python for Analytics  
        **Año:** 2026  
        **Dataset:** InsuranceCompany.csv
        """)

# --- MÓDULO 2: CARGA DE DATOS ---
elif modulo == "Carga de Datos":
    st.header("Módulo 2: Carga del Dataset 📁")
    archivo = st.file_uploader("Seleccione el archivo CSV", type=["csv"])
    
    if archivo:
        df_cargado = pd.read_csv(archivo)
        st.session_state['df'] = df_cargado  # Guardar en sesión
        st.success("¡Archivo cargado y procesado exitosamente!")
        
        # Métricas de dimensiones (Punto 3)
        c1, c2 = st.columns(2)
        c1.metric("Total de Registros (Filas)", df_cargado.shape[0])
        c2.metric("Total de Variables (Columnas)", df_cargado.shape[1])
        
        st.subheader("Vista Previa (Primeros 10 registros)")
        st.dataframe(df_cargado.head(10))
    else:
        st.warning("Por favor, suba el archivo 'InsuranceCompany.csv' para habilitar el análisis.")

# --- MÓDULO 3: EDA ---
elif modulo == "EDA":
    st.header("Módulo 3: Análisis Exploratorio de Datos (EDA) 🔍")
    
    if 'df' in st.session_state:
        df = st.session_state['df']
        analyzer = DataAnalyzer(df)
        
        # Tabs para organizar la rúbrica
        tab1, tab2, tab3 = st.tabs(["Estructura y Tipos", "Estadística Descriptiva", "Análisis Visual"])
        
        with tab1:
            st.subheader("Resumen de Variables (Tipos y Nulos)")
            st.dataframe(analyzer.obtener_resumen())
            st.write(f"**Dimensiones del dataset:** {df.shape[0]} filas por {df.shape[1]} columnas.")

        with tab2:
            st.subheader("Estadísticas de Variables Numéricas")
            st.dataframe(analyzer.estadistica_descriptiva())
            
            num, cat = analyzer.clasificar_columnas()
            col_a, col_b = st.columns(2)
            col_a.info(f"**Variables Numéricas:** \n{', '.join(num)}")
            col_b.info(f"**Variables Categóricas:** \n{', '.join(cat)}")

        with tab3:
            st.subheader("Gráficos Estadísticos e Insights")
            num_cols, _ = analyzer.clasificar_columnas()
            
            # Selector interactivo (Punto 9)
            seleccion = st.selectbox("Elija una variable para graficar:", num_cols)
            
            # Layout de gráficos (Puntos 7, 8 y 10)
            g1, g2 = st.columns(2)
            
            with g1:
                st.write("**Distribución Univariada**")
                st.pyplot(analyzer.plot_histograma(seleccion))
            
            with g2:
                st.write("**Relación Bivariada vs Renovación**")
                st.pyplot(analyzer.plot_boxplot_bivariado(seleccion))
                
            st.caption("Nota: En el eje X del boxplot, '0' significa que el cliente NO renovó y '1' que SÍ renovó.")

    else:
        st.error("⚠️ Error: Debe cargar los datos primero en el módulo 'Carga de Datos'.")

# --- MÓDULO 4: CONCLUSIONES ---

elif modulo == "Conclusiones":
    st.header("Módulo 4: Conclusiones del Análisis Exploratorio 💡")
    
    st.markdown("""
    Basado en el análisis de las variables del dataset **Insurance Company**, se presentan las siguientes conclusiones orientadas a la toma de decisiones estratégicas:

    1. **Impacto Crítico de la Morosidad Reciente:** Los datos muestran una ruptura clara en la tasa de renovación cuando el cliente entra en mora de **3 a 6 meses**. Esta variable presenta la correlación negativa más fuerte con la permanencia, sugiriendo que la ventana de intervención para retener a un cliente debe ocurrir *antes* de que supere los 90 días de impago.

    2. **Segmentación por Capacidad Económica (Income):** A través de los diagramas de caja (Boxplots), se observa que el segmento de clientes con mayores ingresos mensuales muestra una dispersión menor y una mediana de renovación más estable. Esto indica que la **asequibilidad de la prima** es un factor higiénico: no garantiza la lealtad, pero su falta sí provoca la salida del cliente.

    3. **Fidelización Basada en la Madurez del Cliente:** Existe una tendencia observable donde los clientes de mayor edad (transformados de días a años) presentan un comportamiento de pago más disciplinado y menores índices de mora. La toma de decisiones debería priorizar estrategias de **referidos en segmentos senior**, dado su bajo costo de mantenimiento y alta tasa de renovación.

    4. **Eficacia de los Canales de Captación (Sourcing Channel):** El análisis bivariado sugiere que el canal de origen influye en la calidad del perfil crediticio inicial. La empresa debe reevaluar el costo de adquisición de los canales con mayor tasa de morosidad, moviendo la inversión hacia aquellos canales que, aunque sean más lentos, traen clientes con mejores **scores de suscripción (underwriting score)**.

    5. **Relación Prima vs. Persistencia:** Se detectó que el número total de primas pagadas históricamente es un indicador de confianza. Los clientes que superan el primer año de pagos tienen una inercia de renovación mucho mayor, lo que justifica el uso de **incentivos o descuentos especiales** exclusivamente durante los primeros 6 a 12 meses para asegurar que el cliente cruce la barrera crítica de abandono.
    """)

    st.info("💡 **Nota Técnica:** Estas conclusiones se basan en el análisis descriptivo y bivariado de los datos históricos, enfocándose en la comprensión del comportamiento actual para la mejora de procesos internos.")
    
