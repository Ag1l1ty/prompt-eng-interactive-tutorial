import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from utils.components import render_sidebar, render_lesson, render_multi_test_exercise
from utils.grading import grade_4_1, grade_4_2, grade_4_3, EMAILS_4

render_sidebar()
st.title("Capitulo 4: Ejemplos y Few-Shot")

render_lesson("""
### Ensenar con ejemplos

Una de las formas mas efectivas de comunicarle a Claude lo que quieres es
**mostrarle ejemplos** del comportamiento deseado. Esta tecnica se conoce como
**few-shot prompting** y es una de las herramientas mas poderosas de la ingenieria de prompts.

---

### Terminologia

- **Zero-shot:** Sin ejemplos. Solo le das la instruccion.
- **One-shot:** Le das **un ejemplo** del formato o comportamiento deseado.
- **Few-shot:** Le das **dos o mas ejemplos** para que Claude identifique el patron.

Mientras mas ejemplos le des (y mas variados sean), mejor entendera Claude
exactamente lo que esperas.

---

### Que ensenan los ejemplos

Los ejemplos no solo muestran *que* responder, sino tambien:

- **Formato:** longitud, estructura, uso de tags
- **Tono:** formal, casual, empatico, tecnico
- **Patron de razonamiento:** como llegar a la respuesta

#### Ejemplo: Bot de servicio al cliente

Imagina que quieres que Claude responda como un agente de atencion al cliente
con empatia. Puedes darle un ejemplo dentro de tu prompt:

> **Prompt:**
>
> Eres un agente de servicio al cliente. Responde siempre con empatia,
> reconociendo el problema del cliente antes de ofrecer una solucion.
>
> **Ejemplo de conversacion:**
>
> **Cliente:** Mi pedido llego danado y estoy muy frustrado.
>
> **Agente:** Lamento mucho escuchar eso. Entiendo lo frustrante que debe ser
> recibir un producto danado. Vamos a resolverlo de inmediato.
> Tengo dos opciones para usted: un reemplazo con envio express
> o un reembolso completo. Cual prefiere?
>
> Ahora responde al siguiente cliente:
>
> **Cliente:** Llevo 3 dias esperando una respuesta a mi ticket de soporte.

Con este ejemplo, Claude no solo sabe *que* responder, sino *como* estructurar su respuesta:
primero empatia, luego opciones concretas.

---

### Chain of Thought en clasificacion

Cuando combinas ejemplos con la instruccion de **"pensar paso a paso"**,
la precision de Claude mejora significativamente. Esto es especialmente util
en tareas de clasificacion.

La idea es simple: en vez de pedirle a Claude que de la respuesta directamente,
le pides que **razone primero** y **luego** de su respuesta final.

> **Sin Chain of Thought:**
>
> **Prompt:** "Clasifica este email: 'Quiero saber si el Mixmaster funciona con 220V'"
>
> **Respuesta:** "A) Pregunta de pre-venta"

> **Con Chain of Thought:**
>
> **Prompt:** "Analiza este email paso a paso. Identifica las palabras clave,
> el tono y la intencion. Luego da tu clasificacion final en tags `<answer>`."
>
> **Respuesta:** "El cliente pregunta sobre voltaje del producto, lo cual indica
> que aun no lo ha comprado. Es una consulta tecnica previa a la compra.
> `<answer>A</answer>`"

El razonamiento explicito reduce errores, especialmente en casos ambiguos.

---

### Emails de prueba

En los ejercicios de abajo, tu prompt sera probado con **4 emails diferentes**
automaticamente. Esto simula un escenario real donde necesitas un prompt
que funcione de manera consistente con multiples entradas.

Las categorias de clasificacion son:

- **(A)** Pregunta de pre-venta
- **(B)** Articulo roto o defectuoso
- **(C)** Pregunta de facturacion
- **(D)** Otro

Tu prompt debe usar `{email}` como marcador donde se insertara cada email de prueba.
""")

st.divider()
st.header("Ejercicios")

test_cases = [{"content": email, "index": i} for i, email in enumerate(EMAILS_4)]

render_multi_test_exercise(
    exercise_id="4.1",
    title="Clasificacion de Emails",
    instruction="Escribe una plantilla de prompt con `{email}` como marcador para clasificar emails en 4 categorias:\n\n- **(A)** Pregunta de pre-venta\n- **(B)** Articulo roto o defectuoso\n- **(C)** Pregunta de facturacion\n- **(D)** Otro\n\nLa respuesta debe incluir la letra y la categoria completa, ej: `B) Articulo roto o defectuoso`.",
    hint="Incluye las 4 categorias en tu prompt. Dile a Claude que responda SOLO con la clasificacion.",
    test_cases=test_cases,
    grade_fn=grade_4_1,
    prompt_template="Clasifica este email: {email}",
)

render_multi_test_exercise(
    exercise_id="4.2",
    title="Clasificacion con Razonamiento",
    instruction="Mejora tu prompt para que Claude **piense paso a paso** antes de dar la respuesta final. La respuesta final debe ir dentro de tags `<answer>X</answer>` donde X es la letra (A, B, C o D).\n\nEsta tecnica de 'pensar antes de responder' mejora significativamente la precision.",
    hint="Dile a Claude que analice el email paso a paso y luego ponga su respuesta final en tags <answer>. Puedes dar un ejemplo del formato deseado con tags <example>.",
    test_cases=test_cases,
    grade_fn=grade_4_2,
    prompt_template="Clasifica este email: {email}",
)

render_multi_test_exercise(
    exercise_id="4.3",
    title="Clasificacion con Ejemplos (Few-Shot)",
    instruction="Ahora usa **ejemplos (few-shot)** para ensenarle a Claude como clasificar. Incluye 2-3 emails de ejemplo con su clasificacion correcta. Claude debe aprender el formato de tu ejemplo.\n\nLa respuesta debe terminar con la letra de la categoria correcta.",
    hint="Escribe 2-3 emails inventados con su clasificacion. Usa un formato consistente que termine con la letra. Asegurate de incluir las categorias y el placeholder {email}.",
    test_cases=test_cases,
    grade_fn=grade_4_3,
    prompt_template="Clasifica este email: {email}",
    prefill="La categoria correcta es:",
)
