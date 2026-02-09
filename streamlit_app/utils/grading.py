import re
import json


# ============================================================
# Cap 1 - Ser Claro y Directo
# ============================================================

def grade_1_1(text):
    """Respuesta exacta: 'Michael Jordan' y nada mas."""
    return text.strip() == "Michael Jordan"


def grade_1_2(text):
    """Correccion matematica: debe decir que es incorrecto."""
    return bool(
        re.search(r"incorrecto|no es correcto|incorrect|not correct|error", text.lower())
    )


def grade_1_3(text):
    """Respuesta detallada: >= 800 palabras."""
    return len(text.strip().split()) >= 800


# ============================================================
# Cap 2 - Estructurar con XML Tags
# ============================================================

def grade_2_1(text):
    """Haiku sobre cerdos: debe contener 'cerdos'/'pigs' y 'haiku'."""
    return bool(
        re.search(r"cerdo|pigs|pig", text.lower())
        and re.search(r"haiku", text.lower())
    )


def grade_2_2(text):
    """Pregunta sobre perros: respuesta debe incluir color marron."""
    return bool(re.search(r"brown|marrón|marron|café|cafe", text.lower()))


def grade_2_3(text):
    """Mismo que 2.2 - minimo contexto necesario."""
    return bool(re.search(r"brown|marrón|marron|café|cafe", text.lower()))


# ============================================================
# Cap 3 - Formato de Output y Prefill
# ============================================================

def grade_3_1(text):
    """Steph Curry GOAT: debe mencionar Warriors/Golden State."""
    return bool(re.search(r"Warrior|Warriors|Golden State", text))


def grade_3_2(text):
    """Dos haikus de gatos: 'gato'/'cat', tag <haiku>, >5 lineas."""
    return bool(
        re.search(r"cat|gato", text.lower())
        and re.search(r"<haiku>", text)
        and (text.count("\n") + 1) > 5
    )


def grade_3_3(text):
    """Dos haikus, dos animales: 'cola'/'tail', 'gato'/'cat', tag <haiku>."""
    return bool(
        re.search(r"tail|cola", text.lower())
        and re.search(r"cat|gato", text.lower())
        and re.search(r"<haiku>", text)
    )


# ============================================================
# Cap 4 - Ejemplos y Few-Shot (clasificacion de emails)
# ============================================================

EMAILS_4 = [
    "Hola -- Mi Mixmaster4000 esta haciendo un ruido extrano cuando lo uso. Tambien huele un poco a humo y plastico, como electronica quemandose. Necesito un reemplazo.",
    "Puedo usar mi Mixmaster 4000 para mezclar pintura, o solo sirve para mezclar comida?",
    "LLEVO 4 MESES ESPERANDO A QUE DEJEN DE COBRARME DESPUES DE CANCELAR!! QUE ESTA PASANDO???",
    "Como llegue aqui no soy bueno con la computadora. Ayudaa.",
]

ANSWERS_4 = [["B"], ["A", "D"], ["C"], ["D"]]

REGEX_4_1 = {"A": r"A\)", "B": r"B\)", "C": r"C\)", "D": r"D\)"}
REGEX_4_2 = {
    "A": "<answer>A</answer>",
    "B": "<answer>B</answer>",
    "C": "<answer>C</answer>",
    "D": "<answer>D</answer>",
}


def grade_4_1(response, test_case):
    """Clasificacion directa: letra correcta con parentesis."""
    idx = test_case["index"]
    return any(bool(re.search(REGEX_4_1[ans], response)) for ans in ANSWERS_4[idx])


def grade_4_2(response, test_case):
    """Clasificacion con tags <answer>: letra en tags XML."""
    idx = test_case["index"]
    return any(bool(re.search(REGEX_4_2[ans], response)) for ans in ANSWERS_4[idx])


def grade_4_3(response, test_case):
    """Few-shot: ultimo caracter de respuesta es la letra correcta."""
    idx = test_case["index"]
    if not response:
        return False
    return any(bool(re.search(ans, response[-1])) for ans in ANSWERS_4[idx])


# ============================================================
# Cap 5 - Evitar Alucinaciones
# ============================================================

def grade_5_1(text):
    """Claude debe admitir que no sabe (no alucinar)."""
    contains = bool(
        re.search(r"lamentablemente|unfortunately", text.lower())
        or re.search(r"no tengo|i do not", text.lower())
        or re.search(r"no sé|no se|i don't", text.lower())
        or re.search(r"no puedo confirmar|no dispongo", text.lower())
    )
    does_not_contain = not bool(re.search("2022", text))
    return contains and does_not_contain


def grade_5_2(text):
    """Respuesta basada en documento: debe encontrar '49-fold' o '49 veces'."""
    return bool(re.search(r"49-fold|49 veces|49x", text))


# ============================================================
# Cap 6 - Prompts Complejos (sin calificacion automatica)
# ============================================================
# Ejercicios 6.1 y 6.2 son abiertos - se marcan completos al ejecutar.


# ============================================================
# Cap 7 - Pensamiento Extendido
# ============================================================

def grade_7_1(text):
    """Problema de maquinas: respuesta contiene '5'."""
    return "5" in text


def grade_7_2(text):
    """Problema bat-and-ball: respuesta es $0.05."""
    return bool(re.search(r"0[.,]05|5 cents|five cents|5 centavos|cinco centavos", text.lower()))


def grade_7_3(text):
    """Code review: debe identificar >= 2 de 3 bugs."""
    bugs_found = 0
    if re.search(
        r"empty|zero|division|len.*0|ZeroDivision|vac[ií][oa]|cero|divisi[oó]n",
        text, re.IGNORECASE
    ):
        bugs_found += 1
    if re.search(
        r"negative|max.*0|initial|negativ|m[aá]ximo|inicial",
        text, re.IGNORECASE
    ):
        bugs_found += 1
    if re.search(
        r"modify.*iterat|mutat|remove.*during|concurrent|modificar.*iteran|eliminar.*durante",
        text, re.IGNORECASE
    ):
        bugs_found += 1
    return bugs_found >= 2


# ============================================================
# Cap 8 - System Prompts Avanzados
# ============================================================

def grade_8_1(text):
    """Bot de atencion: tiene categoria + estructura de ticket."""
    has_category = bool(
        re.search(
            r"<categor|categor|shipping|delivery|delayed|env[ií]o|entrega|retras",
            text, re.IGNORECASE,
        )
    )
    has_structure = bool(
        re.search(
            r"ticket|reference|caso|n[uú]mero|referencia|#\d",
            text, re.IGNORECASE,
        )
    )
    return has_category and has_structure


def grade_8_2_math(text):
    """Guardrails: Claude NO debe responder '12' directamente."""
    return not bool(
        re.search(
            r"^12$|^12\.|the answer is 12|la respuesta es 12|= ?12$|son 12|es 12[.\s]",
            text, re.MULTILINE | re.IGNORECASE,
        )
    )


def grade_8_2_off(text):
    """Guardrails: Claude debe redirigir temas no permitidos."""
    return bool(
        re.search(
            r"math|focus|let's|instead|sorry|matem[aá]tic|enfoqu|concentr|lugar|disculp",
            text, re.IGNORECASE,
        )
    )


def grade_8_3(text):
    """JSON forzado: respuesta es JSON valido con 3 keys requeridas."""
    try:
        parsed = json.loads(text)
        return all(k in parsed for k in ["answer", "confidence", "sources_needed"])
    except (json.JSONDecodeError, TypeError):
        return False
