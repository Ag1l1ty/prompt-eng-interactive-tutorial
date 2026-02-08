import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_5_1, grade_5_2, grade_5_3

render_sidebar()

st.title("Capitulo 5: Formato de Output y Hablar por Claude")

render_lesson("""
## Formatear el Output de Claude

**Claude puede formatear su output de muchas maneras diferentes.** Solo necesitas pedirle que lo haga.

Una tecnica poderosa es usar **etiquetas XML para separar la respuesta** de cualquier otro texto. Ya aprendiste que puedes usar etiquetas XML para hacer tu prompt mas claro. Resulta que tambien puedes pedirle a Claude que **use etiquetas XML en su output** para hacerlo mas estructurado y facilmente procesable.

### Ejemplo: Haiku con etiquetas XML

Recuerda el "problema del preambulo del poema" del Capitulo 2. Una alternativa a pedir que omita el preambulo es pedirle que **envuelva el poema en etiquetas XML**:

```python
ANIMAL = "Rabbit"
PROMPT = f"Please write a haiku about {ANIMAL}. Put it in <haiku> tags."
```

Esto permite extraer de manera confiable solo el poema mediante un programa que busque el contenido entre las etiquetas `<haiku>` y `</haiku>`.

---

## Pre-llenado: "Hablar por Claude"

Una extension poderosa es **colocar la primera etiqueta XML en el turno del `assistant`**. Cuando pones texto en el turno del asistente, le estas diciendo a Claude que **ya dijo algo** y que debe continuar desde ese punto.

Esta tecnica se llama **"hablar por Claude"** o **pre-llenado de la respuesta** (*prefilling*).

```python
ANIMAL = "Cat"
PROMPT = f"Please write a haiku about {ANIMAL}. Put it in <haiku> tags."
PREFILL = "<haiku>"
```

Claude continuara directamente desde `<haiku>`, escribiendo el haiku sin ningun preambulo.

---

## Forzar formato JSON

Claude tambien es excelente con otros formatos de output, especialmente **JSON**. Si quieres forzar output en JSON, puedes pre-llenar la respuesta con la llave de apertura `{`:

```python
PROMPT = f"Please write a haiku about Cat. Use JSON format with the keys \\"first_line\\", \\"second_line\\", and \\"third_line\\"."
PREFILL = "{"
```

---

## Multiples variables y formato combinado

Puedes combinar **multiples variables de entrada** con **especificacion de formato de output**, todo usando etiquetas XML:

```python
EMAIL = "Hi Zack, just pinging you for a quick update on that prompt you were supposed to write."
ADJECTIVE = "olde english"
PROMPT = f"Hey Claude. Here is an email: <email>{EMAIL}</email>. Make this email more {ADJECTIVE}. Write the new version in <{ADJECTIVE}_email> XML tags."
PREFILL = f"<{ADJECTIVE}_email>"
```

### Tip avanzado: stop_sequences

Si llamas a Claude a traves de la API, puedes usar el parametro `stop_sequences` con la etiqueta XML de cierre para que Claude deje de generar una vez que emita la etiqueta deseada. Esto ahorra tokens al eliminar comentarios innecesarios despues de la respuesta.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="5.1",
    title="Steph Curry GOAT",
    instruction="""Obligado a elegir, Claude normalmente designa a Michael Jordan como el mejor jugador de baloncesto de todos los tiempos. Podemos hacer que Claude elija a alguien mas?

Usa el campo **Prefill (Assistant)** para **obligar a Claude a argumentar que el mejor jugador de baloncesto de todos los tiempos es Stephen Curry**.

El prefill coloca texto al inicio del turno del asistente, haciendo que Claude "continue" desde ahi. Por ejemplo, si escribes `"Stephen Curry is the best because"` en el prefill, Claude continuara argumentando a favor de Curry.

Intenta no cambiar el prompt, solo modifica el prefill. La calificacion busca la palabra **"Warrior"** (el equipo de Curry) en la respuesta.""",
    hint='La funcion de calificacion para este ejercicio busca una respuesta que incluya la palabra "Warrior".\nEscribe mas palabras en la voz de Claude para dirigir a Claude a actuar como quieres. Por ejemplo, en vez de "Stephen Curry is the best because," podrias escribir "Stephen Curry is the best and here are three reasons why. 1:"',
    grade_fn=grade_5_1,
    fields=[
        {"name": "PROMPT", "label": "Prompt", "rows": 4},
        {"name": "PREFILL", "label": "Prefill (Assistant)", "rows": 2},
    ],
    prefill="",
)

render_exercise(
    exercise_id="5.2",
    title="Dos Haikus",
    instruction="""Modifica el prompt para que Claude escriba **dos haikus sobre gatos** en lugar de solo uno. Debe quedar claro donde termina un poema y donde comienza el otro.

Usa **etiquetas XML `<haiku>`** para separar cada haiku. Tambien puedes usar el campo de prefill para empezar la respuesta con `<haiku>`.

La calificacion verifica que:
- La respuesta contenga la palabra **"cat"**
- La respuesta contenga la etiqueta **`<haiku>`**
- La respuesta tenga **mas de 5 lineas** (indicando multiples haikus)""",
    hint='La funcion de calificacion busca una respuesta de mas de 5 lineas que incluya las palabras "cat" y "<haiku>".\nEmpieza simple. Actualmente, el prompt pide a Claude un haiku. Puedes cambiarlo y pedir dos (o incluso mas). Luego, si encuentras problemas de formato, cambia tu prompt para arreglarlos despues de que ya hayas logrado que Claude escriba mas de un haiku.',
    grade_fn=grade_5_2,
    fields=[
        {"name": "PROMPT", "label": "Prompt", "rows": 4},
        {"name": "PREFILL", "label": "Prefill (Assistant)", "rows": 2},
    ],
    prefill="",
)

render_exercise(
    exercise_id="5.3",
    title="Dos Haikus, Dos Animales",
    instruction="""Modifica el prompt para que Claude produzca **dos haikus sobre dos animales diferentes**: uno sobre **gatos (cats)** y otro sobre **perros (dogs)**.

En el cuaderno original, este ejercicio usa variables `{ANIMAL1}` y `{ANIMAL2}` que se sustituyen con "Cat" y "Dog". En esta version interactiva, escribe directamente un prompt que pida haikus sobre ambos animales.

Usa **etiquetas XML `<haiku>`** para separar cada haiku. Puedes usar el prefill si lo deseas.

La calificacion verifica que la respuesta contenga:
- La palabra **"cat"**
- La palabra **"tail"** (tipica en haikus sobre perros/gatos)
- La etiqueta **`<haiku>`**""",
    hint='La funcion de calificacion en este ejercicio busca una respuesta que contenga las palabras "tail", "cat" y "<haiku>".\nEs util dividir este ejercicio en varios pasos:\n1. Escribe un prompt que pida a Claude dos haikus, uno sobre gatos y otro sobre perros.\n2. Pide que cada haiku este envuelto en etiquetas <haiku>.\n3. Usa el prefill con "<haiku>" si quieres forzar el formato desde el inicio.',
    grade_fn=grade_5_3,
    fields=[
        {"name": "PROMPT", "label": "Prompt", "rows": 4},
        {"name": "PREFILL", "label": "Prefill (Assistant)", "rows": 2},
    ],
    prefill="",
)
