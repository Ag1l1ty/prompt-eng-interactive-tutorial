import streamlit as st
from utils.components import init_session, render_sidebar

st.set_page_config(
    page_title="Tutorial de Ingenieria de Prompts",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session()
render_sidebar()

st.title("Tutorial Interactivo de Ingenieria de Prompts")

st.markdown("""
> Basado en el [tutorial original de Anthropic](https://github.com/anthropics/prompt-eng-interactive-tutorial)
> -- Traducido al espanol, actualizado a Claude Opus 4.6, y reestructurado para 2026.

---

### Como usar este tutorial

1. **Ingresa tu clave API** de Anthropic en la barra lateral
2. **Navega** por los capitulos usando el menu lateral
3. **Lee las lecciones** y completa los **ejercicios interactivos**
4. Usa las **pistas** si te quedas atascado

---

### Estructura del Curso
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
#### Fundamentos
| Cap | Tema |
|-----|------|
| 1 | Ser Claro y Directo |
| 2 | Estructurar con XML Tags |
| 3 | Formato de Output y Prefill |
| 4 | Ejemplos y Few-Shot |
| 5 | Evitar Alucinaciones |
""")

with col2:
    st.markdown("""
#### Avanzado
| Cap | Tema |
|-----|------|
| 6 | Prompts Complejos desde Cero |
| 7 | Pensamiento Extendido |
| 8 | System Prompts Avanzados |
| 9 | Herramientas y Agentes |
| 10 | RAG: Busqueda y Recuperacion |
""")

st.divider()

if not st.session_state.get("api_key"):
    st.warning("Ingresa tu clave API de Anthropic en la barra lateral para comenzar.")
else:
    st.success(
        f"Clave API configurada. Selecciona un capitulo en el menu lateral para comenzar. "
        f"Progreso: {len(st.session_state.completed)}/24 ejercicios completados."
    )
