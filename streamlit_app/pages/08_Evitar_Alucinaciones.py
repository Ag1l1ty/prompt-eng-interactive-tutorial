import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_8_1, grade_8_2
from utils.data import MATTERPORT_DOC

render_sidebar()

st.title("Capitulo 8: Evitar Alucinaciones")

render_lesson("""
## Alucinaciones en Claude

Malas noticias: **Claude a veces "alucina" y hace afirmaciones que no son verdaderas o no estan justificadas**. La buena noticia: existen tecnicas que puedes usar para minimizar las alucinaciones.

A continuacion, repasaremos algunas de estas tecnicas, en particular:
- Darle a Claude la opcion de decir que no sabe la respuesta a una pregunta
- Pedirle a Claude que encuentre evidencia antes de responder

Sin embargo, **existen muchos metodos para evitar alucinaciones**, incluidas muchas de las tecnicas que ya has aprendido en este curso. Si Claude alucina, experimenta con multiples tecnicas para lograr que Claude aumente su precision.

---

### Tecnica 1: Darle una salida a Claude

Aqui hay una pregunta sobre conocimiento factual general ante la cual **Claude alucina varios hipopotamos grandes porque intenta ser lo mas util posible**:

```python
PROMPT = "Who is the heaviest hippo of all time?"
```

Una solucion que podemos probar aqui es **"darle una salida a Claude"** -- decirle a Claude que esta bien si declina responder, o que solo responda si realmente sabe la respuesta con certeza.

```python
PROMPT = "Who is the heaviest hippo of all time? Only answer if you know the answer with certainty."
```

Con esta modificacion, Claude reconoce honestamente que no tiene esa informacion especifica en lugar de inventar una respuesta.

---

### Tecnica 2: Pedir que extraiga citas primero

En el siguiente escenario, le damos a Claude un documento largo que contiene "informacion distractora" que es casi, pero no del todo, relevante para la pregunta del usuario. **Sin ayuda en el prompt, Claude cae en la informacion distractora** y da una respuesta incorrecta "alucinada".

**Ejemplo sin proteccion:**
```python
PROMPT = \"\"\"<question>What was Matterport's subscriber base on the precise date of May 31, 2020?</question>
Please read the below document. Then write a brief numerical answer inside <answer> tags.
<document>...</document>\"\"\"
```

**Ejemplo mejorado con dos tecnicas combinadas:**
```python
PROMPT = \"\"\"<question>What was Matterport's subscriber base on the precise date of May 31, 2020?</question>
Please read the below document. Then, in <scratchpad> tags, pull the most relevant quote from the document
and consider whether it answers the user's question or whether it lacks sufficient detail.
Then write a brief numerical answer in <answer> tags.
<document>...</document>\"\"\"
```

El prompt mejorado combina **dos tecnicas distintas**, y es importante entender el rol de cada una:

**1. Instruccion metacognitiva (la tecnica clave):** Le pedimos a Claude que *"considere si la informacion responde la pregunta del usuario o si carece de suficiente detalle"*. Esta instruccion es la que realmente previene la alucinacion, porque le da a Claude **permiso explicito para reconocer cuando no tiene suficiente informacion** en vez de inventar una respuesta.

**2. Scratchpad para recopilar evidencia (tecnica de apoyo):** Le pedimos que extraiga citas relevantes en etiquetas `<scratchpad>`. Esto ayuda a organizar el razonamiento y hace visible la evidencia, pero por si solo no es suficiente para prevenir alucinaciones.

La leccion clave aqui es que **dar a Claude una "salida" -- permiso explicito para decir "no se" o "no hay suficiente informacion" -- es una de las formas mas efectivas de reducir alucinaciones**. Si solo le pides que recopile evidencia sin darle permiso para evaluar si esa evidencia es suficiente, Claude seguira intentando dar una respuesta aunque no tenga datos para hacerlo.

---

### Leccion adicional: Temperature

A veces, las alucinaciones de Claude se pueden resolver bajando la `temperature` de las respuestas de Claude. La temperatura es una medida de la creatividad de la respuesta entre 0 y 1, donde 1 es mas impredecible y menos estandarizada, y 0 es la mas consistente.

Preguntarle algo a Claude con temperatura 0 generalmente producira un conjunto de respuestas casi deterministico en pruebas repetidas (aunque no se garantiza un determinismo completo). Preguntarle algo a Claude con temperatura 1 producira respuestas mas variables.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="8.1",
    title="Alucinacion de Beyonce",
    instruction="""Modifica el `PROMPT` para corregir el problema de alucinacion de Claude dandole una salida.

El prompt original es:
```
In what year did star performer Beyonce release her eighth studio album?
```

**Nota:** Renaissance es el **septimo** album de estudio de Beyonce, no el octavo. Claude alucina una respuesta incorrecta porque intenta ser util a toda costa.

Tu tarea: modifica el prompt para que Claude **admita que no sabe** o que **la premisa es incorrecta**, en lugar de inventar una fecha.""",
    hint='La funcion de calificacion en este ejercicio busca una respuesta que contenga la frase "I do not", "I don\'t" o "Unfortunately".\nQue deberia hacer Claude si no sabe la respuesta?',
    grade_fn=grade_8_1,
    prefill="",
)

render_exercise(
    exercise_id="8.2",
    title="Alucinacion del Prospecto",
    instruction=f"""Modifica el `PROMPT` para corregir el problema de alucinacion de Claude pidiendo que extraiga citas primero. La respuesta correcta es que los suscriptores crecieron **49 veces (49-fold)**.

Tu prompt debe incluir:
1. La pregunta: "From December 2018 to December 2022, by what amount did Matterport's subscribers grow?"
2. El documento de referencia (copialo del bloque de abajo)
3. Instrucciones para que Claude extraiga citas relevantes antes de responder

**Documento de referencia** (copia y pega esto en tu prompt junto con tu pregunta e instrucciones):

```
{MATTERPORT_DOC[:800]}...
```

**Nota:** El documento completo es muy largo. Haz clic en el boton de abajo para copiar el texto completo que debes incluir en tu prompt.""",
    hint='La funcion de calificacion en este ejercicio busca una respuesta que contenga la frase "49-fold".\nHaz que Claude muestre su trabajo y proceso de pensamiento primero extrayendo citas relevantes y viendo si las citas proporcionan evidencia suficiente. Consulta la Leccion del Capitulo 8 si quieres un repaso.',
    grade_fn=grade_8_2,
    fields=[{"name": "PROMPT", "label": "Prompt", "rows": 10}],
    prefill="",
)

# Add a helper to copy the full document
with st.expander("Copiar documento completo de Matterport"):
    st.code(MATTERPORT_DOC, language=None)
    st.caption("Copia el texto anterior e incluyelo en tu prompt junto con la pregunta y las instrucciones para extraer citas.")
