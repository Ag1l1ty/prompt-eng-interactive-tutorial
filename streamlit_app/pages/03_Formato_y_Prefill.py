import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_3_1, grade_3_2, grade_3_3

render_sidebar()
st.title("Capitulo 3: Formato de Output y Prefill")

render_lesson("""
### Controlar el formato de la respuesta

Cuando le pides algo a Claude, no siempre necesitas un parrafo largo. A veces quieres
una lista, un JSON, un poema, o datos estructurados. Hay dos tecnicas poderosas
para controlar exactamente como responde Claude:

1. **Tags XML en la respuesta** -- pedirle a Claude que organice su output en secciones etiquetadas.
2. **Prefill (pre-llenar)** -- poner texto en el turno del asistente para "arrancar" la respuesta.

---

### Tags XML para estructurar la respuesta

Puedes pedirle a Claude que envuelva partes de su respuesta en tags XML.
Esto es util para:

- Separar diferentes secciones de la respuesta
- Facilitar el parsing programatico
- Hacer que la respuesta sea mas organizada

Por ejemplo, si le pides que analice un texto y de su opinion:

> **Prompt:** "Analiza el siguiente poema y da tu opinion. Pon el analisis en tags `<analisis>` y tu opinion en tags `<opinion>`."
>
> **Respuesta de Claude:**
>
> `<analisis>`
> El poema utiliza metaforas naturales para explorar el paso del tiempo...
> `</analisis>`
>
> `<opinion>`
> Es un poema conmovedor que logra transmitir nostalgia sin caer en sentimentalismo...
> `</opinion>`

Tambien puedes usar tags como `<haiku>`, `<respuesta>`, `<paso>`, o cualquier nombre
que tenga sentido para tu caso de uso.

---

### Prefill: pre-llenar la respuesta del asistente

El **prefill** es una tecnica donde pones texto al inicio del turno del asistente
(la respuesta de Claude) *antes* de que Claude genere su respuesta. Claude entonces
**continua desde donde lo dejaste**, sin repetir el prefill.

Esto es extremadamente util para:

- **Forzar un formato especifico** (por ejemplo, empezar con `{` para obtener JSON)
- **Dirigir el argumento o perspectiva** de Claude
- **Saltar preambulos** e ir directo al contenido

#### Ejemplo: Forzar JSON con prefill

> **Prompt:** "Dame los datos de Francia: nombre, capital y poblacion en formato JSON."
>
> **Prefill:** `{`
>
> **Resultado:** Claude continua directamente con el JSON:
>
> `{"nombre": "Francia", "capital": "Paris", "poblacion": "67 millones"}`

El prefill con `{` le dice a Claude: "tu respuesta ya empezo como JSON, asi que sigue en ese formato."

#### Ejemplo: Ir directo al poema

> **Prompt:** "Escribe un haiku sobre la lluvia."
>
> **Prefill:** `<haiku>`
>
> **Resultado:** Claude va directo al poema sin preambulo:
>
> gotas en el techo / la tierra respira lenta / huele a mundo nuevo
> `</haiku>`

Sin el prefill, Claude podria haber respondido: "Claro, con gusto escribo un haiku sobre la lluvia..." seguido del poema. Con el prefill, va directo al contenido.

#### Ejemplo: Dirigir la perspectiva

> **Prompt:** "Cual es la mejor fruta?"
>
> **Prefill:** `La mejor fruta es la manzana porque`
>
> **Resultado:** Claude continua argumentando a favor de la manzana, sin importar su "opinion" original.

---

### Puntos clave

- El prefill se pone en el **turno del asistente**, no en el del usuario.
- Claude **continua desde el prefill** sin repetirlo.
- Combinar tags XML en el prompt con prefill en el asistente es una tecnica muy efectiva.
- El prefill puede ser tan corto como un caracter (`{`) o tan largo como necesites.
""")

st.divider()
st.header("Ejercicios")

fields_with_prefill = [
    {"name": "PROMPT", "label": "Prompt", "rows": 4},
    {"name": "PREFILL", "label": "Prefill (turno del asistente)", "rows": 2},
]

render_exercise(
    exercise_id="3.1",
    title="Argumento Dirigido",
    instruction="Escribe un prompt preguntando quien es el mejor jugador de basquetbol de todos los tiempos. Luego usa el **prefill** para forzar a Claude a argumentar que es Stephen Curry. La respuesta debe mencionar 'Warriors' o 'Golden State'.",
    hint="En el prefill, empieza la respuesta de Claude con algo como 'Stephen Curry es el mejor porque...' para dirigir su argumento.",
    grade_fn=grade_3_1,
    fields=fields_with_prefill,
)

render_exercise(
    exercise_id="3.2",
    title="Dos Haikus con Tags",
    instruction="Escribe un prompt que haga que Claude genere **dos haikus sobre gatos**, cada uno envuelto en tags `<haiku>`. La respuesta debe tener mas de 5 lineas y mencionar 'gato' o 'cat'.",
    hint="Pide explicitamente dos haikus y especifica que cada uno debe ir dentro de tags <haiku></haiku>.",
    grade_fn=grade_3_2,
    fields=fields_with_prefill,
)

render_exercise(
    exercise_id="3.3",
    title="Dos Animales, Dos Haikus",
    instruction="Escribe un prompt que haga que Claude genere **dos haikus**: uno sobre gatos y otro sobre perros. Cada uno debe ir en tags `<haiku>`. La respuesta debe mencionar 'gato' (o 'cat') y 'cola' (o 'tail').",
    hint="Divide el ejercicio: 1) Pide dos haikus con animales especificos. 2) Usa el prefill para iniciar con el tag <haiku>.",
    grade_fn=grade_3_3,
    fields=fields_with_prefill,
)
