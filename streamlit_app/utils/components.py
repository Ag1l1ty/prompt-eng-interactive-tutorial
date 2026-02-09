import streamlit as st
from utils.api import get_completion


def init_session():
    """Initialize session state variables."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "completed" not in st.session_state:
        st.session_state.completed = set()


def render_sidebar():
    """Render sidebar with API key input and progress."""
    init_session()
    with st.sidebar:
        st.title("Prompt Engineering")
        st.markdown("### Configuracion")
        api_key = st.text_input(
            "Clave API de Anthropic",
            type="password",
            value=st.session_state.get("api_key", ""),
            help="Tu clave se almacena solo en esta sesion.",
        )
        if api_key:
            st.session_state.api_key = api_key
            st.success("API configurada")
        else:
            st.warning("Ingresa tu API key")

        st.divider()
        total = 24
        done = len(st.session_state.completed)
        st.markdown(f"### Progreso: {done}/{total}")
        st.progress(done / total if total > 0 else 0)

        st.divider()
        st.caption("[GitHub](https://github.com/Ag1l1ty/prompt-eng-interactive-tutorial)")


def render_lesson(content):
    """Render lesson markdown content."""
    st.markdown(content)


def render_exercise(
    exercise_id,
    title,
    instruction,
    hint,
    grade_fn,
    fields=None,
    prefill="",
    system_prompt_default="",
):
    """
    Render a complete exercise with input, run button, response, and grading.

    fields: list of dicts with keys: name, label, rows (default: [{"name": "PROMPT", "label": "Prompt", "rows": 4}])
    grade_fn: callable that takes response text and returns bool
    """
    if fields is None:
        fields = [{"name": "PROMPT", "label": "Prompt", "rows": 4}]

    st.subheader(f"Ejercicio {exercise_id} - {title}")
    st.markdown(instruction)

    inputs = {}
    for field in fields:
        default_val = ""
        if field["name"] == "SYSTEM_PROMPT":
            default_val = system_prompt_default
        inputs[field["name"]] = st.text_area(
            field["label"],
            value=default_val,
            height=field.get("rows", 4) * 28,
            key=f"input_{exercise_id}_{field['name']}",
        )

    col1, col2 = st.columns([1, 4])
    run = col1.button("Ejecutar", key=f"run_{exercise_id}", use_container_width=True)
    show_hint = col2.button(
        "Ver pista", key=f"hint_{exercise_id}", use_container_width=True
    )

    if show_hint:
        st.info(hint)

    if run:
        prompt = inputs.get("PROMPT", "")
        system = inputs.get("SYSTEM_PROMPT", "")
        pf = inputs.get("PREFILL", prefill)

        if not prompt and not system:
            st.warning("Escribe algo en los campos antes de ejecutar.")
            return

        with st.spinner("Claude esta pensando..."):
            response = get_completion(prompt, system_prompt=system, prefill=pf)

        st.markdown("**Respuesta de Claude:**")
        st.code(response, language=None)

        passed = grade_fn(response)
        if passed:
            st.success("Este ejercicio se ha resuelto correctamente.")
            st.session_state.completed.add(exercise_id)
        else:
            st.error("Incorrecto. Intenta de nuevo.")

    st.divider()


def render_multi_test_exercise(
    exercise_id,
    title,
    instruction,
    hint,
    test_cases,
    grade_fn,
    prompt_template,
    prefill="",
):
    """
    Render exercise that loops over multiple test cases (Ch 6, 7).

    test_cases: list of dicts with at least a 'content' key
    grade_fn: callable(response, test_case) -> bool
    prompt_template: string with {email} or similar placeholder
    """
    st.subheader(f"Ejercicio {exercise_id} - {title}")
    st.markdown(instruction)

    prompt_input = st.text_area(
        "Plantilla de prompt (usa {email} como marcador)",
        value=prompt_template,
        height=120,
        key=f"input_{exercise_id}_PROMPT",
    )
    pf = st.text_input(
        "Prefill (opcional)",
        value=prefill,
        key=f"input_{exercise_id}_PREFILL",
    )

    col1, col2 = st.columns([1, 4])
    run = col1.button("Ejecutar todos", key=f"run_{exercise_id}", use_container_width=True)
    show_hint = col2.button("Ver pista", key=f"hint_{exercise_id}", use_container_width=True)

    if show_hint:
        st.info(hint)

    if run:
        all_passed = True
        for i, tc in enumerate(test_cases):
            formatted = prompt_input.format(email=tc["content"])
            with st.spinner(f"Procesando caso {i + 1}/{len(test_cases)}..."):
                response = get_completion(formatted, prefill=pf)
            passed = grade_fn(response, tc)
            if not passed:
                all_passed = False
            icon = "pass" if passed else "fail"
            with st.expander(f"Caso {i + 1}: {'Correcto' if passed else 'Incorrecto'}"):
                st.code(response, language=None)

        if all_passed:
            st.success("Todos los casos resueltos correctamente.")
            st.session_state.completed.add(exercise_id)
        else:
            st.error("Algunos casos fallaron. Revisa tu prompt.")

    st.divider()


def render_code_demo(prompt, system_prompt="", label="Ejemplo"):
    """Render an executable demo from the lesson."""
    with st.expander(f"Demo: {label}", expanded=False):
        if st.button(f"Ejecutar demo", key=f"demo_{label}_{hash(prompt)}"):
            with st.spinner("Claude esta pensando..."):
                response = get_completion(prompt, system_prompt=system_prompt)
            st.code(response, language=None)
