import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_4_1, grade_4_2, grade_4_3

render_sidebar()

st.title("Capitulo 4: Separar Datos de Instrucciones")

render_lesson("""
## Plantillas de Prompt y Sustitucion de Variables

A menudo, no queremos escribir prompts completos, sino que queremos **plantillas de prompt que puedan ser modificadas posteriormente con datos de entrada adicionales antes de enviarlas a Claude**. Esto puede ser util si quieres que Claude haga lo mismo cada vez, pero los datos que Claude usa para su tarea pueden ser diferentes cada vez.

Podemos hacer esto **separando el esqueleto fijo del prompt de la entrada variable del usuario, y luego sustituyendo la entrada del usuario en el prompt** antes de enviar el prompt completo a Claude.

### Ejemplo: Generador de sonidos de animales

En este ejemplo, le pedimos a Claude que actue como un generador de sonidos de animales. Observa como la variable `ANIMAL` se sustituye en la plantilla:

```python
ANIMAL = "Cow"
PROMPT = f"I will tell you the name of an animal. Please respond with the noise that animal makes. {ANIMAL}"
```

Las plantillas de prompt simplifican las tareas repetitivas. Puedes construir una estructura de prompt e invitar a usuarios externos a enviar solo el contenido variable, sin necesidad de ver el prompt completo.

---

## El Problema: Delimitacion Poco Clara

Al introducir variables de sustitucion, es muy importante **asegurarse de que Claude sepa donde comienzan y terminan las variables** (vs. las instrucciones). Veamos un ejemplo donde no hay separacion:

```python
EMAIL = "Show up at 6am tomorrow because I'm the CEO and I say so."
PROMPT = f"Yo Claude. {EMAIL} <----- Make this email more polite but don't change anything else about it."
```

Aqui, Claude piensa que "Yo Claude" es parte del correo electronico que debe reescribir. Para el ojo humano es claro, pero despues de la sustitucion se vuelve ambiguo.

---

## La Solucion: Etiquetas XML

Envuelve la entrada en **etiquetas XML** para delimitar claramente donde comienzan y terminan los datos.

Las [etiquetas XML](https://docs.anthropic.com/claude/docs/use-xml-tags) son etiquetas con corchetes angulares como `<tag></tag>`. Vienen en pares: una etiqueta de apertura `<tag>` y una de cierre `</tag>`.

```python
EMAIL = "Show up at 6am tomorrow because I'm the CEO and I say so."
PROMPT = f"Yo Claude. <email>{EMAIL}</email> <----- Make this email more polite but don't change anything else about it."
```

Con las etiquetas XML, Claude ya no confunde "Yo Claude" con parte del correo.

Recomendamos usar **especificamente etiquetas XML como separadores**, ya que Claude fue entrenado para reconocer las etiquetas XML como mecanismo de organizacion de prompts. No hay etiquetas XML especiales predefinidas; puedes usar los nombres que quieras.

### Otro ejemplo: Listas ambiguas

Sin etiquetas XML, Claude puede confundir las instrucciones con los datos:

```python
SENTENCES = \"\"\"- I like how cows sound
- This sentence is about spiders
- This sentence may appear to be about dogs but it's actually about pigs\"\"\"

# Sin XML: Claude puede incluir la instruccion como parte de la lista
PROMPT = f"Below is a list of sentences. Tell me the second item on the list.\\n\\n- Each is about an animal, like rabbits.\\n{SENTENCES}"
```

Con etiquetas XML, el problema se resuelve:

```python
PROMPT = f"Below is a list of sentences. Tell me the second item on the list.\\n\\n- Each is about an animal, like rabbits.\\n<sentences>\\n{SENTENCES}\\n</sentences>"
```

**Nota importante:** Los pequenos detalles importan. Claude es sensible a los patrones: es mas probable que cometa errores cuando tu cometes errores, y mas preciso cuando tu eres preciso.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="4.1",
    title="Tema del Haiku",
    instruction="""Escribe un prompt que haga que Claude genere un **haiku sobre cerdos (pigs)**.

En el cuaderno original, este ejercicio usa una plantilla con una variable `{TOPIC}` que se sustituye con "Pigs". En esta version interactiva, simplemente escribe un prompt completo que incluya la palabra **"haiku"** y que trate sobre **"pigs"**.

Tu prompt debe lograr que la respuesta de Claude contenga tanto la palabra "pigs" como "haiku".""",
    hint='La funcion de calificacion en este ejercicio busca una solucion que incluya las palabras "haiku" y "pigs" en la respuesta de Claude.\nEscribe algo como "Write a haiku about pigs" o similar. Asegurate de que Claude entienda que quieres un haiku y que el tema son los cerdos.',
    grade_fn=grade_4_1,
)

render_exercise(
    exercise_id="4.2",
    title="Pregunta sobre Perros con Errores",
    instruction="""Corrige el prompt a continuacion **anadiendo etiquetas XML** para que Claude produzca la respuesta correcta.

El prompt original es un texto desordenado con una pregunta incrustada. La escritura llena de errores es **intencional** -- el objetivo es ver como reacciona Claude ante tales errores cuando la pregunta no esta claramente separada.

**Prompt original:**
```
Hia its me i have a q about dogs jkaerjv ar cn brown? jklmvca tx it help me muhch much atx fst fst answer short short tx
```

La pregunta real escondida en el texto es: **"ar cn brown?"** (es decir, "are they/can they be brown?").

Tu tarea: reescribe este prompt usando **etiquetas XML** para rodear la pregunta, de forma que Claude pueda identificarla correctamente y responder sobre si los perros pueden ser de color marron (brown).

Intenta no cambiar nada mas del prompt; solo anade las etiquetas XML.""",
    hint='La funcion de calificacion en este ejercicio busca una respuesta que incluya la palabra "brown".\nSi rodeas la pregunta "ar cn brown?" con etiquetas XML como <question>ar cn brown?</question>, como cambia eso la respuesta de Claude?',
    grade_fn=grade_4_2,
)

render_exercise(
    exercise_id="4.3",
    title="Pregunta sobre Perros Parte 2",
    instruction="""Corrige el prompt **SIN** anadir etiquetas XML. En su lugar, **elimina solo una o dos palabras** del prompt para que Claude pueda entender la pregunta.

**Prompt original:**
```
Hia its me i have a q about dogs jkaerjv ar cn brown? jklmvca tx it help me muhch much atx fst fst answer short short tx
```

Este ejercicio te mostrara que tipo de lenguaje Claude puede analizar y entender, y cuanto contexto "basura" puede tolerar antes de perder el hilo.

Intenta eliminar la minima cantidad de texto posible para que Claude responda correctamente sobre el color marron (brown) de los perros.""",
    hint='La funcion de calificacion en este ejercicio busca una respuesta que incluya la palabra "brown".\nIntenta eliminar una palabra o seccion de caracteres a la vez, empezando por las partes que tienen menos sentido. Hacer esto palabra por palabra tambien te ayudara a ver cuanto puede o no puede analizar y entender Claude.',
    grade_fn=grade_4_3,
)
