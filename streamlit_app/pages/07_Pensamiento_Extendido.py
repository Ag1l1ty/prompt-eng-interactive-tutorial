import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion, get_completion_with_thinking
from utils.grading import grade_7_1, grade_7_2, grade_7_3

render_sidebar()
st.title("Capitulo 7: Pensamiento Extendido")

render_lesson("""
### Antecedente: Cadena de Pensamiento (CoT)

Antes de que existiera el pensamiento extendido, la tecnica estandar para mejorar
el razonamiento de Claude era pedirle que **"piense paso a paso"** directamente
en su respuesta visible. Esta tecnica se conoce como **Chain of Thought (CoT)**.

La idea es simple: en lugar de pedir la respuesta directa, le pides a Claude que
muestre su razonamiento antes de responder.

> **Sin CoT:** "Si tengo 3 cajas con 4 manzanas cada una y regalo 5, cuantas me quedan?"
>
> **Respuesta:** "7"

> **Con CoT:** "Si tengo 3 cajas con 4 manzanas cada una y regalo 5, cuantas me quedan? Piensa paso a paso."
>
> **Respuesta:** "Paso 1: Tengo 3 cajas con 4 manzanas = 3 x 4 = 12 manzanas.
> Paso 2: Regalo 5 manzanas. 12 - 5 = 7 manzanas.
> Respuesta: Me quedan 7 manzanas."

La cadena de pensamiento sigue siendo util para tareas simples donde quieres
**ver** el razonamiento de Claude. Sin embargo, tiene limitaciones:
- El razonamiento ocupa tokens de la respuesta
- Claude puede "autocensurarse" al razonar en voz alta
- Para problemas complejos, no siempre es suficiente

---

### Pensamiento Extendido: La evolucion moderna

El **pensamiento extendido** (extended thinking) es la evolucion natural de CoT.
En vez de pedirle a Claude que razone en su respuesta visible, Claude piensa
**internamente** (de forma oculta) antes de generar su respuesta final.

Se activa a traves de la API con el parametro `thinking`:

```python
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 2000},
    messages=[{"role": "user", "content": prompt}],
)
```

El parametro `budget_tokens` controla la profundidad del razonamiento interno:
- **Minimo:** 1024 tokens
- **Valores tipicos:** 2000-10000 tokens
- **Mas budget** = razonamiento mas profundo, pero mas tiempo y costo

---

### Restricciones importantes

- **No funciona con `temperature`:** El pensamiento extendido requiere temperature por defecto
- **No funciona con prefill:** No se puede combinar con la tecnica de "hablar por Claude"
- **No sustituye un buen prompt:** El pensamiento extendido mejora el razonamiento, pero un prompt mal escrito seguira dando malos resultados

---

### Cuando usarlo vs. cuando NO usarlo

| Situacion | Recomendacion |
|-----------|--------------|
| Problemas de logica o matematicas | Usar pensamiento extendido |
| Analisis de codigo complejo | Usar pensamiento extendido |
| Tareas con multiples restricciones | Usar pensamiento extendido |
| Preguntas factuales simples | NO necesario (CoT o directo) |
| Tareas creativas (escribir, resumir) | NO necesario |
| Cuando necesitas prefill o temperature | NO compatible |

---

### Comparacion: Cadena de Pensamiento vs. Pensamiento Extendido

| | Cadena de Pensamiento | Pensamiento Extendido |
|---|---|---|
| Razonamiento | Visible en la respuesta | Oculto internamente |
| Activacion | Instruccion en el prompt | Parametro API |
| Precision | Buena | Superior |
| Costo | Mas tokens visibles | Budget separado |
""")

st.divider()
st.header("Ejercicios")

# ── Ejercicio 7.1 ──────────────────────────────────────────────
st.subheader("Ejercicio 7.1 - Comparar Normal vs Extendido")
st.markdown("""
Prueba el siguiente problema de logica **con y sin** pensamiento extendido para
comparar los resultados:

> *"Si 5 maquinas fabrican 5 piezas en 5 minutos, cuanto tardan 100 maquinas en fabricar 100 piezas?"*

La respuesta correcta es **5 minutos** (contraintuitivo: cada maquina fabrica 1 pieza
en 5 minutos, sin importar cuantas maquinas haya).
""")

prompt_7_1 = st.text_area(
    "Prompt",
    value="Si 5 maquinas fabrican 5 piezas en 5 minutos, cuanto tardan 100 maquinas en fabricar 100 piezas?",
    height=80,
    key="ex_7_1",
)
budget_7_1 = st.slider(
    "Budget tokens (pensamiento extendido)",
    1024, 10000, 2000, 512,
    key="budget_7_1",
)

col1, col2 = st.columns(2)
with col1:
    if st.button("Sin pensamiento extendido", key="run_7_1_normal"):
        with st.spinner("Claude esta pensando..."):
            response = get_completion(prompt_7_1)
        st.markdown("**Respuesta (modo normal):**")
        st.code(response, language=None)

with col2:
    if st.button("Con pensamiento extendido", key="run_7_1_ext"):
        with st.spinner("Claude esta pensando (con razonamiento interno)..."):
            thinking, response = get_completion_with_thinking(
                prompt_7_1, budget_tokens=budget_7_1
            )
        with st.expander("Pensamiento interno de Claude"):
            st.markdown(thinking)
        st.markdown("**Respuesta (con pensamiento extendido):**")
        st.code(response, language=None)
        if grade_7_1(response):
            st.success("Correcto! La respuesta contiene '5 minutos'.")
            st.session_state.completed.add("7.1")
        else:
            st.error("Incorrecto. La respuesta deberia ser 5 minutos.")

if st.button("Ver pista", key="hint_7_1"):
    st.info(
        "El truco del problema: cada maquina fabrica 1 pieza en 5 minutos. "
        "Con 100 maquinas, cada una fabrica su pieza en paralelo, asi que "
        "100 piezas se fabrican en los mismos 5 minutos. Prueba ambos modos "
        "para ver como el pensamiento extendido ayuda a resolver este tipo de problema."
    )
st.divider()

# ── Ejercicio 7.2 ──────────────────────────────────────────────
st.subheader("Ejercicio 7.2 - Encontrar el Budget Minimo")
st.markdown("""
Otro clasico problema contraintuitivo:

> *"Un bate y una pelota cuestan $1.10 en total. El bate cuesta $1 mas que la pelota. Cuanto cuesta la pelota?"*

La respuesta correcta es **$0.05** (no $0.10 como la mayoria piensa intuitivamente).

Experimenta con el **slider de budget** para encontrar el budget minimo que
permite a Claude responder correctamente.
""")

prompt_7_2 = st.text_area(
    "Prompt",
    value="Un bate y una pelota cuestan $1.10 en total. El bate cuesta $1 mas que la pelota. Cuanto cuesta la pelota?",
    height=80,
    key="ex_7_2",
)
budget_7_2 = st.slider(
    "Budget tokens",
    1024, 10000, 2000, 512,
    key="budget_7_2",
)

if st.button("Ejecutar con pensamiento extendido", key="run_7_2"):
    with st.spinner("Claude esta pensando..."):
        thinking, response = get_completion_with_thinking(
            prompt_7_2, budget_tokens=budget_7_2
        )
    with st.expander("Pensamiento interno de Claude"):
        st.markdown(thinking)
    st.markdown("**Respuesta:**")
    st.code(response, language=None)
    st.info(
        f"Longitud del pensamiento: {len(thinking)} caracteres | "
        f"Budget asignado: {budget_7_2} tokens"
    )
    if grade_7_2(response):
        st.success("Correcto! La pelota cuesta $0.05.")
        st.session_state.completed.add("7.2")
    else:
        st.error("Incorrecto. La respuesta deberia ser $0.05 (5 centavos).")

if st.button("Ver pista", key="hint_7_2"):
    st.info(
        "Si la pelota costara $0.10, el bate costaria $1.10 (un dolar mas), "
        "y el total seria $1.20, no $1.10. La respuesta correcta: pelota = $0.05, "
        "bate = $1.05, total = $1.10. Ajusta el budget y observa como cambia "
        "la longitud del razonamiento interno."
    )
st.divider()

# ── Ejercicio 7.3 ──────────────────────────────────────────────
st.subheader("Ejercicio 7.3 - Revision de Codigo con Pensamiento Extendido")
st.markdown("""
Usa un **system prompt** y **pensamiento extendido** para que Claude analice
el siguiente codigo Python en busca de bugs. El codigo tiene **3 errores**:

1. `maximo = 0` falla si todos los numeros son negativos
2. `sum(numeros) / len(numeros)` lanza `ZeroDivisionError` si la lista esta vacia
3. `numeros.remove(n)` modifica la lista mientras se itera sobre ella

Claude debe identificar al menos **2 de los 3 bugs** para aprobar el ejercicio.
""")

DEFAULT_SYSTEM_7_3 = "Eres un experto revisor de codigo Python. Analiza el codigo en busca de bugs, casos limite y problemas potenciales."

DEFAULT_CODE_7_3 = """Analiza el siguiente codigo Python y encuentra todos los bugs:

```python
def procesar_lista(numeros):
    maximo = 0
    for n in numeros:
        if n > maximo:
            maximo = n
    promedio = sum(numeros) / len(numeros)
    resultado = []
    for n in numeros:
        if n < promedio:
            numeros.remove(n)
    return maximo, promedio, numeros
```"""

system_7_3 = st.text_area(
    "System Prompt",
    value=DEFAULT_SYSTEM_7_3,
    height=100,
    key="sys_7_3",
)
prompt_7_3 = st.text_area(
    "Prompt",
    value=DEFAULT_CODE_7_3,
    height=200,
    key="ex_7_3",
)
budget_7_3 = st.slider(
    "Budget tokens",
    1024, 10000, 4000, 512,
    key="budget_7_3",
)

if st.button("Ejecutar revision de codigo", key="run_7_3"):
    with st.spinner("Claude esta analizando el codigo..."):
        thinking, response = get_completion_with_thinking(
            prompt_7_3,
            system_prompt=system_7_3,
            budget_tokens=budget_7_3,
        )
    with st.expander("Pensamiento interno de Claude"):
        st.markdown(thinking)
    st.markdown("**Analisis de Claude:**")
    st.code(response, language=None)
    if grade_7_3(response):
        st.success("Excelente! Claude identifico al menos 2 de los 3 bugs.")
        st.session_state.completed.add("7.3")
    else:
        st.error(
            "Claude no identifico suficientes bugs. "
            "Intenta mejorar tu system prompt o aumentar el budget."
        )

if st.button("Ver pista", key="hint_7_3"):
    st.info(
        "Pide explicitamente que busque: 1) valores iniciales incorrectos, "
        "2) posibles excepciones con entradas vacias, 3) mutacion de estructuras "
        "durante iteracion. Un budget mas alto (4000+) da mejor analisis."
    )
st.divider()
