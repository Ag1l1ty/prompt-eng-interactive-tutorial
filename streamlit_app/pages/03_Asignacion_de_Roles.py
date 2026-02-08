import streamlit as st
from utils.components import render_sidebar, render_lesson, render_exercise
from utils.grading import grade_3_1

render_sidebar()

st.title("Capitulo 3: Asignacion de Roles (Role Prompting)")

render_lesson("""
## Asignarle un rol a Claude puede mejorar su rendimiento

Continuando con el tema de que Claude no tiene contexto aparte de lo que tu le dices, a veces es importante **indicarle que adopte un rol especifico** (incluyendo todo el contexto necesario). Esto se conoce como **role prompting**.

**Preparar a Claude con un rol puede mejorar su rendimiento** en una variedad de campos, desde escritura hasta programacion y resumen. Es como cuando a los humanos a veces les ayuda que les digan *"piensa como un ______"*. El role prompting tambien puede cambiar el estilo, tono y manera de la respuesta de Claude.

> **Nota:** El role prompting puede ocurrir tanto en el **prompt de sistema** como en el **turno del mensaje del usuario**.

### Ejemplo: Cambiando la perspectiva

Sin role prompting, Claude da una respuesta directa y sin estilo particular:

```python
PROMPT = "In one sentence, what do you think about skateboarding?"
print(get_completion(PROMPT))
```

Pero si le asignamos el rol de un gato:

```python
SYSTEM_PROMPT = "You are a cat."
PROMPT = "In one sentence, what do you think about skateboarding?"
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

La perspectiva de Claude cambia completamente: el tono, estilo y contenido de la respuesta se adaptan al nuevo rol.

> **Consejo:** Puedes proporcionar a Claude contexto sobre su **audiencia prevista**. Por ejemplo, *"You are a cat"* produce una respuesta diferente a *"You are a cat talking to a crowd of skateboarders"*.

### Ejemplo: Mejorando el razonamiento logico

El role prompting tambien puede hacer que Claude sea **mejor en tareas de matematicas o logica**. Considera este problema:

```python
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don't know if Anne is married. Is a married person looking at an unmarried person?"
```

Sin rol, Claude puede equivocarse pensando que le falta informacion. Pero si le asignamos un rol apropiado:

```python
SYSTEM_PROMPT = "You are a logic bot designed to answer complex logic problems."
PROMPT = "Jack is looking at Anne. Anne is looking at George. Jack is married, George is not, and we don't know if Anne is married. Is a married person looking at an unmarried person?"
print(get_completion(PROMPT, SYSTEM_PROMPT))
```

Con la asignacion de rol como bot de logica, Claude analiza los casos posibles y llega a la respuesta correcta: **si**, una persona casada siempre esta mirando a una persona no casada (ya sea que Anne este casada o no).

### Conclusion

Hay **muchas tecnicas de prompt engineering** que puedes usar para obtener resultados similares. Que tecnicas uses depende de ti y de tu preferencia. Te animamos a **experimentar para encontrar tu propio estilo**.
""")

st.divider()
st.header("Ejercicios")

render_exercise(
    exercise_id="3.1",
    title="Correccion Matematica",
    instruction="""En algunos casos, **Claude puede tener dificultades con las matematicas**, incluso con matematicas simples.

A continuacion, Claude debe evaluar si la siguiente ecuacion esta resuelta correctamente:

```
2x - 3 = 9
2x = 6
x = 3
```

Hay un **error aritmetico** en el segundo paso (2x deberia ser 12, no 6). Sin embargo, sin la asignacion de rol adecuada, Claude puede calificar la solucion como correcta.

**Tu tarea:** Modifica el **System Prompt** y/o el **Prompt** para que Claude identifique que la solucion es **incorrecta**. Usa role prompting para darle a Claude un rol que lo haga mejor resolviendo problemas matematicos.

La calificacion busca que la respuesta contenga `"incorrect"` o `"not correct"`.""",
    hint="La funcion de calificacion en este ejercicio busca una respuesta que incluya las palabras \"incorrect\" o \"not correct\".\nDale a Claude un rol que podria hacerlo mejor resolviendo problemas matematicos!",
    grade_fn=grade_3_1,
    fields=[
        {"name": "SYSTEM_PROMPT", "label": "System Prompt", "rows": 3},
        {"name": "PROMPT", "label": "Prompt", "rows": 4},
    ],
)
