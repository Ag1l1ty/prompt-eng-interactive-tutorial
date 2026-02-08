import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_2_1, grade_2_2, grade_2_3

render_sidebar()

st.title("Capitulo 2: Ser Claro y Directo")

render_lesson("""
## Claude responde mejor a instrucciones claras y directas

Piensa en Claude como cualquier otra persona que es **nueva en el trabajo**. Claude no tiene contexto sobre que hacer aparte de lo que literalmente le dices. Al igual que cuando instruyes a un humano por primera vez en una tarea, cuanto mas le expliques exactamente lo que quieres de manera directa, mejor y mas precisa sera su respuesta.

### La Regla de Oro del Prompting Claro

> Muestra tu prompt a un colega o amigo y haz que sigan las instrucciones por si mismos para ver si pueden producir el resultado que deseas. **Si ellos estan confundidos, Claude tambien lo estara.**

### Ejemplos

Tomemos una tarea como escribir poesia. Si le pedimos a Claude que escriba un haiku:

```python
PROMPT = "Write a haiku about robots."
print(get_completion(PROMPT))
```

Claude produce un buen haiku, pero puede incluir un preambulo como *"Here is a haiku..."*. Si queremos que vaya directo al poema, simplemente se lo **pedimos**:

```python
PROMPT = "Write a haiku about robots. Skip the preamble; go straight into the poem."
print(get_completion(PROMPT))
```

### Ser especifico en lo que quieres

Si preguntamos quien es el mejor jugador de baloncesto de todos los tiempos, Claude puede dar una respuesta ambigua listando varios nombres sin decidirse.

```python
PROMPT = "Who is the best basketball player of all time?"
```

Pero si le pedimos que elija uno definitivamente:

```python
PROMPT = "Who is the best basketball player of all time? Yes, there are differing opinions, but if you absolutely had to pick one player, who would it be?"
```

Claude se compromete con una respuesta clara. La clave es **pedir exactamente lo que necesitas**, sin dejar ambiguedades.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="2.1",
    title="Espanol",
    instruction="""Escribe un prompt que haga que Claude **responda en espanol**.

El objetivo es que la respuesta de Claude contenga la palabra `"hola"`. Pidele a Claude que responda en espanol como lo harias al hablar con un humano.""",
    hint="La funcion de calificacion en este ejercicio busca cualquier respuesta que incluya la palabra \"hola\".\nPidele a Claude que responda en espanol como lo harias al hablar con un humano. Asi de simple!",
    grade_fn=grade_2_1,
)

render_exercise(
    exercise_id="2.2",
    title="Solo Un Jugador",
    instruction="""Escribe un prompt para que Claude responda con **exactamente** `"Michael Jordan"` y nada mas.

No debe haber preambulo, explicacion, ni puntuacion adicional. Solo el nombre exacto.""",
    hint="La funcion de calificacion en este ejercicio busca EXACTAMENTE \"Michael Jordan\".\nComo le pedirias a otro humano que hiciera esto? Responder sin otras palabras? Responder solo con el nombre y nada mas? Hay varias formas de abordar esta respuesta.",
    grade_fn=grade_2_2,
)

render_exercise(
    exercise_id="2.3",
    title="Escribe una Historia",
    instruction="""Escribe un prompt que haga que Claude genere una respuesta lo **mas larga posible**.

Tu respuesta debe tener **al menos 800 palabras** para ser calificada como correcta.

> **Consejo:** Como los LLMs aun no son buenos contando palabras, puede que tengas que apuntar por encima de tu objetivo.""",
    hint="La funcion de calificacion en esta celda busca una respuesta que sea igual o mayor a 800 palabras.\nComo los LLMs aun no son buenos contando palabras, puede que tengas que apuntar por encima de tu objetivo.",
    grade_fn=grade_2_3,
)
