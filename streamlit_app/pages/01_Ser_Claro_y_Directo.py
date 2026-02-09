import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_1_1, grade_1_2, grade_1_3

render_sidebar()
st.title("Capitulo 1: Ser Claro y Directo")

render_lesson("""
### La regla de oro de la claridad

Hay una regla simple que resume todo este capitulo:

> **Si le muestras tu prompt a un colega y no lo entiende, Claude tampoco lo va a entender.**

Claude es increiblemente capaz, pero no puede leer tu mente. Si tu prompt es ambiguo,
vago o incompleto, la respuesta de Claude tambien lo sera.

---

### Se especifico

Evita preguntas genericas. Mientras mas contexto y restricciones le des a Claude,
mejor sera su respuesta.

> **Prompt vago:** "Quien es el mejor jugador?"
>
> *Problema: Mejor jugador de que? De futbol, baloncesto, ajedrez? De todos los tiempos o actual?*

> **Prompt especifico:** "Si tuvieras que elegir UN solo jugador como el mejor basquetbolista de todos los tiempos, quien seria? Responde solo con el nombre."
>
> *Ahora Claude sabe exactamente que tipo de respuesta dar.*

---

### Se directo

No le des vueltas al asunto. Pide exactamente lo que quieres, sin rodeos ni
preambulos innecesarios.

Veamos la diferencia entre un prompt vago y uno directo:

> **Prompt vago:** "Escribe un haiku sobre robots"
>
> **Respuesta tipica:** "Claro, con mucho gusto te escribo un haiku sobre robots.
> Los haikus son una forma poetica japonesa que... *(preambulo innecesario)*
>
> Metal y circuitos / despiertan bajo la luz / alma de acero"

> **Prompt directo:** "Escribe un haiku sobre robots. Ve directo al poema, sin preambulo."
>
> **Respuesta:** "Metal y circuitos / despiertan bajo la luz / alma de acero"

La diferencia es clara: el prompt directo elimina el relleno y va al grano.

---

### Consejos practicos

- **Di lo que quieres, no lo que no quieres.** "Responde solo con el nombre" es mejor
  que "No agregues explicaciones".
- **Especifica el formato.** Si quieres una lista, un parrafo, un numero, pidelo.
- **Da contexto.** Si la pregunta tiene multiples interpretaciones, aclara cual te interesa.
- **Se conciso pero completo.** No hace falta escribir un ensayo como prompt,
  pero tampoco dejes informacion importante fuera.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="1.1",
    title="Respuesta Exacta",
    instruction="Escribe un prompt que haga que Claude responda EXACTAMENTE con **'Michael Jordan'**, sin ninguna otra palabra ni explicacion.",
    hint="La funcion de calificacion busca EXACTAMENTE 'Michael Jordan'. Como le pedirias a alguien que respondiera solo con un nombre, sin agregar nada mas? Se lo mas directo posible.",
    grade_fn=grade_1_1,
)

render_exercise(
    exercise_id="1.2",
    title="Correccion Directa",
    instruction="Usa un **system prompt** con un rol apropiado y un **prompt de usuario** para que Claude identifique el error en esta ecuacion:\n\n`2x - 3 = 9, por lo tanto 2x = 6`\n\nClaude debe indicar claramente que el resultado es **incorrecto**.",
    hint="Dale a Claude un rol de experto matematico en el system prompt. El error es que si 2x - 3 = 9, entonces 2x = 12, no 6. Asegurate de que Claude use la palabra 'incorrecto' o 'no es correcto' en su respuesta.",
    grade_fn=grade_1_2,
    fields=[
        {"name": "SYSTEM_PROMPT", "label": "System Prompt", "rows": 3},
        {"name": "PROMPT", "label": "Prompt", "rows": 4},
    ],
)

render_exercise(
    exercise_id="1.3",
    title="Respuesta Detallada",
    instruction="Escribe un prompt que haga que Claude genere una respuesta de al menos **800 palabras**. Tip: los LLMs no son buenos contando palabras exactamente, asi que apunta mas alto en tu solicitud.",
    hint="Pide explicitamente mas de 1000 palabras. Puedes solicitar un ensayo, una historia, o un analisis detallado sobre algun tema. Mientras mas especifico sea el tema, mas facil sera para Claude generar contenido extenso.",
    grade_fn=grade_1_3,
)
