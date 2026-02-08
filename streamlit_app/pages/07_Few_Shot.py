import streamlit as st
from utils.components import render_sidebar, render_lesson, render_multi_test_exercise
from utils.grading import grade_7_1, EMAILS_6

render_sidebar()

st.title("Capitulo 7: Uso de Ejemplos / Few-Shot Prompting")

render_lesson("""
## Darle a Claude ejemplos de lo que quieres

**Darle a Claude ejemplos de como quieres que se comporte (o como no quieres que se comporte) es extremadamente efectivo** para:
- Obtener la respuesta correcta
- Obtener la respuesta en el formato correcto

Este tipo de prompting se llama "**prompting con ejemplos (few-shot)**". Tambien podrias encontrar la frase "zero-shot" o "n-shot" o "one-shot". El numero de "shots" se refiere a cuantos ejemplos se usan dentro del prompt.

### Ejemplo: Bot para padres

Imagina que eres un desarrollador intentando construir un "bot para padres" que responde preguntas de ninos. La respuesta predeterminada de Claude es bastante formal y robotica:

```python
PROMPT = "Will Santa bring me presents on Christmas?"
```

Podrias tomarte el tiempo de describir el tono deseado, pero es mucho mas facil simplemente **darle a Claude algunos ejemplos de respuestas ideales**:

```python
PROMPT = \\"\\"\\"Please complete the conversation by writing the next line, speaking as "A".
Q: Is the tooth fairy real?
A: Of course, sweetie. Wrap up your tooth and put it under your pillow tonight. \
There might be something waiting for you in the morning.
Q: Will Santa bring me presents on Christmas?\\"\\"\\"
```

Con un solo ejemplo, Claude entiende el tono deseado y responde de manera calida y paternal.

### Ejemplo: Extraccion y formato

En lugar de guiar a Claude paso a paso con instrucciones complejas de formato, simplemente podemos **proporcionarle algunos ejemplos correctamente formateados y Claude puede extrapolar a partir de ahi**.

```python
PROMPT = \\"\\"\\"Silvermist Hollow, a charming village, was home to an extraordinary group...
Among them was Dr. Liam Patel, a neurosurgeon...
Olivia Chen was an innovative architect...
<individuals>
1. Dr. Liam Patel [NEUROSURGEON]
2. Olivia Chen [ARCHITECT]
...
</individuals>

At the heart of the town, Chef Oliver Hamilton has transformed the culinary scene...
<individuals>
1. Oliver Hamilton [CHEF]
2. Elizabeth Chen [LIBRARIAN]
...
</individuals>

Oak Valley, a charming small town, is home to a remarkable trio...\\"\\"\\"

PREFILL = "<individuals>"
```

Con los dos primeros parrafos como ejemplos formateados, Claude extrae nombres y profesiones del tercer parrafo usando exactamente el mismo formato, sin necesidad de instrucciones explicitas sobre como hacerlo.

### Conclusion

El few-shot prompting es particularmente util cuando:
- El formato de output deseado es complejo o inusual
- Es mas facil **mostrar** que **describir** lo que quieres
- Necesitas consistencia en el estilo, tono o formato
- Las instrucciones escritas serian demasiado largas o confusas
""")

st.divider()
st.header("Ejercicios")

# Build test cases from EMAILS_6
test_cases = [{"content": email, "index": i} for i, email in enumerate(EMAILS_6)]

# ── Exercise 7.1 ──────────────────────────────────────────────────────────────

render_multi_test_exercise(
    exercise_id="7.1",
    title="Formato de Correos via Ejemplos",
    instruction="""Vamos a rehacer la clasificacion de correos, pero esta vez usando **ejemplos few-shot**.

Edita la plantilla de prompt para incluir **ejemplos de correos con su clasificacion correcta**, de modo que Claude aprenda el formato y las categorias a partir de ellos.

Las categorias siguen siendo:
- **(A)** Pregunta de pre-venta
- **(B)** Articulo roto o defectuoso
- **(C)** Pregunta de facturacion
- **(D)** Otro (por favor explique)

**Objetivo:** La **ultima letra** de la respuesta de Claude debe ser la letra de la categoria correcta.

**Consejos:**
- Incluye al menos dos correos de ejemplo con su clasificacion
- El formato de respuesta en tus ejemplos debe terminar con la letra de la categoria
- No es necesario dar un ejemplo para cada categoria
- Asegurate de mantener `{email}` como marcador para el correo a clasificar
- Puedes usar el campo de prefill para guiar el inicio de la respuesta de Claude""",
    hint="""Vas a tener que escribir algunos emails de ejemplo y clasificarlos para Claude (con el formato exacto que quieres). Hay multiples formas de hacer esto. Aqui hay algunas pautas:
1. Intenta tener al menos dos emails de ejemplo. Claude no necesita un ejemplo para todas las categorias.
2. Asegurate de que el formato de respuesta de tu ejemplo sea exactamente el formato que quieres que Claude use, para que Claude pueda emular el formato tambien. Este formato deberia hacer que la respuesta de Claude termine con la letra de la categoria.
3. Asegurate de que todavia tengas las categorias listadas dentro del prompt, de lo contrario Claude no sabra a que categorias hacer referencia, y tambien {email} como placeholder para sustitucion.""",
    test_cases=test_cases,
    grade_fn=grade_7_1,
    prompt_template="Please classify this email as either green or blue: {email}",
    prefill="",
)
