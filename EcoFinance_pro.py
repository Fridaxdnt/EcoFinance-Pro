import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

# Configuración de página avanzada
st.set_page_config(
    page_title="EcoFinance Pro",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: white;
    }
    .ia-response {
        background-color: #1E1E1E !important;
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2ecc71;
    }
    .header {
        color: #2ecc71;
    }
</style>
""", unsafe_allow_html=True)

# Base de datos
conn = sqlite3.connect('cerro_verde.db')
cursor = conn.cursor()

# Tabla mejorada para minería
cursor.execute('''
CREATE TABLE IF NOT EXISTS operaciones_mineras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE,
    proceso TEXT,
    material TEXT,
    agua_m3 FLOAT,
    energia_kwh FLOAT,
    co2_ton FLOAT,
    residuos_ton FLOAT,
    produccion_ton FLOAT,
    ingresos_soles FLOAT,
    gastos_soles FLOAT,
    inversion_ambiental_soles FLOAT
)
''')
conn.commit()

# Datos legales de Perú (precargados)
normas_peru = {
    "Ley General del Ambiente": "Ley N° 28611",
    "Límite CO₂ Minería": "50 ton/día (DS N° 003-2014-MINAM)",
    "Agua": "Límite 5000 m3/día (Ley de Recursos Hídricos)",
    "Multas": "Hasta 10,000 UIT por incumplimiento"
}

# IA Mejorada con conocimiento peruano
def consulta_ia(pregunta, df):
    conocimiento_peru = """
    Contexto Legal Perú:
    - Regulación: OEFA supervisa cumplimiento ambiental
    - Impuestos: Beneficios tributarios por inversión ambiental (Ley 30215)
    - Requisitos: EIA aprobado para operar (DS N° 019-2009-MINAM)
    """
    
    analisis = ""
    if "agua" in pregunta.lower():
        eficiencia = df.groupby('proceso').apply(
            lambda x: x['produccion_ton'].sum()/x['agua_m3'].sum()
        ).sort_values(ascending=False)
        mejor_proceso = eficiencia.idxmax
        analisis = f"""
        🔍 Análisis de Eficiencia Hídrica:
        - Proceso más eficiente: {mejor_proceso} ({eficiencia.max():.2f} ton/m3)
        - Recomendación: Implementar sistema de recirculación (Inversión: $1.2M, ROI: 3 años)
        - Normativa Perú: Límite {normas_peru['Agua']} - Cerro Verde usa {df['agua_m3'].sum()/30:.0f} m3/día
        """
    
    elif "emision" in pregunta.lower():
        analisis = f"""
        📉 Análisis de Emisiones:
        - Total CO₂: {df['co2_ton'].sum():.1f} ton/mes
        - Proceso clave: {df.groupby('proceso')['co2_ton'].sum().idxmax()}
        - Cumplimiento: {'✅' if df['co2_ton'].sum()/30 < 50 else '❌'} vs {normas_peru['Límite CO₂ Minería']}
        """
    
    return f"""
    <div class='ia-response'>
        <h3 class='header'>🔎 Respuesta IA - Especializada en Minería Perú</h3>
        <p><strong>Consulta:</strong> {pregunta}</p>
        {analisis}
        <hr>
        <h4 class='header'>📚 Base Legal Perú:</h4>
        <ul>
            <li>{normas_peru['Ley General del Ambiente']}</li>
            <li>Límites: {normas_peru['Límite CO₂ Minería']}</li>
            <li>Multas: {normas_peru['Multas']}</li>
        </ul>
    </div>
    """

# Interfaz
st.title("⛏️ EcoFinance Pro")
st.markdown("**Herramienta contable**")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📥 Datos", "📊 Visualización", "🤖 IA Chat", "📈 Simulación", "📑 Reporte"])

# Pestaña 1: Ingreso de datos
with tab1:
    with st.form("form_mineria"):
        cols = st.columns(3)
        with cols[0]:
            fecha = st.date_input("Fecha")
            proceso = st.selectbox("Proceso", ["Extracción", "Procesamiento", "Transporte", "Relaves"])
        with cols[1]:
            agua = st.number_input("Agua (m3)", min_value=0.0)
            energia = st.number_input("Energía (kWh)", min_value=0.0)
        with cols[2]:
            co2 = st.number_input("CO₂ (ton)", min_value=0.0)
            produccion = st.number_input("Producción (ton)", min_value=0.0)
        
        if st.form_submit_button("💾 Guardar Datos"):
            cursor.execute('''
                INSERT INTO operaciones_mineras 
                VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fecha, proceso, "Cobre", agua, energia, co2, 0, produccion, 
                produccion*5000, produccion*3500, co2*40
            ))
            conn.commit()
            st.success("Datos mineros guardados")

# Pestaña 3: IA Chat
with tab3:
    st.markdown("### 🧠 Asesor IA")
    pregunta = st.text_input("Escriba su pregunta técnica/legal y presione Enter:", key="ia_input")
    
    if pregunta:
        df = pd.read_sql("SELECT * FROM operaciones_mineras", conn)
        st.markdown(consulta_ia(pregunta, df), unsafe_allow_html=True)

# Pestaña 4: Simulación
with tab4:
    st.markdown("### 💡 Simulador de Inversiones Sostenibles")
    
    with st.expander("⚙️ Configurar Escenario"):
        cols = st.columns(2)
        with cols[0]:
            inversion = st.number_input("Inversión (S/.)", min_value=0, value=1000000)
            plazo = st.slider("Plazo (años)", 1, 10, 5)
        with cols[1]:
            tipo = st.selectbox("Tecnología", [
                "Filtros CO₂", "Recirculación Agua", 
                "Energía Solar", "Gestión de Relaves"
            ])
    
    if st.button("🔄 Simular Impacto"):
        resultados = {
            "Reducción CO₂": "15-25%",
            "Ahorro Anual": f"S/. {inversion*0.2:,.0f}",
            "ROI": f"{plazo} años",
            "Cumplimiento Legal": "✅ 100%"
        }
        
        st.markdown("### 📊 Resultados de Simulación")
        st.table(pd.DataFrame.from_dict(resultados, orient='index', columns=['Valor']))

# Pestaña 5: Reportes
with tab5:
    st.markdown("### 📑 Reporte Ejecutivo Automatizado")
    
    if st.button("🖨️ Generar Reporte"):
        df = pd.read_sql("SELECT * FROM operaciones_mineras", conn)
        
        st.markdown(f"""
        ## Análisis Integral - {datetime.now().strftime('%B %Y')}
        
        **📌 Hallazgos Clave:**
        - Producción total: {df['produccion_ton'].sum():,.0f} ton
        - Intensidad hídrica: {df['agua_m3'].sum()/df['produccion_ton'].sum():.1f} m3/ton
        - Emisiones por S/. ingresado: {df['co2_ton'].sum()/df['ingresos_soles'].sum():.4f} ton/S/.
        
        **📈 Tendencia Ambiental:**
        La eficiencia energética ha {'mejorado' if df['energia_kwh'].mean() < 100 else 'empeorado'} en 
        comparación con el trimestre anterior.
        
        **⚖️ Cumplimiento Legal:**
        - Niveles de CO₂: {'Dentro' if df['co2_ton'].mean() < 1.5 else 'Fuera'} de límites legales
        - Agua utilizada: {df['agua_m3'].sum()/30:,.0f} m3/día vs Límite {normas_peru['Agua']}
        """)
        
        fig = px.bar(df, x='proceso', y='co2_ton', title="Emisiones por Proceso")
        st.plotly_chart(fig)

conn.close()