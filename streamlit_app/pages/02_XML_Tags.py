import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_2_1, grade_2_2, grade_2_3

render_sidebar()
st.title("Capitulo 2: Estructurar Prompts con XML Tags")

render_lesson("""
### Plantillas de prompt con variables

Cuando trabajas con prompts de forma programatica, es comun usar **plantillas** con
variables que se sustituyen antes de enviar el prompt a Claude. Por ejemplo:

> **Plantilla:** "Escribe un poema sobre {TEMA}"
>
> **Prompt final:** "Escribe un poema sobre la lluvia"

Esto funciona bien para casos simples, pero cuando las variables contienen texto
largo o complejo, surge un problema.

---

### El problema: donde terminan las instrucciones y empiezan los datos?

Cuando sustituyes una variable con texto real, **Claude no sabe donde terminan
tus instrucciones y donde empiezan los datos del usuario**. Esto puede causar
confusiones.

> **Sin tags:** "Reescribe este email de forma mas profesional: Hola jefe necesito vacaciones ya"
>
> *Problema: Claude podria no estar seguro de donde empieza exactamente el email
> a reescribir. Que pasa si el email tuviera instrucciones dentro?*

> **Con tags:** "Reescribe este email de forma mas profesional:
>
> `<email>`Hola jefe necesito vacaciones ya`</email>`"
>
> *Ahora Claude entiende claramente que es instruccion y que es datos.*

---

### La solucion: tags XML como delimitadores

Claude esta **especificamente entrenado para reconocer tags XML** como elementos
de estructura en un prompt. Puedes usar tags como:

- `<email>...</email>` para contenido de un email
- `<pregunta>...</pregunta>` para una pregunta del usuario
- `<datos>...</datos>` para datos de entrada
- `<instrucciones>...</instrucciones>` para separar las instrucciones
- `<documento>...</documento>` para un documento de referencia

Los nombres de los tags pueden ser los que tu quieras. Lo importante es que
**delimiten claramente** donde empieza y termina cada seccion.

---

### Por que funcionan tan bien los tags XML?

1. **Separacion clara** entre instrucciones y datos
2. **Claude los reconoce** como estructura, no como contenido
3. **Facilitan prompts complejos** con multiples secciones de datos
4. **Previenen inyeccion de prompts** al aislar el contenido del usuario

Veamos un ejemplo mas complejo:

> **Sin tags:**
> "Dado el siguiente texto, responde la pregunta.
> Texto: La capital de Francia es Paris y tiene mas de 2 millones de habitantes.
> Pregunta: Cual es la capital de Francia?"
>
> *Funciona, pero es fragil. Si el texto contuviera la palabra "Pregunta:", Claude se confundiria.*

> **Con tags:**
> "Dado el siguiente texto, responde la pregunta.
>
> `<texto>`La capital de Francia es Paris y tiene mas de 2 millones de habitantes.`</texto>`
>
> `<pregunta>`Cual es la capital de Francia?`</pregunta>`"
>
> *Ahora cada parte esta perfectamente delimitada, sin ambiguedad.*

---

### Consejos para usar XML tags

- **Usa nombres descriptivos** para los tags: `<email>`, `<codigo>`, `<contexto>`
- **Se consistente** con los nombres que eliges
- **No te excedas**: usa tags solo cuando aporten claridad
- **Combinalos con instrucciones claras** para mejores resultados
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="2.1",
    title="Haiku con Tema",
    instruction="Escribe un prompt que haga que Claude escriba un **haiku sobre cerdos**. La respuesta debe contener las palabras 'haiku' y 'cerdo' (o 'cerdos').",
    hint="No olvides ser directo. Simplemente pide un haiku sobre cerdos. Asegurate de que Claude mencione la palabra 'haiku' en su respuesta (por ejemplo, pidiendo que titule el poema).",
    grade_fn=grade_2_1,
)

render_exercise(
    exercise_id="2.2",
    title="Texto Confuso con XML",
    instruction="""El siguiente texto esta desordenado y contiene una pregunta escondida. Usa **tags XML** para aislar la pregunta y que Claude la responda correctamente:

`Hola soi io teng una prgnta sobr perros jkaerjv ar cn marron? jklmvca grs`

La pregunta real es: "Los perros pueden ser de color marron?" Reestructura el prompt con tags XML para que Claude responda correctamente.""",
    hint="Rodea la pregunta real con tags XML como <pregunta>...</pregunta> para que Claude la identifique claramente. Por ejemplo: <pregunta>Los perros pueden ser de color marron?</pregunta>",
    grade_fn=grade_2_2,
)

render_exercise(
    exercise_id="2.3",
    title="Minimo Contexto Necesario",
    instruction="""Usando el mismo texto confuso del ejercicio anterior, esta vez **NO** uses tags XML. En su lugar, elimina las partes innecesarias del texto hasta que Claude pueda responder la pregunta correctamente.

Texto original: `Hola soi io teng una prgnta sobr perros jkaerjv ar cn marron? jklmvca grs`

Que tan poco texto necesitas para que Claude entienda la pregunta?""",
    hint="Elimina las palabras sin sentido una por una. La pregunta clave es sobre si los perros pueden ser de color marron. Que tan pocas palabras necesita Claude para entender y responder correctamente?",
    grade_fn=grade_2_3,
)
