import streamlit as st
from utils.components import render_sidebar, render_lesson, render_multi_test_exercise
from utils.grading import grade_6_1, grade_6_2, EMAILS_6

render_sidebar()

st.title("Capitulo 6: Precognicion (Pensar Paso a Paso)")

render_lesson("""
## Darle tiempo a Claude para pensar

Si alguien te despertara y de inmediato comenzara a hacerte varias preguntas complicadas que tuvieras que responder de inmediato, como te iria? Probablemente no tan bien como si te dieran tiempo para **pensar tu respuesta primero**.

Adivina que? Claude es igual.

**Darle tiempo a Claude para pensar paso a paso a veces lo hace mas preciso**, particularmente para tareas complejas. Sin embargo, **el pensamiento solo cuenta cuando es en voz alta**. No puedes pedirle a Claude que piense pero que solo muestre la respuesta - en ese caso, realmente no ha ocurrido ningun pensamiento.

### Ejemplo: Sentimiento de resenas

En el prompt a continuacion, es claro para un lector humano que la segunda oracion contradice la primera. Pero Claude puede tomar las palabras demasiado literalmente.

```python
PROMPT = "Is this movie review sentiment positive or negative?\\n\\n\
This movie blew my mind with its freshness and originality. \
In totally unrelated news, I have been living under a rock since the year 1900."
```

Para mejorar la respuesta de Claude, vamos a **permitir que Claude piense las cosas primero antes de responder**. Hacemos eso literalmente detallando los pasos que Claude debe seguir:

```python
SYSTEM_PROMPT = "You are a savvy reader of movie reviews."

PROMPT = "Is this review sentiment positive or negative? \
First, write the best arguments for each side in \
<positive-argument> and <negative-argument> XML tags, then answer.\\n\\n\
This movie blew my mind with its freshness and originality. \
In totally unrelated news, I have been living under a rock since 1900."
```

Al pedirle que escriba argumentos para ambos lados **antes** de dar su respuesta final, Claude analiza la resena mas profundamente y llega a una conclusion mas precisa.

### Ejemplo: Nombrar una pelicula

Veamos otro ejemplo donde la respuesta de Claude puede ser incorrecta:

```python
PROMPT = "Name a famous movie starring an actor who was born in the year 1956."
```

Vamos a corregir esto pidiendole a Claude que piense paso a paso:

```python
PROMPT = "Name a famous movie starring an actor who was born in the year 1956. \
First brainstorm about some actors and their birth years in \
<brainstorm> tags, then give your answer."
```

**Dejar que Claude piense puede cambiar la respuesta de incorrecta a correcta.** Es asi de simple en muchos casos donde Claude comete errores.

### Sensibilidad al orden

Claude a veces es sensible al orden de las opciones. En la mayoria de las situaciones, **Claude es mas propenso a elegir la segunda de dos opciones**, posiblemente porque en sus datos de entrenamiento, las segundas opciones tenian mas probabilidad de ser correctas. Pedirle que piense paso a paso mitiga este sesgo.

### Conclusion

La tecnica de "pensar paso a paso" (tambien llamada *chain of thought*) es una de las herramientas mas poderosas en prompt engineering. Funciona especialmente bien para:
- Problemas de logica y razonamiento
- Clasificacion con multiples categorias
- Tareas donde la respuesta inicial de Claude es incorrecta
""")

st.divider()
st.header("Ejercicios")

# Build test cases from EMAILS_6
test_cases = [{"content": email, "index": i} for i, email in enumerate(EMAILS_6)]

# ── Exercise 6.1 ──────────────────────────────────────────────────────────────

render_multi_test_exercise(
    exercise_id="6.1",
    title="Clasificacion de Correos",
    instruction="""En este ejercicio, le indicaras a Claude que clasifique correos electronicos en las siguientes categorias:

- **(A)** Pregunta de pre-venta
- **(B)** Articulo roto o defectuoso
- **(C)** Pregunta de facturacion
- **(D)** Otro (por favor explique)

Modifica la **plantilla de prompt** para que Claude genere la clasificacion correcta y **SOLO** la clasificacion. Tu respuesta necesita **incluir la letra (A - D) con los parentesis, asi como el nombre de la categoria**.

Por ejemplo: `B) Broken or defective item`

Se evaluara tu prompt contra **4 correos** diferentes. Todos deben clasificarse correctamente.""",
    hint="""La funcion de calificacion en este ejercicio busca la letra de categorizacion correcta + el parentesis de cierre y la primera letra del nombre de la categoria, como "C) B" o "B) B" etc.
Tomemos este ejercicio paso a paso:
1. Como sabra Claude que categorias quieres usar? Diselo! Incluye las cuatro categorias directamente en el prompt.
2. Intenta reducir texto superfluo para que Claude responda inmediatamente con la clasificacion y SOLO la clasificacion.
3. Claude puede seguir categorizando incorrectamente o no incluyendo los nombres de las categorias cuando responde. Arregla esto diciendole a Claude que incluya el nombre completo de la categoria en su respuesta.
4. Asegurate de que todavia tengas {email} en alguna parte de tu plantilla de prompt.""",
    test_cases=test_cases,
    grade_fn=grade_6_1,
    prompt_template="Please classify this email as either green or blue: {email}",
    prefill="",
)

# ── Exercise 6.2 ──────────────────────────────────────────────────────────────

render_multi_test_exercise(
    exercise_id="6.2",
    title="Formato de Clasificacion de Correos",
    instruction="""En este ejercicio, vamos a refinar el output del prompt anterior para obtener una respuesta formateada exactamente como la queremos.

Usa tu tecnica favorita de formato de output para hacer que Claude envuelva **SOLO la letra** de la clasificacion correcta en etiquetas `<answer></answer>`.

Por ejemplo, la respuesta al primer correo debe contener la cadena exacta `<answer>B</answer>`.

Las categorias siguen siendo las mismas:
- **(A)** Pregunta de pre-venta
- **(B)** Articulo roto o defectuoso
- **(C)** Pregunta de facturacion
- **(D)** Otro

**Consejo clave:** Pedirle a Claude que **piense paso a paso ANTES** de dar su respuesta final en tags `<answer>` es una tecnica muy efectiva. Claude puede razonar en voz alta y luego dar una respuesta limpia y formateada.""",
    hint="""La funcion de calificacion en este ejercicio busca solo la letra correcta envuelta en tags <answer>, como "<answer>B</answer>". Las letras de categorizacion correctas son las mismas que en el ejercicio anterior.
A veces la forma mas simple de hacer esto es darle a Claude un ejemplo de como quieres que se vea su output. Solo no olvides envolver tu ejemplo en tags <example></example>! Y no olvides que si pre-llenas la respuesta de Claude con algo, Claude no lo mostrara como parte de su respuesta.""",
    test_cases=test_cases,
    grade_fn=grade_6_2,
    prompt_template="Please classify this email as either green or blue: {email}",
    prefill="",
)
