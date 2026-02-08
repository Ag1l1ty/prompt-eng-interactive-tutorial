import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion, get_completion_with_thinking
from utils.grading import grade_10_1, grade_10_2, grade_10_3

render_sidebar()

st.title("Capitulo 10: Pensamiento Extendido (Extended Thinking)")

render_lesson("""
## De Cadena de Pensamiento a Pensamiento Extendido

En el **Capitulo 6**, aprendimos a pedirle a Claude que "piense paso a paso" incluyendo su razonamiento de forma visible en la respuesta. Esto se conoce como **cadena de pensamiento** (Chain of Thought) y funciona porque forzamos a Claude a descomponer un problema antes de dar su respuesta final.

**Pensamiento Extendido** (Extended Thinking) lleva esta idea un paso mas alla. En vez de pedirle a Claude que escriba su pensamiento como parte de la respuesta visible, la API de Anthropic tiene un parametro nativo `thinking` que permite a Claude **razonar internamente** antes de responder.

### Diferencias clave entre Cadena de Pensamiento (Cap. 6) y Pensamiento Extendido

| Aspecto | Cadena de Pensamiento (Cap. 6) | Pensamiento Extendido (Cap. 10) |
|---------|-------------------------------|----------------------------------|
| Como se activa | Pidiendo en el prompt "piensa paso a paso" | Parametro `thinking` en la API |
| Pensamiento visible | Si, en la respuesta | Separado en un bloque `thinking` |
| Control | Manual, via instrucciones | Nativo, con `budget_tokens` |
| Calidad de razonamiento | Buena | Superior para problemas complejos |

### Como usar Pensamiento Extendido

Para activar el pensamiento extendido, se agrega el parametro `thinking` a la llamada de la API:

```python
message = client.messages.create(
    model=MODEL_NAME,
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 2000
    },
    messages=[{"role": "user", "content": prompt}]
)
```

El parametro `budget_tokens` controla cuantos tokens puede usar Claude para pensar. Un presupuesto mayor permite un razonamiento mas profundo.

### Restricciones importantes

1. **No se puede usar `temperature`**: El pensamiento extendido requiere que se omita el parametro temperature o que se establezca en 1.0
2. **No se puede usar pre-llenado (prefill)**: No puedes poner palabras en la boca de Claude con un mensaje de assistant cuando usas thinking
3. **`budget_tokens` minimo**: Debe ser al menos 1024
4. **`budget_tokens` < `max_tokens`**: El presupuesto de pensamiento debe ser menor que el maximo de tokens

### Demo: Comparacion con y sin Pensamiento Extendido

Veamos como Claude maneja un problema logico complejo **sin** y **con** pensamiento extendido.

**El problema**: Jack is looking at Anne, but Anne is looking at George. Jack is married, but George is not. Is a married person looking at an unmarried person?

**Analisis**: La respuesta correcta es **Yes** (Si). El truco esta en considerar los dos casos posibles para Anne:
- Si Anne esta casada: ella (casada) esta mirando a George (no casado) -> Si
- Si Anne no esta casada: Jack (casado) esta mirando a Anne (no casada) -> Si

En ambos casos, una persona casada esta mirando a una persona no casada. Sin pensamiento extendido, Claude a menudo responde "Cannot be determined" porque no considera ambos escenarios sistematicamente.

### Efecto del presupuesto de tokens (budget_tokens)

El parametro `budget_tokens` controla la profundidad del razonamiento. Un presupuesto mayor no siempre es necesario -- la clave es encontrar el **minimo suficiente** para cada tipo de problema.

### Cuando usar Pensamiento Extendido

**Usa Pensamiento Extendido cuando:**
- Problemas de matematicas o logica complejos
- Analisis de codigo con multiples dependencias
- Tareas que requieren razonamiento multi-paso
- Cuando la precision importa mas que la velocidad o el costo

**NO uses Pensamiento Extendido cuando:**
- Preguntas factuales simples ("Cual es la capital de Francia?")
- Escritura creativa sin restricciones
- Cuando la latencia y el costo son prioritarios
- Cuando necesitas `temperature=0.0` para resultados deterministicos
- Cuando necesitas pre-llenado (prefill) de la respuesta
""")

st.divider()
st.header("Ejercicios")

# ── Exercise 10.1 ────────────────────────────────────────────────────────────

st.subheader("Ejercicio 10.1 - Pensamiento Extendido vs Normal")
st.markdown("""Usa el siguiente problema de logica. Primero resuelvelo **sin** pensamiento extendido,
y luego **con** pensamiento extendido. Compara las respuestas.

**Problema**: If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?

La respuesta correcta es **5 minutos**. Cada maquina produce 1 widget en 5 minutos,
asi que 100 maquinas producen 100 widgets en los mismos 5 minutos.

Escribe un prompt que pida la respuesta numerica en minutos. Puedes modificar el prompt si lo deseas.""")

prompt_10_1 = st.text_area(
    "Prompt",
    value="If it takes 5 machines 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets? Give only the numerical answer in minutes.",
    height=100,
    key="ex_10_1_prompt",
)
budget_10_1 = st.slider(
    "Budget tokens",
    min_value=1024,
    max_value=10000,
    value=2000,
    step=512,
    key="ex_10_1_budget",
)

col_hint_10_1, col_show_10_1 = st.columns([1, 4])
show_hint_10_1 = col_show_10_1.button("Ver pista", key="hint_10_1", use_container_width=True)
if show_hint_10_1:
    st.info("Este ejercicio busca que compares la respuesta de Claude con y sin pensamiento extendido.\nIntenta un problema matematico o logico complejo. Primero usa get_completion() normal, y luego get_completion_with_thinking().")

col1, col2 = st.columns(2)
with col1:
    if st.button("Sin pensamiento extendido", key="run_10_1_normal"):
        if not prompt_10_1.strip():
            st.warning("Escribe algo en el prompt antes de ejecutar.")
        else:
            with st.spinner("Claude pensando (normal)..."):
                response_normal = get_completion(prompt_10_1)
            st.markdown("**Respuesta (normal):**")
            st.code(response_normal, language=None)

with col2:
    if st.button("Con pensamiento extendido", key="run_10_1_thinking"):
        if not prompt_10_1.strip():
            st.warning("Escribe algo en el prompt antes de ejecutar.")
        else:
            with st.spinner("Claude pensando (extendido)..."):
                thinking, response_ext = get_completion_with_thinking(
                    prompt_10_1, budget_tokens=budget_10_1
                )
            with st.expander("Pensamiento interno de Claude", expanded=False):
                st.markdown(thinking)
            st.markdown("**Respuesta (extendido):**")
            st.code(response_ext, language=None)

            if grade_10_1(response_ext):
                st.success("Correcto! La respuesta contiene '5'.")
                st.session_state.completed.add("10.1")
            else:
                st.error("Incorrecto. La respuesta deberia contener '5'. Intenta de nuevo.")

st.divider()

# ── Exercise 10.2 ────────────────────────────────────────────────────────────

st.subheader("Ejercicio 10.2 - Optimizar el Presupuesto")
st.markdown("""Para el siguiente problema, encuentra el `budget_tokens` **minimo** que produce una respuesta correcta.
Empieza con un valor bajo (ej: 1024) y ve subiendo gradualmente.

**Problema**: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?

La respuesta correcta es **$0.05** (5 centavos). Muchas personas (y LLMs sin pensar) responden $0.10 intuitivamente,
pero si la pelota cuesta $0.10, el bate costaria $1.10 y el total seria $1.20.

Escribe un prompt que pida solo el monto en dolares.""")

prompt_10_2 = st.text_area(
    "Prompt",
    value="A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost? Give only the dollar amount.",
    height=100,
    key="ex_10_2_prompt",
)
budget_10_2 = st.slider(
    "Budget tokens",
    min_value=1024,
    max_value=10000,
    value=1024,
    step=512,
    key="ex_10_2_budget",
)

col_hint_10_2, col_show_10_2 = st.columns([1, 4])
show_hint_10_2 = col_show_10_2.button("Ver pista", key="hint_10_2", use_container_width=True)
if show_hint_10_2:
    st.info("Este ejercicio busca que encuentres el budget_tokens minimo que produce una respuesta correcta.\nEmpieza con un valor bajo (ej: 1024) y ve subiendo gradualmente hasta que Claude responda correctamente.")

if st.button("Ejecutar con pensamiento extendido", key="run_10_2"):
    if not prompt_10_2.strip():
        st.warning("Escribe algo en el prompt antes de ejecutar.")
    else:
        with st.spinner("Claude pensando (extendido)..."):
            thinking, response_10_2 = get_completion_with_thinking(
                prompt_10_2, budget_tokens=budget_10_2
            )
        with st.expander("Pensamiento interno de Claude", expanded=False):
            st.markdown(thinking)
        st.markdown(f"**Budget:** {budget_10_2} tokens")
        st.markdown(f"**Longitud del pensamiento:** {len(thinking)} caracteres")
        st.markdown("**Respuesta:**")
        st.code(response_10_2, language=None)

        if grade_10_2(response_10_2):
            st.success(f"Correcto! Claude respondio correctamente con budget_tokens={budget_10_2}.")
            st.session_state.completed.add("10.2")
        else:
            st.error("Incorrecto. La respuesta deberia ser $0.05 (5 centavos). Intenta ajustar el budget.")

st.divider()

# ── Exercise 10.3 ────────────────────────────────────────────────────────────

st.subheader("Ejercicio 10.3 - Combinar con System Prompts")
st.markdown("""Combina un system prompt detallado con pensamiento extendido para analizar el siguiente fragmento de codigo
y encontrar **todos los bugs**.

El codigo tiene **3 bugs principales**:
1. `calculate_average`: division por cero si la lista esta vacia
2. `find_max`: inicializa `max_val = 0`, falla con numeros negativos
3. `remove_duplicates`: modifica la lista mientras itera sobre ella

Escribe un system prompt que guie a Claude como revisor de codigo experto, y un prompt que le pida analizar el codigo.
La calificacion verifica que Claude identifique al menos **2 de los 3 bugs**.""")

CODE_10_3 = """
def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    average = total / len(numbers)
    return average

def find_max(numbers):
    max_val = 0
    for num in numbers:
        if num > max_val:
            max_val = num
    return max_val

def remove_duplicates(lst):
    for item in lst:
        if lst.count(item) > 1:
            lst.remove(item)
    return lst
"""

st.markdown("**Codigo a analizar:**")
st.code(CODE_10_3, language="python")

system_10_3 = st.text_area(
    "System Prompt",
    value="You are an expert code reviewer. Analyze the provided code and:\n1. List ALL bugs you find\n2. Explain why each is a bug\n3. Provide the corrected code\nBe thorough and systematic.",
    height=150,
    key="ex_10_3_system",
)
prompt_10_3 = st.text_area(
    "Prompt",
    value=f"Review this Python code and find all bugs:\n{CODE_10_3}",
    height=100,
    key="ex_10_3_prompt",
)
budget_10_3 = st.slider(
    "Budget tokens",
    min_value=1024,
    max_value=10000,
    value=4000,
    step=512,
    key="ex_10_3_budget",
)

col_hint_10_3, col_show_10_3 = st.columns([1, 4])
show_hint_10_3 = col_show_10_3.button("Ver pista", key="hint_10_3", use_container_width=True)
if show_hint_10_3:
    st.info("Combina un system prompt detallado con pensamiento extendido.\nPiensa en como el system prompt puede guiar el analisis mientras el pensamiento extendido permite un razonamiento mas profundo.")

if st.button("Ejecutar con pensamiento extendido", key="run_10_3"):
    if not prompt_10_3.strip():
        st.warning("Escribe algo en el prompt antes de ejecutar.")
    else:
        with st.spinner("Claude analizando codigo (extendido)..."):
            thinking, response_10_3 = get_completion_with_thinking(
                prompt_10_3, system_prompt=system_10_3, budget_tokens=budget_10_3
            )
        with st.expander("Pensamiento interno de Claude", expanded=False):
            st.markdown(thinking)
        st.markdown("**Analisis de Claude:**")
        st.code(response_10_3, language=None)

        if grade_10_3(response_10_3):
            st.success("Correcto! Claude identifico al menos 2 de los 3 bugs principales.")
            st.session_state.completed.add("10.3")
        else:
            st.error("Incorrecto. Claude deberia identificar al menos 2 bugs: lista vacia (division por cero), max con negativos, o modificar lista durante iteracion.")

st.divider()
st.markdown("---")
st.markdown("Continua al **Capitulo 11: System Prompts Avanzados** para aprender a construir system prompts poderosos y bien estructurados.")
