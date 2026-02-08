import json
import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import get_completion, run_tool_loop

render_sidebar()

st.title("Apendice 12.2: Uso de Herramientas (Tool Use)")

render_lesson("""
## Que es el uso de herramientas?

El uso de herramientas (*tool use*), tambien conocido como llamada a funciones (*function calling*),
permite a Claude **interactuar con sistemas externos** ejecutando funciones que tu defines.

Claude no ejecuta las funciones directamente. El flujo funciona asi:

1. **Tu defines las herramientas** como un parametro `tools` en la llamada a la API, usando JSON Schema
2. **Claude decide** si necesita una herramienta y genera una solicitud estructurada con el nombre y los argumentos
3. **Tu codigo ejecuta** la funcion real y devuelve el resultado a Claude
4. **Claude usa el resultado** para formular su respuesta final

### Por que es util?

La llamada a funciones expande las capacidades de Claude para tareas que requieren:

- **Calculadora** para operaciones aritmeticas precisas
- **Consultas a bases de datos** SQL y recuperacion de datos
- **APIs externas** como clima, busqueda, etc.
- **Manipulacion de archivos** para leer y escribir datos

### Paso 1: Definir las herramientas

Las herramientas se definen como una lista de diccionarios con:
- `name`: Nombre de la herramienta (identificador unico)
- `description`: Descripcion clara de que hace la herramienta
- `input_schema`: Esquema JSON que define los parametros de entrada

```python
calculator_tool = {
    "name": "calculator",
    "description": "A calculator that performs basic arithmetic operations.",
    "input_schema": {
        "type": "object",
        "properties": {
            "first_operand": {"type": "integer", "description": "First operand"},
            "second_operand": {"type": "integer", "description": "Second operand"},
            "operator": {
                "type": "string",
                "enum": ["+", "-", "*", "/"],
                "description": "The arithmetic operation to perform"
            }
        },
        "required": ["first_operand", "second_operand", "operator"]
    }
}
```

### Paso 2: Enviar el mensaje con herramientas

Se envia el mensaje junto con la lista de herramientas. Claude analiza la pregunta y decide si
necesita usar alguna herramienta. Si decide usarla, responde con `stop_reason: "tool_use"`
y un bloque `ToolUseBlock` con el nombre y los argumentos.

### Paso 3: Ejecutar y devolver el resultado

Extraemos la solicitud, ejecutamos la funcion real, y devolvemos el resultado a Claude
como un mensaje `tool_result`. Claude entonces usa ese resultado para formular su respuesta.

### El bucle agentico

En la practica, todo se automatiza en un **bucle agentico** (*agentic loop*):
1. Enviar el mensaje a Claude
2. Si Claude solicita una herramienta, ejecutarla y devolver el resultado
3. Repetir hasta que Claude responda sin solicitar herramientas

```python
result, tool_log = run_tool_loop(
    "What is 1984135 multiplied by 9343116?",
    tools=[calculator_tool],
    available_functions={"calculator": calculator_fn}
)
```

Claude tambien sabe **cuando NO usar herramientas**. Si le haces una pregunta que no
requiere ninguna herramienta, simplemente responde con texto normal.
""")

st.divider()
st.header("Demos Interactivos")

# ── Tool definitions ─────────────────────────────────────────────────────────

calculator_tool = {
    "name": "calculator",
    "description": "A calculator that performs basic arithmetic operations. Supports addition, subtraction, multiplication, and division.",
    "input_schema": {
        "type": "object",
        "properties": {
            "first_operand": {
                "type": "number",
                "description": "First operand (before the operator)",
            },
            "second_operand": {
                "type": "number",
                "description": "Second operand (after the operator)",
            },
            "operator": {
                "type": "string",
                "enum": ["+", "-", "*", "/"],
                "description": "The arithmetic operation to perform",
            },
        },
        "required": ["first_operand", "second_operand", "operator"],
    },
}


def calculator_fn(input_data):
    """Execute a basic arithmetic operation."""
    op = input_data["operator"]
    a = input_data["first_operand"]
    b = input_data["second_operand"]
    if op == "+":
        return {"result": a + b}
    elif op == "-":
        return {"result": a - b}
    elif op == "*":
        return {"result": a * b}
    elif op == "/":
        if b == 0:
            return {"error": "Division by zero"}
        return {"result": a / b}
    return {"error": f"Unknown operator: {op}"}


# ── Demo 1: Definicion de herramienta ────────────────────────────────────────

st.subheader("Demo 1: Definicion de la herramienta")
st.markdown("""
Asi se define la herramienta de calculadora que Claude puede usar.
Examina el JSON Schema que describe los parametros:
""")

with st.expander("Ver definicion de la herramienta calculadora", expanded=True):
    st.json(calculator_tool)

st.divider()

# ── Demo 2: Calculadora con Tool Use ────────────────────────────────────────

st.subheader("Demo 2: Calculadora con Tool Use")
st.markdown("""
Escribe una pregunta que requiera calculos matematicos. Claude detectara que necesita
la calculadora, la llamara con los argumentos correctos, y usara el resultado para responder.
""")

user_q = st.text_input(
    "Pregunta que requiere calculo",
    value="What is 1,984,135 multiplied by 9,343,116?",
    key="tool_q",
)

if st.button("Ejecutar con herramientas", key="run_tools"):
    with st.spinner("Claude usando herramientas..."):
        result, log = run_tool_loop(
            user_q,
            tools=[calculator_tool],
            available_functions={"calculator": calculator_fn},
        )

    if log:
        st.markdown("**Llamadas a herramientas:**")
        for i, entry in enumerate(log):
            with st.expander(f"Llamada {i + 1}: {entry['tool']}", expanded=True):
                st.markdown("**Argumentos enviados:**")
                st.json(entry["input"])
                st.markdown("**Resultado de la funcion:**")
                st.json(entry["result"])
    else:
        st.info("Claude no necesito usar herramientas para esta pregunta.")

    st.markdown("**Respuesta final de Claude:**")
    st.code(result, language=None)

st.divider()

# ── Demo 3: Pregunta sin herramientas ────────────────────────────────────────

st.subheader("Demo 3: Cuando Claude NO usa herramientas")
st.markdown("""
Claude es lo suficientemente inteligente para saber cuando **no** necesita una herramienta.
Prueba con una pregunta de conocimiento general que no requiere calculos.
""")

no_tool_q = st.text_input(
    "Pregunta de conocimiento general",
    value="What is the capital of France?",
    key="no_tool_q",
)

if st.button("Ejecutar (con herramientas disponibles)", key="run_no_tools"):
    with st.spinner("Claude decidiendo..."):
        result, log = run_tool_loop(
            no_tool_q,
            tools=[calculator_tool],
            available_functions={"calculator": calculator_fn},
        )

    if log:
        st.warning("Claude decidio usar herramientas (inesperado para esta pregunta).")
        for entry in log:
            with st.expander(f"Llamada: {entry['tool']}"):
                st.json(entry["input"])
                st.json(entry["result"])
    else:
        st.success("Claude respondio sin usar herramientas, como esperabamos.")

    st.markdown("**Respuesta:**")
    st.code(result, language=None)

st.divider()

# ── Demo 4: Mini base de datos con herramientas ──────────────────────────────

st.subheader("Demo 4: Mini base de datos con herramientas")
st.markdown("""
Este demo simula el ejercicio del notebook: una "base de datos" en memoria con usuarios
y productos. Claude puede consultar y agregar registros usando herramientas.
""")

# Initialize mini DB in session state
if "mini_db" not in st.session_state:
    st.session_state.mini_db = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
        ],
        "products": [
            {"id": 1, "name": "Widget", "price": 9.99},
            {"id": 2, "name": "Gadget", "price": 14.99},
            {"id": 3, "name": "Doohickey", "price": 19.99},
        ],
    }

# DB tool definitions
db_tools = [
    {
        "name": "get_user",
        "description": "Get a user from the database by their ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "The user's ID"},
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "get_product",
        "description": "Get a product from the database by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "The product's ID"},
            },
            "required": ["product_id"],
        },
    },
    {
        "name": "add_user",
        "description": "Add a new user to the database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The user's name"},
                "email": {"type": "string", "description": "The user's email"},
            },
            "required": ["name"],
        },
    },
    {
        "name": "add_product",
        "description": "Add a new product to the database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The product's name"},
                "price": {"type": "number", "description": "The product's price"},
            },
            "required": ["name"],
        },
    },
]


def get_user_fn(input_data):
    for user in st.session_state.mini_db["users"]:
        if user["id"] == input_data["user_id"]:
            return user
    return {"error": f"User with id {input_data['user_id']} not found"}


def get_product_fn(input_data):
    for product in st.session_state.mini_db["products"]:
        if product["id"] == input_data["product_id"]:
            return product
    return {"error": f"Product with id {input_data['product_id']} not found"}


def add_user_fn(input_data):
    user_id = len(st.session_state.mini_db["users"]) + 1
    email = input_data.get("email", f"{input_data['name'].lower()}@example.com")
    user = {"id": user_id, "name": input_data["name"], "email": email}
    st.session_state.mini_db["users"].append(user)
    return user


def add_product_fn(input_data):
    product_id = len(st.session_state.mini_db["products"]) + 1
    price = input_data.get("price", 0.0)
    product = {"id": product_id, "name": input_data["name"], "price": price}
    st.session_state.mini_db["products"].append(product)
    return product


db_functions = {
    "get_user": get_user_fn,
    "get_product": get_product_fn,
    "add_user": add_user_fn,
    "add_product": add_product_fn,
}

# Show current DB state
with st.expander("Ver estado actual de la base de datos"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Usuarios:**")
        st.json(st.session_state.mini_db["users"])
    with col2:
        st.markdown("**Productos:**")
        st.json(st.session_state.mini_db["products"])

db_query = st.text_input(
    "Consulta a la base de datos",
    value="Tell me the name of User 2",
    key="db_q",
)

# Quick-select buttons for example queries
st.markdown("**Prueba estos ejemplos:**")
ex_col1, ex_col2, ex_col3, ex_col4 = st.columns(4)


if st.button("Ejecutar consulta", key="run_db"):
    with st.spinner("Claude consultando la base de datos..."):
        result, log = run_tool_loop(
            db_query,
            tools=db_tools,
            available_functions=db_functions,
        )

    if log:
        st.markdown("**Herramientas utilizadas:**")
        for i, entry in enumerate(log):
            with st.expander(f"Llamada {i + 1}: {entry['tool']}", expanded=True):
                st.markdown("**Argumentos:**")
                st.json(entry["input"])
                st.markdown("**Resultado:**")
                if isinstance(entry["result"], (dict, list)):
                    st.json(entry["result"])
                else:
                    st.code(str(entry["result"]), language=None)

    st.markdown("**Respuesta de Claude:**")
    st.code(result, language=None)
    st.session_state.completed.add("12.2")

if st.button("Reiniciar base de datos", key="reset_db"):
    st.session_state.mini_db = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
        ],
        "products": [
            {"id": 1, "name": "Widget", "price": 9.99},
            {"id": 2, "name": "Gadget", "price": 14.99},
            {"id": 3, "name": "Doohickey", "price": 19.99},
        ],
    }
    st.rerun()
