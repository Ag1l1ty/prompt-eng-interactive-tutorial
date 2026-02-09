import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion

render_sidebar()
st.title("Capitulo 10: RAG - Busqueda y Recuperacion")

render_lesson("""
### Que es RAG?

**RAG** (*Retrieval-Augmented Generation*) es una tecnica donde **recuperas
documentos relevantes** y los incluyes como contexto en el prompt para que Claude
responda basandose en ellos.

En vez de depender unicamente del conocimiento interno de Claude (que tiene una
fecha de corte y no conoce tus datos privados), le proporcionas la informacion
exacta que necesita para responder.

---

### Por que usar RAG?

RAG resuelve tres problemas fundamentales de los LLMs:

| Problema | Como RAG lo soluciona |
|----------|----------------------|
| **Conocimiento desactualizado** | Le das documentos con la informacion mas reciente |
| **Datos privados** | Le proporcionas datos internos que Claude no tiene |
| **Alucinaciones** | Claude se basa en evidencia real, no en suposiciones |

---

### Flujo de RAG

El flujo tipico de RAG es:

1. **Pregunta del usuario** -- El usuario hace una pregunta
2. **Buscar/recuperar documentos** -- Tu sistema busca los documentos mas relevantes
   (por palabras clave, embeddings, APIs, etc.)
3. **Insertar en el prompt** -- Los documentos recuperados se incluyen como contexto
4. **Claude responde** -- Claude genera su respuesta basandose en el contexto proporcionado

---

### Metodos de busqueda

Hay varias formas de recuperar documentos relevantes:

- **Palabras clave:** Busqueda simple por coincidencia de terminos
- **Busqueda semantica (embeddings):** Convierte texto a vectores numericos y
  busca por similitud de significado
- **Bases de datos vectoriales:** Almacenan embeddings para busqueda eficiente
  (Pinecone, Weaviate, ChromaDB, etc.)
- **APIs:** Consultar sistemas externos directamente

---

### Mejores practicas para RAG

1. **Envolver documentos en tags XML** -- Usa tags como `<documento>` para separar
   claramente el contexto de las instrucciones

2. **Incluir metadatos** -- Agrega titulo, fecha y fuente para que Claude pueda
   citar correctamente

3. **Limitar la cantidad de contexto** -- No envies documentos de 100 paginas.
   Recupera solo las secciones mas relevantes

4. **Pedir citas y referencias** -- Instruye a Claude para que indique de donde
   proviene cada dato en su respuesta

5. **Instruir que diga "no se"** -- Si la respuesta no esta en los documentos
   proporcionados, Claude debe decirlo explicitamente en vez de inventar

---

### RAG + Anti-alucinaciones

Combinar RAG con las tecnicas del Capitulo 5 (Evitar Alucinaciones) produce
resultados muy confiables:

- Dar documentos como contexto **+** pedir citas **+** instruir "si no esta en
  el documento, di que no lo sabes" = respuestas precisas y verificables.

---

### Resumen

| Concepto | Descripcion |
|----------|-------------|
| RAG | Recuperar documentos y darlos como contexto a Claude |
| Flujo | Pregunta, buscar, insertar contexto, responder |
| Tags XML | Envolver documentos en `<documento>` para claridad |
| Citas | Pedir a Claude que indique la fuente de cada dato |
| Anti-alucinacion | Instruir que diga "no se" si no esta en el contexto |
""")

st.divider()
st.header("Demos Interactivos")

# ── Demo 1: RAG Basico ──────────────────────────────────────────
st.subheader("Demo 1: Respuesta Basada en Documentos")
st.markdown("""
En este demo, proporcionas un documento y haces una pregunta sobre el.
Claude respondera **unicamente** con informacion del documento proporcionado.
""")

contexto = st.text_area(
    "Documento de contexto",
    value="El Mixmaster 4000 fue lanzado en 2023. Tiene un motor de 500W y viene en 3 colores: rojo, azul y plateado. La garantia cubre 2 anos. El precio es de $299.99.",
    height=100,
    key="rag_ctx",
)
pregunta = st.text_input(
    "Pregunta sobre el documento",
    value="En que colores viene el Mixmaster?",
    key="rag_q",
)
if st.button("Buscar y responder", key="run_rag"):
    prompt = (
        "Basandote UNICAMENTE en el siguiente documento, responde la pregunta.\n\n"
        f"<documento>\n{contexto}\n</documento>\n\n"
        f"Pregunta: {pregunta}\n\n"
        "Si la respuesta no esta en el documento, di 'No tengo esa informacion en el documento proporcionado.'"
    )
    with st.spinner("Claude buscando respuesta..."):
        response = get_completion(prompt)
    st.code(response, language=None)

st.divider()

# ── Demo 2: Multiples Documentos ────────────────────────────────
st.subheader("Demo 2: Multiples Documentos")
st.markdown("""
En escenarios reales, la informacion suele estar distribuida en **multiples documentos**.
Aqui puedes probar como Claude sintetiza informacion de 3 fuentes diferentes
y cita de que documento proviene cada dato.
""")

doc1 = st.text_area(
    "Documento 1: Historia",
    value="Acme Corp fue fundada en 2010 por Maria Garcia en Ciudad de Mexico. Empezo como una startup de 3 personas.",
    height=80,
    key="doc1",
)
doc2 = st.text_area(
    "Documento 2: Finanzas",
    value="En 2024, Acme Corp reporto ingresos de $50 millones, un aumento del 30% respecto al ano anterior. La empresa tiene 500 empleados.",
    height=80,
    key="doc2",
)
doc3 = st.text_area(
    "Documento 3: Futuro",
    value="Acme Corp planea expandirse a 5 paises de Latinoamerica en 2026 y lanzar su producto insignia, el AcmeBot, un asistente de IA.",
    height=80,
    key="doc3",
)
pregunta_multi = st.text_input(
    "Pregunta",
    value="Dame un resumen completo de Acme Corp",
    key="rag_multi_q",
)
if st.button("Consultar documentos", key="run_rag_multi"):
    prompt = (
        "Basandote en los siguientes documentos, responde la pregunta. "
        "Cita de que documento proviene cada dato.\n\n"
        f"<documento_1>\n{doc1}\n</documento_1>\n"
        f"<documento_2>\n{doc2}\n</documento_2>\n"
        f"<documento_3>\n{doc3}\n</documento_3>\n\n"
        f"Pregunta: {pregunta_multi}"
    )
    with st.spinner("Claude analizando documentos..."):
        response = get_completion(prompt)
    st.code(response, language=None)

st.divider()

# ── Demo 3: Detectar Limites del Contexto ───────────────────────
st.subheader("Demo 3: Detectar Limites del Contexto")
st.markdown("""
Una de las habilidades mas importantes en RAG es que Claude reconozca cuando
**la respuesta NO esta en los documentos**. Prueba haciendo una pregunta cuya
respuesta no aparece en el documento proporcionado.
""")

doc_limitado = st.text_area(
    "Documento limitado",
    value="El restaurante 'El Buen Sabor' abre de lunes a viernes de 12pm a 10pm. Especialidad: tacos al pastor. Direccion: Calle Principal 123.",
    height=80,
    key="doc_lim",
)
pregunta_trampa = st.text_input(
    "Pregunta (cuya respuesta NO esta en el documento)",
    value="Cual es el numero de telefono del restaurante?",
    key="rag_trap",
)
if st.button("Probar limites", key="run_rag_lim"):
    prompt = (
        "Basandote UNICAMENTE en el siguiente documento, responde la pregunta. "
        "Si la informacion no esta en el documento, di explicitamente que no tienes esa informacion.\n\n"
        f"<documento>\n{doc_limitado}\n</documento>\n\n"
        f"Pregunta: {pregunta_trampa}"
    )
    with st.spinner("Claude evaluando contexto..."):
        response = get_completion(prompt)
    st.code(response, language=None)
    st.session_state.completed.add("10.1")

st.divider()
st.success("Has completado todos los capitulos del tutorial! Ahora tienes las herramientas para disenar prompts efectivos para cualquier caso de uso.")
