import anthropic
import streamlit as st

MODEL_NAME = "claude-opus-4-6"


def get_client():
    """Returns an Anthropic client using the API key from session state."""
    api_key = st.session_state.get("api_key", "")
    if not api_key:
        st.error("Por favor ingresa tu clave API de Anthropic en la barra lateral.")
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


def get_completion(prompt, system_prompt="", prefill=""):
    """Standard Claude API call."""
    client = get_client()
    messages = [{"role": "user", "content": prompt}]
    if prefill:
        messages.append({"role": "assistant", "content": prefill})
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=2000,
            temperature=0.0,
            system=system_prompt,
            messages=messages,
        )
        return response.content[0].text
    except anthropic.AuthenticationError:
        st.error("Clave API invalida. Verifica tu clave en la barra lateral.")
        st.stop()
    except anthropic.RateLimitError:
        st.error("Limite de tasa excedido. Espera un momento e intenta de nuevo.")
        st.stop()
    except anthropic.APIError as e:
        st.error(f"Error de API: {e}")
        st.stop()


def get_completion_with_thinking(prompt, system_prompt="", budget_tokens=2000):
    """Claude API call with extended thinking (Chapter 10)."""
    client = get_client()
    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=16000,
            thinking={"type": "enabled", "budget_tokens": budget_tokens},
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}],
        )
        thinking_text = ""
        response_text = ""
        for block in response.content:
            if block.type == "thinking":
                thinking_text = block.thinking
            elif block.type == "text":
                response_text = block.text
        return thinking_text, response_text
    except anthropic.AuthenticationError:
        st.error("Clave API invalida.")
        st.stop()
    except anthropic.RateLimitError:
        st.error("Limite de tasa excedido.")
        st.stop()
    except anthropic.APIError as e:
        st.error(f"Error de API: {e}")
        st.stop()


def run_tool_loop(user_message, tools, available_functions, system_prompt=""):
    """Agentic tool use loop (Chapter 12.2)."""
    import json

    client = get_client()
    messages = [{"role": "user", "content": user_message}]
    tool_log = []

    for _ in range(5):  # max iterations
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            system=system_prompt,
            tools=tools,
            messages=messages,
        )

        if response.stop_reason != "tool_use":
            final_text = next(
                (b.text for b in response.content if hasattr(b, "text")), ""
            )
            return final_text, tool_log

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                func = available_functions.get(block.name)
                result = func(block.input) if func else f"Unknown tool: {block.name}"
                tool_log.append(
                    {"tool": block.name, "input": block.input, "result": result}
                )
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result) if result else "null",
                    }
                )
        messages.append({"role": "user", "content": tool_results})

    return "Max iterations reached", tool_log
