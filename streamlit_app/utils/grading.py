import re
import json


def grade_1_1(text):
    pattern = re.compile(r"^(?=.*1)(?=.*2)(?=.*3).*$", re.DOTALL)
    return bool(pattern.match(text))


def grade_1_2(text):
    return bool(re.search(r"giggles", text) or re.search(r"soo", text))


def grade_2_1(text):
    return "hola" in text.lower()


def grade_2_2(text):
    return text.strip() == "Michael Jordan"


def grade_2_3(text):
    return len(text.strip().split()) >= 800


def grade_3_1(text):
    return "incorrect" in text.lower() or "not correct" in text.lower()


def grade_4_1(text):
    return bool(re.search("pigs", text.lower()) and re.search("haiku", text.lower()))


def grade_4_2(text):
    return bool(re.search("brown", text.lower()))


def grade_4_3(text):
    return bool(re.search("brown", text.lower()))


def grade_5_1(text):
    return bool(re.search("Warrior", text))


def grade_5_2(text):
    return bool(
        re.search("cat", text.lower())
        and re.search("<haiku>", text)
        and (text.count("\n") + 1) > 5
    )


def grade_5_3(text):
    return bool(
        re.search("tail", text.lower())
        and re.search("cat", text.lower())
        and re.search("<haiku>", text)
    )


# Ch 6 exercises use multi-test grading
EMAILS_6 = [
    "Hi -- My Mixmaster4000 is producing a strange noise when I operate it. It also smells a bit smoky and plasticky, like burning electronics.  I need a replacement.",
    "Can I use my Mixmaster 4000 to mix paint, or is it only meant for mixing food?",
    "I HAVE BEEN WAITING 4 MONTHS FOR MY MONTHLY CHARGES TO END AFTER CANCELLING!!  WTF IS GOING ON???",
    "How did I get here I am not good with computer.  Halp.",
]

ANSWERS_6 = [["B"], ["A", "D"], ["C"], ["D"]]

REGEX_6_1 = {"A": r"A\) P", "B": r"B\) B", "C": r"C\) B", "D": r"D\) O"}
REGEX_6_2 = {
    "A": "<answer>A</answer>",
    "B": "<answer>B</answer>",
    "C": "<answer>C</answer>",
    "D": "<answer>D</answer>",
}


def grade_6_1(response, test_case):
    idx = test_case["index"]
    return any(bool(re.search(REGEX_6_1[ans], response)) for ans in ANSWERS_6[idx])


def grade_6_2(response, test_case):
    idx = test_case["index"]
    return any(bool(re.search(REGEX_6_2[ans], response)) for ans in ANSWERS_6[idx])


def grade_7_1(response, test_case):
    idx = test_case["index"]
    if not response:
        return False
    return any(bool(re.search(ans, response[-1])) for ans in ANSWERS_6[idx])


def grade_8_1(text):
    contains = bool(
        re.search("Unfortunately", text)
        or re.search("I do not", text)
        or re.search("I don't", text)
    )
    does_not_contain = not bool(re.search("2022", text))
    return contains and does_not_contain


def grade_8_2(text):
    return bool(re.search("49-fold", text))


def grade_10_1(text):
    return "5" in text


def grade_10_2(text):
    return bool(re.search(r"0\.05|5 cents|five cents", text.lower()))


def grade_10_3(text):
    bugs_found = 0
    if re.search(r"empty|zero|division|len.*0|ZeroDivision", text, re.IGNORECASE):
        bugs_found += 1
    if re.search(r"negative|max.*0|initial", text, re.IGNORECASE):
        bugs_found += 1
    if re.search(
        r"modify.*iterating|mutating|remove.*during|concurrent", text, re.IGNORECASE
    ):
        bugs_found += 1
    return bugs_found >= 2


def grade_11_1(text):
    has_category = bool(
        re.search(r"<categor|categor|shipping|delivery|delayed", text, re.IGNORECASE)
    )
    has_structure = bool(
        re.search(r"ticket|reference|caso|numero", text, re.IGNORECASE)
    )
    return has_category and has_structure


def grade_11_2_math(text):
    return not bool(re.search(r"^12$|^12\.|the answer is 12", text, re.MULTILINE))


def grade_11_2_off(text):
    return bool(
        re.search(r"math|matematik|focus|let's|instead|sorry", text, re.IGNORECASE)
    )


def grade_11_3(text):
    try:
        parsed = json.loads(text)
        return all(k in parsed for k in ["answer", "confidence", "sources_needed"])
    except (json.JSONDecodeError, TypeError):
        return False
