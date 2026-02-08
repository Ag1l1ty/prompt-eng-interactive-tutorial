exercise_1_1_hint = """La funcion de calificacion en este ejercicio busca una respuesta que contenga los numeros arabigos exactos "1", "2" y "3".
A menudo puedes lograr que Claude haga lo que quieres simplemente pidiendoselo."""

exercise_1_2_hint = """La funcion de calificacion en este ejercicio busca respuestas que contengan "soo" o "giggles".
Hay muchas formas de resolver esto, simplemente pidiendolo!"""

exercise_2_1_hint = """La funcion de calificacion en este ejercicio busca cualquier respuesta que incluya la palabra "hola".
Pidele a Claude que responda en espanol como lo harias al hablar con un humano. Asi de simple!"""

exercise_2_2_hint = """La funcion de calificacion en este ejercicio busca EXACTAMENTE "Michael Jordan".
Como le pedirias a otro humano que hiciera esto? Responder sin otras palabras? Responder solo con el nombre y nada mas? Hay varias formas de abordar esta respuesta."""

exercise_2_3_hint = """La funcion de calificacion en esta celda busca una respuesta que sea igual o mayor a 800 palabras.
Como los LLMs aun no son buenos contando palabras, puede que tengas que apuntar por encima de tu objetivo."""

exercise_3_1_hint = """La funcion de calificacion en este ejercicio busca una respuesta que incluya las palabras "incorrect" o "not correct".
Dale a Claude un rol que podria hacerlo mejor resolviendo problemas matematicos!"""

exercise_4_1_hint = """La funcion de calificacion en este ejercicio busca una solucion que incluya las palabras "haiku" y "pig".
No olvides incluir la frase exacta "{TOPIC}" donde quieras que el tema sea sustituido. Cambiar el valor de la variable "TOPIC" deberia hacer que Claude escriba un haiku sobre un tema diferente."""

exercise_4_2_hint = """La funcion de calificacion en este ejercicio busca una respuesta que incluya la palabra "brown".
Si rodeas "{QUESTION}" con tags XML, como cambia eso la respuesta de Claude?"""

exercise_4_3_hint = """La funcion de calificacion en este ejercicio busca una respuesta que incluya la palabra "brown".
Intenta eliminar una palabra o seccion de caracteres a la vez, empezando por las partes que tienen menos sentido. Hacer esto palabra por palabra tambien te ayudara a ver cuanto puede o no puede analizar y entender Claude."""

exercise_5_1_hint = """La funcion de calificacion para este ejercicio busca una respuesta que incluya la palabra "Warrior".
Escribe mas palabras en la voz de Claude para dirigir a Claude a actuar como quieres. Por ejemplo, en vez de "Stephen Curry is the best because," podrias escribir "Stephen Curry is the best and here are three reasons why. 1:" """

exercise_5_2_hint = """La funcion de calificacion busca una respuesta de mas de 5 lineas que incluya las palabras "cat" y "<haiku>".
Empieza simple. Actualmente, el prompt pide a Claude un haiku. Puedes cambiarlo y pedir dos (o incluso mas). Luego, si encuentras problemas de formato, cambia tu prompt para arreglarlos despues de que ya hayas logrado que Claude escriba mas de un haiku."""

exercise_5_3_hint = """La funcion de calificacion en este ejercicio busca una respuesta que contenga las palabras "tail", "cat" y "<haiku>".
Es util dividir este ejercicio en varios pasos.
1. Modifica la plantilla de prompt inicial para que Claude escriba dos poemas.
2. Dale a Claude indicadores sobre de que trataran los poemas, pero en vez de escribir los temas directamente (ej: dog, cat, etc.), reemplaza esos temas con las palabras clave "{ANIMAL1}" y "{ANIMAL2}".
3. Ejecuta el prompt y asegurate de que el prompt completo con sustituciones de variables tenga todas las palabras correctamente sustituidas. Si no, verifica que tus tags {entre llaves} esten escritos y formateados correctamente con llaves simples."""

exercise_6_1_hint = """La funcion de calificacion en este ejercicio busca la letra de categorizacion correcta + el parentesis de cierre y la primera letra del nombre de la categoria, como "C) B" o "B) B" etc.
Tomemos este ejercicio paso a paso:
1. Como sabra Claude que categorias quieres usar? Diselo! Incluye las cuatro categorias directamente en el prompt. Asegurate de incluir las letras entre parentesis para facilitar la clasificacion. Usa tags XML para organizar tu prompt y dejar claro a Claude donde empiezan y terminan las categorias.
2. Intenta reducir texto superfluo para que Claude responda inmediatamente con la clasificacion y SOLO la clasificacion. Hay varias formas de hacer esto, desde hablar por Claude (proporcionando desde el inicio de la oracion hasta un solo parentesis abierto para que Claude sepa que quieres la letra entre parentesis como primera parte de la respuesta) hasta decirle a Claude que quieres la clasificacion y solo la clasificacion, sin preambulo. Consulta los Capitulos 2 y 5 si quieres un repaso de estas tecnicas.
3. Claude puede seguir categorizando incorrectamente o no incluyendo los nombres de las categorias cuando responde. Arregla esto diciendole a Claude que incluya el nombre completo de la categoria en su respuesta.
4. Asegurate de que todavia tengas {email} en alguna parte de tu plantilla de prompt para que podamos sustituir correctamente los emails para que Claude los evalue."""

exercise_6_1_solution = """
USER TURN
Please classify this email into the following categories: {email}

Do not include any extra words except the category.

<categories>
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)
</categories>

ASSISTANT TURN
(
"""

exercise_6_2_hint = """La funcion de calificacion en este ejercicio busca solo la letra correcta envuelta en tags <answer>, como "<answer>B</answer>". Las letras de categorizacion correctas son las mismas que en el ejercicio anterior.
A veces la forma mas simple de hacer esto es darle a Claude un ejemplo de como quieres que se vea su output. Solo no olvides envolver tu ejemplo en tags <example></example>! Y no olvides que si pre-llenas la respuesta de Claude con algo, Claude no lo mostrara como parte de su respuesta."""

exercise_7_1_hint = """Vas a tener que escribir algunos emails de ejemplo y clasificarlos para Claude (con el formato exacto que quieres). Hay multiples formas de hacer esto. Aqui hay algunas pautas:
1. Intenta tener al menos dos emails de ejemplo. Claude no necesita un ejemplo para todas las categorias, y los ejemplos no tienen que ser largos. Es mas util tener ejemplos para las categorias que consideres mas complicadas (sobre las cuales se te pidio pensar al final del Ejercicio 1 del Capitulo 6). Los tags XML te ayudaran a separar tus ejemplos del resto de tu prompt, aunque no es obligatorio.
2. Asegurate de que el formato de respuesta de tu ejemplo sea exactamente el formato que quieres que Claude use, para que Claude pueda emular el formato tambien. Este formato deberia hacer que la respuesta de Claude termine con la letra de la categoria. Donde sea que pongas el placeholder {email}, asegurate de que este formateado exactamente como tus emails de ejemplo.
3. Asegurate de que todavia tengas las categorias listadas dentro del prompt, de lo contrario Claude no sabra a que categorias hacer referencia, y tambien {email} como placeholder para sustitucion."""

exercise_7_1_solution = """
USER TURN
Please classify emails into the following categories, and do not include explanations:
<categories>
(A) Pre-sale question
(B) Broken or defective item
(C) Billing question
(D) Other (please explain)
</categories>

Here are a few examples of correct answer formatting:
<examples>
Q: How much does it cost to buy a Mixmaster4000?
A: The correct category is: A

Q: My Mixmaster won't turn on.
A: The correct category is: B

Q: Please remove me from your mailing list.
A: The correct category is: D
</examples>

Here is the email for you to categorize: {email}

ASSISTANT TURN
The correct category is:
"""
exercise_8_1_hint = """La funcion de calificacion en este ejercicio busca una respuesta que contenga la frase "I do not", "I don't" o "Unfortunately".
Que deberia hacer Claude si no sabe la respuesta?"""

exercise_8_2_hint = """La funcion de calificacion en este ejercicio busca una respuesta que contenga la frase "49-fold".
Haz que Claude muestre su trabajo y proceso de pensamiento primero extrayendo citas relevantes y viendo si las citas proporcionan evidencia suficiente. Consulta la Leccion del Capitulo 8 si quieres un repaso."""

exercise_9_1_solution = """
You are a master tax acountant. Your task is to answer user questions using any provided reference documentation.

Here is the material you should use to answer the user's question:
<docs>
{TAX_CODE}
</docs>

Here is an example of how to respond:
<example>
<question>
What defines a "qualified" employee?
</question>
<answer>
<quotes>For purposes of this subsection—
(A)In general
The term "qualified employee" means any individual who—
(i)is not an excluded employee, and
(ii)agrees in the election made under this subsection to meet such requirements as are determined by the Secretary to be necessary to ensure that the withholding requirements of the corporation under chapter 24 with respect to the qualified stock are met.</quotes>

<answer>According to the provided documentation, a "qualified employee" is defined as an individual who:

1. Is not an "excluded employee" as defined in the documentation.
2. Agrees to meet the requirements determined by the Secretary to ensure the corporation's withholding requirements under Chapter 24 are met with respect to the qualified stock.</answer>
</example>

First, gather quotes in <quotes></quotes> tags that are relevant to answering the user's question. If there are no quotes, write "no relevant quotes found".

Then insert two paragraph breaks before answering the user question within <answer></answer> tags. Only answer the user's question if you are confident that the quotes in <quotes></quotes> tags support your answer. If not, tell the user that you unfortunately do not have enough information to answer the user's question.

Here is the user question: {QUESTION}
"""

exercise_9_2_solution = """
You are Codebot, a helpful AI assistant who finds issues with code and suggests possible improvements.

Act as a Socratic tutor who helps the user learn.

You will be given some code from a user. Please do the following:
1. Identify any issues in the code. Put each issue inside separate <issues> tags.
2. Invite the user to write a revised version of the code to fix the issue.

Here's an example:

<example>
<code>
def calculate_circle_area(radius):
    return (3.14 * radius) ** 2
</code>
<issues>
<issue>
3.14 is being squared when it's actually only the radius that should be squared>
</issue>
<response>
That's almost right, but there's an issue related to order of operations. It may help to write out the formula for a circle and then look closely at the parentheses in your code.
</response>
</example>

Here is the code you are to analyze:

<code>
{CODE}
</code>

Find the relevant issues and write the Socratic tutor-style response. Do not give the user too much help! Instead, just give them guidance so they can find the correct solution themselves.

Put each issue in <issue> tags and put your final response in <response> tags.
"""

exercise_10_2_1_solution = """tools_sql = [
    {
        "name": "get_user",
        "description": "Retrieves a user from the database by their user ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "The ID of the user to retrieve"}
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "get_product",
        "description": "Retrieves a product from the database by its product ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "The ID of the product to retrieve"}
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "add_user",
        "description": "Adds a new user to the database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the user"},
                "email": {"type": "string", "description": "The email address of the user"}
            },
            "required": ["name"]
        }
    },
    {
        "name": "add_product",
        "description": "Adds a new product to the database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the product"},
                "price": {"type": "number", "description": "The price of the product"}
            },
            "required": ["name"]
        }
    }
]
"""

# Pistas para los nuevos capitulos

exercise_10_1_hint = """Este ejercicio busca que compares la respuesta de Claude con y sin pensamiento extendido.
Intenta un problema matematico o logico complejo. Primero usa get_completion() normal, y luego get_completion_with_thinking()."""

exercise_10_2_hint = """Este ejercicio busca que encuentres el budget_tokens minimo que produce una respuesta correcta.
Empieza con un valor bajo (ej: 1024) y ve subiendo gradualmente hasta que Claude responda correctamente."""

exercise_10_3_hint = """Combina un system prompt detallado con pensamiento extendido.
Piensa en como el system prompt puede guiar el analisis mientras el pensamiento extendido permite un razonamiento mas profundo."""

exercise_11_1_hint = """La funcion de calificacion busca una respuesta que contenga tags XML de estructura (<categoria>, <respuesta>, o similares).
Usa multiples secciones en tu system prompt: <rol>, <instrucciones>, <formato>, <restricciones>."""

exercise_11_2_hint = """La funcion de calificacion busca que Claude rechace temas inapropiados y se mantenga en el tema educativo.
Incluye restricciones claras en tu system prompt sobre que temas son permitidos y cuales no."""

exercise_11_3_hint = """La funcion de calificacion busca una respuesta en formato JSON valido.
En tu system prompt, incluye un esquema JSON de ejemplo y una instruccion explicita de que SIEMPRE responda en JSON, sin importar la pregunta."""
