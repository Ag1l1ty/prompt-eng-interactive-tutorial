import json
import streamlit as st
from utils.components import render_sidebar, render_lesson
from utils.api import run_tool_loop

render_sidebar()
st.title("Capitulo 9: Herramientas y Agentes (Tool Use)")

render_lesson("""
### Que es Tool Use (Function Calling)?

Hasta ahora, Claude ha respondido preguntas usando solo su conocimiento interno.
Pero hay situaciones donde Claude necesita **hacer cosas en el mundo real**:
consultar bases de datos, hacer calculos precisos, llamar APIs externas, etc.

**Tool Use** (tambien llamado *Function Calling*) permite que Claude
**llame funciones que TU defines**. Claude no ejecuta codigo directamente --
en vez de eso, te dice *que* funcion quiere llamar y con *que* parametros,
y tu ejecutas la funcion en tu lado.

---

### Flujo de 4 pasos

El flujo de Tool Use funciona asi:

1. **Tu defines las herramientas** -- Le dices a Claude que herramientas tiene disponibles,
   usando un formato JSON Schema con nombre, descripcion y parametros.
2. **Claude decide llamar una herramienta** -- Si la pregunta del usuario requiere
   una herramienta, Claude genera un bloque `tool_use` con el nombre y los argumentos.
3. **Tu ejecutas la funcion** -- Tu codigo recibe la solicitud de Claude, ejecuta la
   funcion real y devuelve el resultado.
4. **Claude interpreta el resultado** -- Claude recibe el resultado de la funcion y
   lo usa para formular su respuesta final al usuario.

> **Importante:** Claude decide **CUANDO** usar herramientas. Si la pregunta no requiere
> una herramienta (por ejemplo, "Cual es la capital de Francia?"), Claude responde
> directamente sin llamar ninguna funcion.

---

### Bucle agentico

En escenarios complejos, Claude puede necesitar **varias herramientas en secuencia**.
Por ejemplo: buscar un usuario, luego buscar sus pedidos, luego calcular un total.

El patron es un **bucle agentico**: repetir el ciclo de llamada-ejecucion-respuesta
hasta que Claude deje de pedir herramientas y de su respuesta final.

---

### Como se define una herramienta

Cada herramienta se define con tres elementos:

- **Nombre:** Identificador unico de la funcion (ej: `calculadora`)
- **Descripcion:** Texto que explica a Claude que hace la herramienta y cuando usarla
- **Esquema de parametros:** Definicion en JSON Schema de los parametros que acepta

> **Herramienta: calculadora**
> - Nombre: `calculadora`
> - Descripcion: Realiza operaciones aritmeticas basicas
> - Parametros: `primer_operando` (numero), `segundo_operando` (numero), `operador` (+, -, *, /)

La **descripcion** es crucial: es lo que Claude lee para decidir si debe usar
la herramienta o no. Una buena descripcion = mejores decisiones.

---

### Resumen

| Concepto | Descripcion |
|----------|-------------|
| Tool Use | Claude puede llamar funciones que tu defines |
| Flujo | Definir herramientas, Claude decide, tu ejecutas, Claude interpreta |
| Bucle agentico | Repetir hasta que Claude deje de pedir herramientas |
| JSON Schema | Formato para definir parametros de las herramientas |
| Decision inteligente | Claude solo usa herramientas cuando es necesario |
""")

st.divider()
st.header("Demos Interactivos")

# ── Tool definitions ────────────────────────────────────────────
calculator_tool = {
    "name": "calculadora",
    "description": "Realiza operaciones aritmeticas basicas. Usa esta herramienta cuando necesites sumar, restar, multiplicar o dividir dos numeros.",
    "input_schema": {
        "type": "object",
        "properties": {
            "primer_operando": {"type": "number", "description": "Primer numero"},
            "segundo_operando": {"type": "number", "description": "Segundo numero"},
            "operador": {
                "type": "string",
                "enum": ["+", "-", "*", "/"],
                "description": "Operacion aritmetica a realizar",
            },
        },
        "required": ["primer_operando", "segundo_operando", "operador"],
    },
}


def calculadora_fn(input_data):
    a = input_data["primer_operando"]
    b = input_data["segundo_operando"]
    op = input_data["operador"]
    ops = {
        "+": a + b,
        "-": a - b,
        "*": a * b,
        "/": a / b if b != 0 else "Error: division por cero",
    }
    return {"resultado": ops.get(op, "Operador invalido")}


# ── Demo 1: Calculadora con herramientas ────────────────────────
st.subheader("Demo 1: Calculadora con Herramientas")
st.markdown("""
Escribe una pregunta que requiera un calculo numerico. Claude detectara que necesita
la herramienta `calculadora` y la llamara automaticamente. Puedes ver los detalles
de cada llamada en los expanders.
""")

pregunta = st.text_input(
    "Pregunta que requiere calculo",
    value="Cuanto es 1984135 multiplicado por 9343116?",
    key="tool_q",
)
if st.button("Ejecutar con herramientas", key="run_tools"):
    with st.spinner("Claude usando herramientas..."):
        resultado, log = run_tool_loop(
            pregunta,
            tools=[calculator_tool],
            available_functions={"calculadora": calculadora_fn},
        )
    for entry in log:
        with st.expander(f"Llamada: {entry['tool']}"):
            st.json(entry["input"])
            st.markdown(f"**Resultado:** {entry['result']}")
    st.markdown("**Respuesta final:**")
    st.code(resultado, language=None)
    st.session_state.completed.add("9.1")

st.divider()

# ── Demo 2: Cuando Claude NO usa herramientas ──────────────────
st.subheader("Demo 2: Cuando Claude NO Usa Herramientas")
st.markdown("""
Claude es inteligente: si la pregunta **no requiere calculo**, responde directamente
sin llamar ninguna herramienta. Prueba con una pregunta de conocimiento general.
""")

pregunta_general = st.text_input(
    "Pregunta general (sin calculo)",
    value="Cual es la capital de Francia?",
    key="tool_q2",
)
if st.button("Ejecutar", key="run_no_tools"):
    with st.spinner("..."):
        resultado, log = run_tool_loop(
            pregunta_general,
            tools=[calculator_tool],
            available_functions={"calculadora": calculadora_fn},
        )
    if not log:
        st.info("Claude no uso herramientas (respuesta directa)")
    else:
        for entry in log:
            with st.expander(f"Llamada: {entry['tool']}"):
                st.json(entry["input"])
                st.markdown(f"**Resultado:** {entry['result']}")
    st.code(resultado, language=None)

st.divider()

# ── Demo 3: Mini Base de Datos ──────────────────────────────────
st.subheader("Demo 3: Mini Base de Datos")
st.markdown("""
Este demo simula un sistema con **4 herramientas** conectadas a una pequena
base de datos en memoria. Puedes hacer consultas en lenguaje natural como:

- *"Dime el nombre del Usuario 2"*
- *"Agrega un producto llamado Teclado por $49.99"*
- *"Cuantos usuarios hay?"*

Claude decidira que herramienta(s) usar para responder tu consulta.
""")

# Initialize simple in-memory DB in session state
if "demo_db" not in st.session_state:
    st.session_state.demo_db = {
        "usuarios": {
            1: {"nombre": "Ana", "email": "ana@ejemplo.com"},
            2: {"nombre": "Carlos", "email": "carlos@ejemplo.com"},
        },
        "productos": {
            1: {"nombre": "Laptop", "precio": 999.99},
            2: {"nombre": "Mouse", "precio": 29.99},
        },
    }

# Show current DB state
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Usuarios actuales:**")
    for uid, u in st.session_state.demo_db["usuarios"].items():
        st.markdown(f"- ID {uid}: {u['nombre']} ({u['email']})")
with col2:
    st.markdown("**Productos actuales:**")
    for pid, p in st.session_state.demo_db["productos"].items():
        st.markdown(f"- ID {pid}: {p['nombre']} (${p['precio']})")

# Define 4 tools
db_tools = [
    {
        "name": "obtener_usuario",
        "description": "Obtiene la informacion de un usuario por su ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {"type": "integer", "description": "ID del usuario"},
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "obtener_producto",
        "description": "Obtiene la informacion de un producto por su ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "integer", "description": "ID del producto"},
            },
            "required": ["product_id"],
        },
    },
    {
        "name": "agregar_usuario",
        "description": "Agrega un nuevo usuario a la base de datos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {"type": "string", "description": "Nombre del usuario"},
                "email": {"type": "string", "description": "Email del usuario"},
            },
            "required": ["nombre", "email"],
        },
    },
    {
        "name": "agregar_producto",
        "description": "Agrega un nuevo producto a la base de datos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "nombre": {"type": "string", "description": "Nombre del producto"},
                "precio": {"type": "number", "description": "Precio del producto"},
            },
            "required": ["nombre", "precio"],
        },
    },
]


def obtener_usuario_fn(input_data):
    uid = input_data["user_id"]
    user = st.session_state.demo_db["usuarios"].get(uid)
    if user:
        return {"encontrado": True, "id": uid, **user}
    return {"encontrado": False, "mensaje": f"Usuario con ID {uid} no encontrado"}


def obtener_producto_fn(input_data):
    pid = input_data["product_id"]
    prod = st.session_state.demo_db["productos"].get(pid)
    if prod:
        return {"encontrado": True, "id": pid, **prod}
    return {"encontrado": False, "mensaje": f"Producto con ID {pid} no encontrado"}


def agregar_usuario_fn(input_data):
    db = st.session_state.demo_db["usuarios"]
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = {"nombre": input_data["nombre"], "email": input_data["email"]}
    return {"exito": True, "id": new_id, "mensaje": f"Usuario '{input_data['nombre']}' agregado con ID {new_id}"}


def agregar_producto_fn(input_data):
    db = st.session_state.demo_db["productos"]
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = {"nombre": input_data["nombre"], "precio": input_data["precio"]}
    return {"exito": True, "id": new_id, "mensaje": f"Producto '{input_data['nombre']}' agregado con ID {new_id}"}


db_functions = {
    "obtener_usuario": obtener_usuario_fn,
    "obtener_producto": obtener_producto_fn,
    "agregar_usuario": agregar_usuario_fn,
    "agregar_producto": agregar_producto_fn,
}

consulta_db = st.text_input(
    "Consulta en lenguaje natural",
    value="Dime el nombre del Usuario 2",
    key="db_query",
)
if st.button("Consultar base de datos", key="run_db"):
    with st.spinner("Claude consultando la base de datos..."):
        resultado_db, log_db = run_tool_loop(
            consulta_db,
            tools=db_tools,
            available_functions=db_functions,
            system_prompt="Eres un asistente que ayuda a consultar y modificar una base de datos de usuarios y productos. Responde siempre en espanol.",
        )
    for entry in log_db:
        with st.expander(f"Llamada: {entry['tool']}"):
            st.json(entry["input"])
            st.markdown(f"**Resultado:** {json.dumps(entry['result'], ensure_ascii=False)}")
    st.markdown("**Respuesta final:**")
    st.code(resultado_db, language=None)
    st.session_state.completed.add("9.1")

if st.button("Reiniciar base de datos", key="reset_db"):
    st.session_state.demo_db = {
        "usuarios": {
            1: {"nombre": "Ana", "email": "ana@ejemplo.com"},
            2: {"nombre": "Carlos", "email": "carlos@ejemplo.com"},
        },
        "productos": {
            1: {"nombre": "Laptop", "precio": 999.99},
            2: {"nombre": "Mouse", "precio": 29.99},
        },
    }
    st.rerun()
