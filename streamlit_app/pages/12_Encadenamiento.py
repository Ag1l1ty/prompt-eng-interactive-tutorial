import streamlit as st
from utils.components import render_sidebar, render_lesson, render_code_demo
from utils.api import get_completion

render_sidebar()

st.title("Apendice 12.1: Encadenamiento de Prompts")

render_lesson("""
## Escribir es reescribir

El dicho dice: "Escribir es reescribir." Resulta que **Claude a menudo puede mejorar la precision
de su respuesta cuando se le pide que lo haga**.

El **encadenamiento de prompts** (prompt chaining) consiste en tomar la salida de una llamada
a Claude y usarla como entrada para la siguiente. Hay muchas formas de pedirle a Claude que
"piense de nuevo". Las formas que resultan naturales para pedirle a un humano que revise su
trabajo tambien funcionaran generalmente con Claude.

### Por que encadenar prompts?

- **Auto-correccion:** Claude puede revisar y corregir sus propias respuestas
- **Refinamiento iterativo:** Mejorar un borrador paso a paso
- **Procesamiento en etapas:** Extraer informacion y luego transformarla
- **Flujos de trabajo complejos:** Dividir tareas grandes en pasos manejables

### Ejemplo 1: Auto-verificacion

En este primer ejemplo, le pedimos a Claude que proponga diez palabras que terminen en "ab".
Es posible que una o mas no sean palabras reales. Luego, en un segundo paso, le pedimos que
verifique y corrija su respuesta.

```python
# Paso 1: Generar palabras
first_user = "Name ten words that all end with the exact letters 'ab'."
first_response = get_completion(first_user)

# Paso 2: Pedirle que verifique
second_user = "Please find replacements for all 'words' that are not real words. "
              "If all the words are real words, return the original list."
# Se construye la conversacion multi-turno con la respuesta anterior
```

El truco clave es dar a Claude una **salida alternativa** ("If all the words are real words,
return the original list") para que no cambie palabras que ya son correctas.

### Ejemplo 2: Refinamiento creativo

Tambien puedes usar el encadenamiento para **pedirle a Claude que mejore sus respuestas**.
Primero le pides que escriba una historia, y luego que la mejore:

```python
# Paso 1
first_user = "Write a three-sentence short story about a girl who likes to run."
first_response = get_completion(first_user)

# Paso 2: Mejorar
second_user = "Make the story better."
# Se envia la conversacion completa incluyendo la respuesta anterior
```

### Ejemplo 3: Extraccion y transformacion

Otro patron poderoso es **extraer datos en un paso y transformarlos en otro**:

```python
# Paso 1: Extraer nombres
first_user = 'Find all names from the below text: "Hey, Jesse. It\\'s me, Erin..."'
first_response = get_completion(first_user)

# Paso 2: Transformar
second_user = "Alphabetize the list."
# Se incluye la respuesta del paso 1 como contexto
```

### Sustitucion y composicion

Esta tecnica de sustitucion es muy poderosa. Puedes usar marcadores para pasar listas,
palabras, respuestas anteriores de Claude y mas. Tambien puedes usarla para lo que llamamos
"llamada a funciones" (*function calling*), que consiste en pedirle a Claude que ejecute
alguna funcion, tomar los resultados y pedirle que haga aun mas con ellos. Mas sobre esto
en el siguiente apendice.
""")

st.divider()
st.header("Demos Interactivos")

# ── Demo 1: Auto-verificacion de palabras ────────────────────────────────────

st.subheader("Demo 1: Auto-verificacion de palabras")
st.markdown("""
Este demo replica el ejemplo del notebook: Claude genera palabras que terminan en "ab"
y luego verifica su propia respuesta.
""")

ending = st.text_input(
    "Terminacion de las palabras",
    value="ab",
    key="chain_ending",
)

if st.button("Ejecutar cadena de verificacion", key="run_verify_chain"):
    # Paso 1: Generar
    with st.spinner("Paso 1: Generando palabras..."):
        step1_prompt = f"Name ten words that all end with the exact letters '{ending}'."
        step1 = get_completion(step1_prompt)
    st.markdown("**Paso 1 - Palabras generadas:**")
    st.code(step1, language=None)

    # Paso 2: Verificar y corregir
    with st.spinner("Paso 2: Verificando y corrigiendo..."):
        # Build multi-turn conversation
        import anthropic

        api_key = st.session_state.get("api_key", "")
        if api_key:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-opus-4-6",
                max_tokens=2000,
                temperature=0.0,
                messages=[
                    {"role": "user", "content": step1_prompt},
                    {"role": "assistant", "content": step1},
                    {
                        "role": "user",
                        "content": "Please find replacements for all 'words' that are not real words. If all the words are real words, return the original list.",
                    },
                ],
            )
            step2 = response.content[0].text
        else:
            st.error("Configura tu API key en la barra lateral.")
            st.stop()

    st.markdown("**Paso 2 - Verificacion:**")
    st.code(step2, language=None)
    st.success("Cadena de verificacion completada!")

st.divider()

# ── Demo 2: Refinamiento creativo ────────────────────────────────────────────

st.subheader("Demo 2: Refinamiento creativo")
st.markdown("""
Claude escribe una historia corta y luego la mejora. Compara ambas versiones para ver
como el encadenamiento mejora la calidad.
""")

story_topic = st.text_input(
    "Tema de la historia",
    value="a girl who likes to run",
    key="chain_story_topic",
)

if st.button("Generar y mejorar historia", key="run_story_chain"):
    import anthropic

    api_key = st.session_state.get("api_key", "")
    if not api_key:
        st.error("Configura tu API key en la barra lateral.")
        st.stop()
    client = anthropic.Anthropic(api_key=api_key)

    # Paso 1: Primera version
    with st.spinner("Paso 1: Escribiendo primer borrador..."):
        first_prompt = f"Write a three-sentence short story about {story_topic}."
        step1 = get_completion(first_prompt)
    st.markdown("**Paso 1 - Primer borrador:**")
    st.code(step1, language=None)

    # Paso 2: Mejorar
    with st.spinner("Paso 2: Mejorando la historia..."):
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            temperature=0.0,
            messages=[
                {"role": "user", "content": first_prompt},
                {"role": "assistant", "content": step1},
                {"role": "user", "content": "Make the story better."},
            ],
        )
        step2 = response.content[0].text
    st.markdown("**Paso 2 - Version mejorada:**")
    st.code(step2, language=None)
    st.success("Cadena de refinamiento completada!")

st.divider()

# ── Demo 3: Extraccion y transformacion ──────────────────────────────────────

st.subheader("Demo 3: Extraccion y transformacion")
st.markdown("""
Claude primero extrae informacion de un texto, y luego la transforma en el segundo paso.
Este patron es util para pipelines de procesamiento de datos.
""")

source_text = st.text_area(
    "Texto fuente",
    value=(
        "Hey, Jesse. It's me, Erin. I'm calling about the party that Joey "
        "is throwing tomorrow. Keisha said she would come and I think Mel "
        "will be there too."
    ),
    height=100,
    key="chain_extract_text",
)
transform_instruction = st.text_input(
    "Instruccion de transformacion (Paso 2)",
    value="Alphabetize the list.",
    key="chain_transform",
)

if st.button("Extraer y transformar", key="run_extract_chain"):
    import anthropic

    api_key = st.session_state.get("api_key", "")
    if not api_key:
        st.error("Configura tu API key en la barra lateral.")
        st.stop()
    client = anthropic.Anthropic(api_key=api_key)

    # Paso 1: Extraer
    extract_prompt = f"Find all names from the below text:\n\n\"{source_text}\""
    with st.spinner("Paso 1: Extrayendo informacion..."):
        step1 = get_completion(extract_prompt)
    st.markdown("**Paso 1 - Extraccion:**")
    st.code(step1, language=None)

    # Paso 2: Transformar
    with st.spinner("Paso 2: Transformando..."):
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=2000,
            temperature=0.0,
            messages=[
                {"role": "user", "content": extract_prompt},
                {"role": "assistant", "content": step1},
                {"role": "user", "content": transform_instruction},
            ],
        )
        step2 = response.content[0].text
    st.markdown("**Paso 2 - Transformacion:**")
    st.code(step2, language=None)
    st.success("Cadena de extraccion completada!")

st.divider()

# ── Demo 4: Encadenamiento libre ─────────────────────────────────────────────

st.subheader("Demo 4: Encadenamiento libre")
st.markdown("""
Crea tu propia cadena de prompts. Escribe un tema y observa como cada paso
construye sobre el anterior: generacion de outline, expansion, y edicion.
""")

topic = st.text_input(
    "Tema para el encadenamiento",
    value="artificial intelligence",
    key="chain_topic",
)

if st.button("Ejecutar cadena de 3 pasos", key="run_chain"):
    with st.spinner("Paso 1: Generando outline..."):
        step1 = get_completion(f"Create a 3-point outline about {topic}. Be concise.")
    st.markdown("**Paso 1 - Outline:**")
    st.code(step1, language=None)

    with st.spinner("Paso 2: Expandiendo..."):
        step2 = get_completion(
            f"Expand this outline into a short paragraph (about 100 words):\n\n{step1}"
        )
    st.markdown("**Paso 2 - Expansion:**")
    st.code(step2, language=None)

    with st.spinner("Paso 3: Editando para calidad..."):
        step3 = get_completion(
            f"Edit this paragraph for clarity and style. Make it engaging:\n\n{step2}"
        )
    st.markdown("**Paso 3 - Edicion final:**")
    st.code(step3, language=None)

    st.success("Cadena de 3 pasos completada!")
    st.session_state.completed.add("12.1")
