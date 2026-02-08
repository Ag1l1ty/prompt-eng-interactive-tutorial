import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_1_1, grade_1_2

render_sidebar()

st.title("Capitulo 1: Estructura Basica de Prompts")

render_lesson("""
## La API de Messages de Claude

Para interactuar con Claude, utilizamos la **API de Messages**. Como minimo, una llamada requiere los siguientes parametros:

- **`model`**: el nombre del modelo a utilizar (por ejemplo, `claude-opus-4-6`).
- **`max_tokens`**: el numero maximo de tokens a generar antes de detenerse. Claude puede detenerse antes de alcanzar este limite. Es una parada *forzada*, lo que significa que puede cortar una palabra u oracion a la mitad.
- **`messages`**: un arreglo de mensajes de entrada. Claude opera en turnos conversacionales alternados entre `user` y `assistant`.

Cada mensaje debe ser un objeto con `role` y `content`. El primer mensaje siempre debe tener el rol `user`.

### Parametros opcionales importantes

- **`system`**: el prompt de sistema, que proporciona contexto e instrucciones generales a Claude antes de la conversacion.
- **`temperature`**: controla la variabilidad en las respuestas. Para resultados deterministicos, se usa `0`.

### Ejemplo basico

```python
PROMPT = "Hi Claude, how are you?"
print(get_completion(PROMPT))
```

```python
PROMPT = "Can you tell me the color of the ocean?"
print(get_completion(PROMPT))
```

```python
PROMPT = "What year was Celine Dion born in?"
print(get_completion(PROMPT))
```

### Reglas de formato

Los mensajes de `user` y `assistant` **deben alternarse**, y **siempre deben comenzar con un turno de `user`**. Puedes tener multiples pares para simular conversaciones de multiples turnos. Tambien puedes incluir un mensaje final de `assistant` para que Claude continue desde ese punto (esto se vera en capitulos posteriores).

Si no se respetan estas reglas, la API devolvera un error.

### Prompts de Sistema

Un **prompt de sistema** es una forma de proporcionar contexto, instrucciones y directrices a Claude **antes** de presentarle la pregunta o tarea del usuario. Estructuralmente, existe separado de la lista de mensajes y se pasa en el parametro `system`.

```python
SYSTEM_PROMPT = "Your answer should always be a series of critical thinking questions that further the conversation (do not provide answers to your questions). Do not actually answer the user question."

PROMPT = "Why is the sky blue?"
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

Un **prompt de sistema bien escrito puede mejorar significativamente el rendimiento de Claude**, aumentando su capacidad para seguir reglas e instrucciones de manera consistente.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="1.1",
    title="Contar hasta Tres",
    instruction="""Usando el formato adecuado de `user` / `assistant`, escribe un prompt para que Claude **cuente hasta tres**.

La respuesta debe contener los numeros `1`, `2` y `3`.""",
    hint="La funcion de calificacion en este ejercicio busca una respuesta que contenga los numeros arabigos exactos \"1\", \"2\" y \"3\".\nA menudo puedes lograr que Claude haga lo que quieres simplemente pidiendoselo.",
    grade_fn=grade_1_1,
)

render_exercise(
    exercise_id="1.2",
    title="Prompt de Sistema",
    instruction="""Modifica el **prompt de sistema** para que Claude responda como si fuera un nino de 3 anos.

El prompt del usuario ya esta fijado como: `"How big is the sky?"`

La calificacion busca respuestas que contengan palabras como `"soo"` o `"giggles"`, tipicas de un nino pequeno.""",
    hint="La funcion de calificacion en este ejercicio busca respuestas que contengan \"soo\" o \"giggles\".\nHay muchas formas de resolver esto, simplemente pidiendolo!",
    grade_fn=grade_1_2,
    fields=[
        {"name": "SYSTEM_PROMPT", "label": "System Prompt", "rows": 3},
        {"name": "PROMPT", "label": "Prompt", "rows": 4},
    ],
    system_prompt_default="",
)
