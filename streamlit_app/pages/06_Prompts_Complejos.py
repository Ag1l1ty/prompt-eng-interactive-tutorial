import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion
from utils.data import TAX_CODE

render_sidebar()
st.title("Capitulo 6: Prompts Complejos desde Cero")

render_lesson("""
### Construyendo prompts complejos paso a paso

Hasta ahora hemos visto tecnicas individuales: ser claro, usar XML tags, dar ejemplos,
evitar alucinaciones. Pero en la practica, los mejores prompts **combinan varias
tecnicas** en un solo prompt bien estructurado.

Este capitulo te ensena a construir prompts complejos de forma sistematica.

---

### Estructura recomendada para prompts complejos

No todos los elementos son necesarios siempre. Usa los que apliquen a tu caso:

| # | Elemento | Descripcion | Requerido? |
|---|----------|-------------|------------|
| 1 | **Contexto de la tarea** | Rol y objetivo general | Recomendado |
| 2 | **Tono** | Formal, casual, tecnico, etc. | Opcional |
| 3 | **Reglas e instrucciones** | Restricciones y comportamientos especificos | Si |
| 4 | **Ejemplos (few-shot)** | Pares de entrada/salida deseada | Opcional |
| 5 | **Datos de entrada** | En tags XML (`<documento>`, `<codigo>`, etc.) | Si hay datos |
| 6 | **Tarea inmediata** | La pregunta o accion concreta | Si |
| 7 | **Pensar paso a paso** | Instruccion de razonar antes de responder | Opcional |
| 8 | **Formato de output** | JSON, lista, parrafos, tags, etc. | Recomendado |
| 9 | **Prefill** | Inicio forzado de la respuesta | Opcional |

---

### Ejemplo de prompt complejo

Observa como se combinan los elementos:

> **1. Contexto:** "Eres un asesor fiscal experto en leyes de EE.UU."
>
> **2. Tono:** "Usa lenguaje claro, evitando jerga legal innecesaria."
>
> **3. Reglas:** "Basa tus respuestas SOLO en el codigo fiscal proporcionado.
> Si la respuesta no esta en el documento, dilo claramente."
>
> **4. Datos:** `<codigo_fiscal>` ... texto del codigo ... `</codigo_fiscal>`
>
> **5. Tarea:** "Pregunta del usuario: Cuanto tiempo tengo para hacer una eleccion 83b?"
>
> **6. Paso a paso:** "Primero identifica las secciones relevantes, luego responde."
>
> **7. Formato:** "Responde en maximo 3 parrafos."

---

### El proceso es iterativo, no perfecto

No intentes escribir el prompt perfecto de una sola vez. El proceso recomendado es:

1. **Empieza simple** - Solo la tarea basica
2. **Prueba** - Observa la respuesta
3. **Identifica problemas** - Que falta? Que sobra? Que esta mal?
4. **Agrega elementos** - Reglas, ejemplos, formato, etc.
5. **Repite** - Hasta obtener resultados consistentes

---

### Encadenamiento de prompts

Para tareas **muy complejas** que son dificiles de resolver en un solo prompt, puedes
**dividir el trabajo en pasos** donde el output de un paso alimenta el siguiente:

> **Paso 1:** "Genera un outline de 5 secciones para un articulo sobre IA en medicina."
>
> **Paso 2:** "Dado este outline, expande la seccion 3 con 300 palabras." *(usa el output del paso 1)*
>
> **Paso 3:** "Revisa el texto y corrige errores gramaticales." *(usa el output del paso 2)*

Ventajas del encadenamiento:
- Cada paso es mas simple y controlable
- Puedes inspeccionar y corregir resultados intermedios
- Claude tiene un contexto mas enfocado en cada paso
- Reduces la probabilidad de errores acumulados

Al final de este capitulo hay un **demo interactivo** de encadenamiento.
""")

st.divider()
st.header("Ejercicios")

# ══════════════════════════════════════════════════════════════
# Ejercicio 6.1 - Asesor Fiscal
# ══════════════════════════════════════════════════════════════
st.subheader("Ejercicio 6.1 - Asesor Fiscal")
st.markdown("""
Construye un prompt complejo paso a paso para crear un **asesor fiscal** que responda
preguntas sobre el codigo tributario de EE.UU. (Seccion 83 del IRC).

Rellena los campos de abajo para armar tu prompt. Al hacer clic en **Ejecutar**,
todos los campos se combinan y se envian a Claude.

**Pregunta a responder:** "Cuanto tiempo tengo para hacer una eleccion 83b?"

*La respuesta correcta es **30 dias** despues de la transferencia de la propiedad.*
""")

with st.expander("Ver codigo fiscal de referencia (Seccion 83 IRC)"):
    st.text(TAX_CODE[:2000] + "\n\n... [documento completo incluido automaticamente] ...")
    st.code(TAX_CODE, language=None)

sys_prompt_6_1 = st.text_area(
    "1. System prompt (rol / contexto)",
    value="",
    height=84,
    key="input_6.1_system",
    placeholder="Ej: Eres un asesor fiscal experto en leyes tributarias de EE.UU.",
)

tono_6_1 = st.text_area(
    "2. Tono (opcional)",
    value="",
    height=56,
    key="input_6.1_tono",
    placeholder="Ej: Usa lenguaje claro y accesible, evitando jerga legal innecesaria.",
)

reglas_6_1 = st.text_area(
    "3. Reglas e instrucciones",
    value="",
    height=112,
    key="input_6.1_reglas",
    placeholder="Ej: Basa tus respuestas SOLO en el codigo fiscal proporcionado.\nSi la respuesta no esta en el documento, dilo claramente.\nCita las secciones relevantes.",
)

ejemplos_6_1 = st.text_area(
    "4. Ejemplos (opcional)",
    value="",
    height=84,
    key="input_6.1_ejemplos",
    placeholder="Ej: Pregunta: Que es una restriccion que nunca caduca?\nRespuesta: Segun la seccion (d), es una restriccion que por sus terminos nunca expira...",
)

pregunta_6_1 = st.text_area(
    "5. Pregunta del usuario",
    value="How long do I have to make an 83b election?",
    height=56,
    key="input_6.1_pregunta",
)

formato_6_1 = st.text_area(
    "6. Formato de output",
    value="",
    height=56,
    key="input_6.1_formato",
    placeholder="Ej: Responde en maximo 3 parrafos. Cita la seccion especifica del codigo.",
)

col1, col2 = st.columns([1, 4])
run_6_1 = col1.button("Ejecutar", key="run_6.1", use_container_width=True)
hint_6_1 = col2.button("Ver pista", key="hint_6.1", use_container_width=True)

if hint_6_1:
    st.info(
        "Asegurate de incluir: 1) Un system prompt con rol de asesor fiscal. "
        "2) Reglas que obliguen a Claude a usar SOLO el documento. "
        "3) El codigo fiscal se incluye automaticamente. "
        "4) La pregunta sobre la eleccion 83b. "
        "La respuesta esta en la seccion (b)(2): 'not later than 30 days after the date of such transfer'."
    )

if run_6_1:
    # Ensamblar el prompt completo
    partes_prompt = []
    if tono_6_1.strip():
        partes_prompt.append(f"Tono: {tono_6_1.strip()}")
    if reglas_6_1.strip():
        partes_prompt.append(f"Instrucciones:\n{reglas_6_1.strip()}")
    if ejemplos_6_1.strip():
        partes_prompt.append(f"Ejemplos:\n{ejemplos_6_1.strip()}")
    partes_prompt.append(f"<codigo_fiscal>\n{TAX_CODE}\n</codigo_fiscal>")
    if pregunta_6_1.strip():
        partes_prompt.append(f"Pregunta del usuario: {pregunta_6_1.strip()}")
    if formato_6_1.strip():
        partes_prompt.append(f"Formato de respuesta: {formato_6_1.strip()}")

    prompt_completo = "\n\n".join(partes_prompt)

    with st.expander("Ver prompt ensamblado"):
        st.code(prompt_completo[:3000] + ("\n\n... [truncado para visualizacion]" if len(prompt_completo) > 3000 else ""), language=None)

    with st.spinner("Claude esta pensando..."):
        respuesta = get_completion(prompt_completo, system_prompt=sys_prompt_6_1.strip())

    st.markdown("**Respuesta de Claude:**")
    st.code(respuesta, language=None)

    # Marcar como completado al ejecutar (ejercicio abierto)
    st.session_state.completed.add("6.1")
    st.success("Ejercicio marcado como completado. Revisa la respuesta -- debe mencionar '30 days' o '30 dias'.")

st.divider()

# ══════════════════════════════════════════════════════════════
# Ejercicio 6.2 - Tutor Socratico de Codigo
# ══════════════════════════════════════════════════════════════
st.subheader("Ejercicio 6.2 - Tutor Socratico de Codigo")
st.markdown("""
Construye un prompt para que Claude actue como un **tutor socratico** que revisa
codigo de un estudiante. En lugar de dar la respuesta directamente, Claude debe
**guiar al estudiante con preguntas** para que descubra el bug por si mismo.

El codigo a revisar tiene un **bug de division por cero**:
""")

codigo_buggy = '''def calcular_inversos_multiplicativos(numeros):
    inversos = []
    for i in range(len(numeros)):
        inverso = 1 / numeros[i]  # Bug: division por cero si numeros[i] == 0
        inversos.append(inverso)
    return inversos'''

st.code(codigo_buggy, language="python")

st.markdown("""
Rellena los campos para construir tu prompt de tutor socratico.
Claude **no debe revelar el bug directamente**, sino guiar con preguntas.
""")

sys_prompt_6_2 = st.text_area(
    "1. System prompt (rol de tutor)",
    value="",
    height=84,
    key="input_6.2_system",
    placeholder="Ej: Eres un tutor de programacion que usa el metodo socratico. Nunca das la respuesta directamente.",
)

reglas_6_2 = st.text_area(
    "2. Reglas de comportamiento",
    value="",
    height=112,
    key="input_6.2_reglas",
    placeholder="Ej: NO reveles el bug directamente.\nHaz preguntas que guien al estudiante.\nSugiere que considere casos especiales en los datos de entrada.",
)

contexto_6_2 = st.text_area(
    "3. Contexto adicional (opcional)",
    value="",
    height=56,
    key="input_6.2_contexto",
    placeholder="Ej: El estudiante es principiante en Python y aun no domina el manejo de excepciones.",
)

instruccion_6_2 = st.text_area(
    "4. Instruccion / tarea",
    value="",
    height=84,
    key="input_6.2_instruccion",
    placeholder="Ej: Un estudiante te muestra el siguiente codigo y te pide que lo revises. Respondele como tutor.",
)

formato_6_2 = st.text_area(
    "5. Formato de output",
    value="",
    height=56,
    key="input_6.2_formato",
    placeholder="Ej: Responde con 2-3 preguntas guia, sin revelar la solucion.",
)

col1, col2 = st.columns([1, 4])
run_6_2 = col1.button("Ejecutar", key="run_6.2", use_container_width=True)
hint_6_2 = col2.button("Ver pista", key="hint_6.2", use_container_width=True)

if hint_6_2:
    st.info(
        "Clave: 1) Dale a Claude el rol de tutor socratico. "
        "2) Incluye reglas explicitas de NO dar la respuesta. "
        "3) Incluye el codigo en tags XML. "
        "4) Pidele que haga preguntas como 'Que pasa si la lista contiene un cero?' "
        "El bug es que `1 / numeros[i]` falla si `numeros[i] == 0`."
    )

if run_6_2:
    # Ensamblar el prompt
    partes_prompt = []
    if reglas_6_2.strip():
        partes_prompt.append(f"Reglas:\n{reglas_6_2.strip()}")
    if contexto_6_2.strip():
        partes_prompt.append(f"Contexto:\n{contexto_6_2.strip()}")
    if instruccion_6_2.strip():
        partes_prompt.append(instruccion_6_2.strip())

    partes_prompt.append(f"<codigo_del_estudiante>\n{codigo_buggy}\n</codigo_del_estudiante>")

    if formato_6_2.strip():
        partes_prompt.append(f"Formato de respuesta: {formato_6_2.strip()}")

    prompt_completo = "\n\n".join(partes_prompt)

    with st.expander("Ver prompt ensamblado"):
        st.code(prompt_completo, language=None)

    with st.spinner("Claude esta pensando..."):
        respuesta = get_completion(prompt_completo, system_prompt=sys_prompt_6_2.strip())

    st.markdown("**Respuesta de Claude:**")
    st.code(respuesta, language=None)

    # Marcar como completado al ejecutar (ejercicio abierto)
    st.session_state.completed.add("6.2")
    st.success("Ejercicio marcado como completado. Revisa que Claude guie al estudiante sin revelar la respuesta directamente.")

st.divider()

# ══════════════════════════════════════════════════════════════
# Bonus: Encadenamiento de Prompts
# ══════════════════════════════════════════════════════════════
st.subheader("Bonus: Encadenamiento de Prompts")
st.markdown("""
Para tareas muy complejas, puedes **encadenar** multiples llamadas a Claude, donde
el output de un paso se usa como input del siguiente.

Este demo muestra un encadenamiento de 2 pasos:
1. **Paso 1:** Generar un outline sobre un tema
2. **Paso 2:** Expandir una seccion del outline en un parrafo detallado

Pruebalo a continuacion:
""")

tema_cadena = st.text_input(
    "Tema para el articulo",
    value="El impacto de la inteligencia artificial en la educacion",
    key="input_chain_tema",
)

col1, col2 = st.columns([1, 4])
run_cadena = col1.button("Ejecutar cadena", key="run_chain", use_container_width=True)

if run_cadena:
    if not tema_cadena.strip():
        st.warning("Escribe un tema para generar el articulo.")
    else:
        # ── Paso 1: Generar outline ─────────────────────────────
        prompt_paso_1 = (
            f"Generate a concise outline with exactly 5 sections for an article about: {tema_cadena.strip()}\n\n"
            "Format: Number each section (1-5) with a short title. No descriptions, just titles."
        )

        with st.spinner("Paso 1: Generando outline..."):
            outline = get_completion(prompt_paso_1)

        st.markdown("**Paso 1 - Outline generado:**")
        st.code(outline, language=None)

        # ── Paso 2: Expandir seccion 3 ──────────────────────────
        prompt_paso_2 = (
            f"Here is an outline for an article:\n\n<outline>\n{outline}\n</outline>\n\n"
            "Expand section 3 into a detailed paragraph of approximately 150 words. "
            "Write in Spanish. Be informative and engaging."
        )

        with st.spinner("Paso 2: Expandiendo seccion 3..."):
            expansion = get_completion(prompt_paso_2)

        st.markdown("**Paso 2 - Seccion 3 expandida:**")
        st.code(expansion, language=None)

        st.info(
            "Observa como el output del Paso 1 (el outline) se uso como input del Paso 2. "
            "Este patron se puede extender a 3, 4 o mas pasos segun la complejidad de la tarea."
        )
