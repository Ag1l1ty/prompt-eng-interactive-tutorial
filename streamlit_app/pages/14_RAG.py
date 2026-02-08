import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion

render_sidebar()

st.title("Apendice 12.3: Busqueda y Recuperacion (RAG)")

render_lesson("""
## Que es RAG?

**RAG** (*Retrieval-Augmented Generation*) es una tecnica que combina la busqueda de informacion
con la generacion de texto. En lugar de depender solo del conocimiento interno de Claude,
le **proporcionamos documentos relevantes como contexto** para que base sus respuestas en
informacion especifica y verificable.

### Por que usar RAG?

Claude tiene un conocimiento extenso, pero:
- Su conocimiento tiene una **fecha de corte** y no incluye informacion posterior
- No tiene acceso a **tus datos privados** (documentos internos, bases de datos, etc.)
- Puede **alucinar** informacion cuando no esta seguro

RAG resuelve estos problemas proporcionando a Claude la informacion exacta que necesita.

### Como funciona?

El flujo basico de RAG es:

1. **El usuario hace una pregunta**
2. **Se buscan documentos relevantes** en tu base de datos, Wikipedia, internet, etc.
3. **Se insertan los documentos** en el prompt como contexto
4. **Claude genera una respuesta** basada en los documentos proporcionados

```python
prompt = f\\"\\"\\"Based on the following document, answer the question.

<document>
{document_text}
</document>

Question: {user_question}\\"\\"\\"

response = get_completion(prompt)
```

### Tecnicas de busqueda

Existen varias formas de buscar documentos relevantes:

- **Busqueda por palabras clave:** Coincidencia de texto simple
- **Busqueda semantica (embeddings):** Usa vectores para encontrar documentos con significado similar
- **Bases de datos vectoriales:** Almacenan embeddings para busqueda rapida a gran escala
- **APIs externas:** Wikipedia, busqueda web, etc.

### Mejores practicas

- **Usa etiquetas XML** para delimitar claramente los documentos del contexto
- **Incluye metadatos** como fuente, fecha y titulo del documento
- **Limita el contexto** a lo relevante para evitar distracciones
- **Pide a Claude que cite sus fuentes** dentro de los documentos proporcionados
- **Instruye a Claude** que diga "no se" si la respuesta no esta en los documentos

### Recursos adicionales

Para profundizar en RAG con Claude, consulta:
- [Ejemplos del cookbook de RAG](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Wikipedia/wikipedia-search-cookbook.ipynb)
- [Documentacion sobre embeddings](https://docs.anthropic.com/claude/docs/embeddings)
""")

st.divider()
st.header("Demos Interactivos")

# ── Demo 1: RAG basico ──────────────────────────────────────────────────────

st.subheader("Demo 1: Respuesta basada en documentos")
st.markdown("""
Este demo muestra el patron fundamental de RAG: proporcionamos un documento como contexto
y Claude responde preguntas basandose **exclusivamente** en ese documento.
""")

context = st.text_area(
    "Documento de contexto",
    value=(
        "The Mixmaster 4000 was released in 2023. It has a 500W motor and comes "
        "in 3 colors: red, blue, and silver. The warranty covers 2 years. It "
        "includes a 1.5L stainless steel bowl and 5 speed settings. The price "
        "is $299.99 and it weighs 4.2 kg. It was designed by the engineering "
        "team in Zurich, Switzerland."
    ),
    height=120,
    key="rag_context",
)
question = st.text_input(
    "Pregunta sobre el documento",
    value="What colors does the Mixmaster come in?",
    key="rag_q",
)

if st.button("Buscar y responder", key="run_rag"):
    prompt = (
        "Based on the following document, answer the question. "
        "Only use information from the document. If the answer is not "
        "in the document, say 'I don't have that information.'\n\n"
        f"<document>\n{context}\n</document>\n\n"
        f"Question: {question}"
    )
    with st.spinner("Claude buscando respuesta en el documento..."):
        response = get_completion(prompt)
    st.markdown("**Respuesta de Claude:**")
    st.code(response, language=None)

st.divider()

# ── Demo 2: Multiples documentos ─────────────────────────────────────────────

st.subheader("Demo 2: Multiples documentos")
st.markdown("""
En escenarios reales de RAG, a menudo se recuperan **multiples documentos** relevantes.
Claude puede sintetizar informacion de varias fuentes.
""")

doc1 = st.text_area(
    "Documento 1",
    value=(
        "Acme Corp was founded in 1985 by Jane Smith in Portland, Oregon. "
        "The company started as a small hardware store and has grown to "
        "over 5,000 employees worldwide. Their headquarters moved to "
        "San Francisco in 2010."
    ),
    height=80,
    key="rag_doc1",
)

doc2 = st.text_area(
    "Documento 2",
    value=(
        "In 2023, Acme Corp reported annual revenue of $2.3 billion, "
        "a 15% increase from the previous year. The company's main products "
        "include cloud computing services, AI tools, and enterprise software. "
        "Their fastest growing segment is AI tools, which grew 45% year-over-year."
    ),
    height=80,
    key="rag_doc2",
)

doc3 = st.text_area(
    "Documento 3",
    value=(
        "Acme Corp announced plans to open a new R&D center in Austin, Texas "
        "in Q2 2024. The center will focus on next-generation AI research and "
        "is expected to create 500 new jobs. CEO Jane Smith said: 'This "
        "investment reflects our commitment to leading AI innovation.'"
    ),
    height=80,
    key="rag_doc3",
)

multi_question = st.text_input(
    "Pregunta sobre los documentos",
    value="Give me a complete overview of Acme Corp: when was it founded, what does it do, and what are its future plans?",
    key="rag_multi_q",
)

if st.button("Consultar multiples documentos", key="run_multi_rag"):
    prompt = (
        "Based on the following documents, answer the question. "
        "Synthesize information from all relevant documents. "
        "Cite which document(s) you used for each piece of information.\n\n"
        f"<document index=\"1\">\n{doc1}\n</document>\n\n"
        f"<document index=\"2\">\n{doc2}\n</document>\n\n"
        f"<document index=\"3\">\n{doc3}\n</document>\n\n"
        f"Question: {multi_question}"
    )
    with st.spinner("Claude sintetizando informacion..."):
        response = get_completion(prompt)
    st.markdown("**Respuesta sintetizada:**")
    st.code(response, language=None)

st.divider()

# ── Demo 3: RAG con deteccion de limites ─────────────────────────────────────

st.subheader("Demo 3: Deteccion de limites del contexto")
st.markdown("""
Un aspecto clave de RAG es que Claude debe **reconocer cuando no tiene informacion suficiente**.
Prueba haciendo preguntas cuya respuesta **no esta** en el documento para verificar que Claude
no inventa informacion.
""")

limited_context = st.text_area(
    "Documento con informacion limitada",
    value=(
        "The XR-7 smartphone was released on March 15, 2024. It features "
        "a 6.7-inch OLED display and 256GB of storage. The battery lasts "
        "up to 18 hours of normal use."
    ),
    height=80,
    key="rag_limited_ctx",
)

tricky_question = st.text_input(
    "Pregunta (prueba una cuya respuesta NO este en el documento)",
    value="What is the price of the XR-7 and what camera does it have?",
    key="rag_tricky_q",
)

if st.button("Probar limites", key="run_tricky_rag"):
    prompt = (
        "Based ONLY on the following document, answer the question. "
        "If any part of the question cannot be answered from the document, "
        "explicitly state that the information is not available in the "
        "provided document. Do NOT make up or infer information that is "
        "not directly stated.\n\n"
        f"<document>\n{limited_context}\n</document>\n\n"
        f"Question: {tricky_question}"
    )
    with st.spinner("Claude evaluando el contexto..."):
        response = get_completion(prompt)
    st.markdown("**Respuesta de Claude:**")
    st.code(response, language=None)
    st.session_state.completed.add("12.3")

st.divider()

# ── Resumen final ────────────────────────────────────────────────────────────

st.info("""
**Felicidades!** Has completado todos los apendices del tutorial de ingenieria de prompts.

Recapitulando lo que aprendiste en estos apendices:
- **12.1 - Encadenamiento:** Como componer multiples llamadas a Claude para tareas complejas
- **12.2 - Herramientas:** Como Claude puede usar funciones externas mediante tool use
- **12.3 - RAG:** Como proporcionar documentos como contexto para respuestas mas precisas

Estas tres tecnicas se combinan frecuentemente en aplicaciones del mundo real para crear
sistemas potentes basados en LLMs.
""")
