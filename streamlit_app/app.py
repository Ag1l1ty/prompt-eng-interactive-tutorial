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
> -- Traducido al espanol, actualizado a Claude Opus 4.6, y ampliado con capitulos nuevos.

---

### Como usar este tutorial

1. **Ingresa tu clave API** de Anthropic en la barra lateral
2. **Navega** por los capitulos usando el menu lateral
3. **Lee las lecciones** y completa los **ejercicios interactivos**
4. Usa los **hints** si te quedas atascado

**Nota:** Los prompts de ejemplo se mantienen en ingles (mejores resultados con Claude).
Las explicaciones estan en espanol.

---

### Estructura del Curso
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
#### Principiante
| Cap | Tema |
|-----|------|
| 1 | Estructura Basica de Prompts |
| 2 | Ser Claro y Directo |
| 3 | Asignacion de Roles |

#### Intermedio
| Cap | Tema |
|-----|------|
| 4 | Separar Datos de Instrucciones |
| 5 | Formato de Output y Hablar por Claude |
| 6 | Precognicion (Pensar Paso a Paso) |
| 7 | Uso de Ejemplos (Few-Shot) |
""")

with col2:
    st.markdown("""
#### Avanzado
| Cap | Tema |
|-----|------|
| 8 | Evitar Alucinaciones |
| 9 | Prompts Complejos desde Cero |
| 10 | Pensamiento Extendido |
| 11 | System Prompts Avanzados |

#### Apendices
| Ap | Tema |
|----|------|
| 12.1 | Encadenamiento de Prompts |
| 12.2 | Uso de Herramientas (Tool Use) |
| 12.3 | Busqueda y Recuperacion |
""")

st.divider()

if not st.session_state.get("api_key"):
    st.warning("Ingresa tu clave API de Anthropic en la barra lateral para comenzar.")
else:
    st.success(
        f"Clave API configurada. Selecciona un capitulo en el menu lateral para comenzar. "
        f"Progreso: {len(st.session_state.completed)}/26 ejercicios completados."
    )
