# CLAUDE.md - Contexto del Proyecto

## Resumen del Proyecto

Fork en espanol del tutorial interactivo de ingenieria de prompts de Anthropic.
- **Repo original:** `anthropics/prompt-eng-interactive-tutorial`
- **Repo destino:** `Ag1l1ty/prompt-eng-interactive-tutorial`
- **Estado:** COMPLETO - todas las tareas finalizadas y pusheadas.

## Estado del Repositorio

- **Directorio local:** `/Users/agilitychanges/prompt-eng-interactive-tutorial`
- **Remote `origin`:** `https://github.com/Ag1l1ty/prompt-eng-interactive-tutorial.git`
- **Remote `upstream`:** `https://github.com/anthropics/prompt-eng-interactive-tutorial.git`
- **Branch:** `master`
- **Git config:** `Ag1l1ty` / `229850407+Ag1l1ty@users.noreply.github.com`

## Estructura de Archivos

```
prompt-eng-interactive-tutorial/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── hints.py
├── CLAUDE.md
├── PROGRESS.md
├── 00_Tutorial_Como_Empezar.ipynb
├── 01_Estructura_Basica_de_Prompts.ipynb
├── 02_Ser_Claro_y_Directo.ipynb
├── 03_Asignacion_de_Roles.ipynb
├── 04_Separar_Datos_de_Instrucciones.ipynb
├── 05_Formato_de_Output_y_Hablar_por_Claude.ipynb
├── 06_Precognicion_Pensar_Paso_a_Paso.ipynb
├── 07_Uso_de_Ejemplos_Few_Shot.ipynb
├── 08_Evitar_Alucinaciones.ipynb
├── 09_Prompts_Complejos_desde_Cero.ipynb
├── 10_Pensamiento_Extendido.ipynb          (capitulo nuevo)
├── 11_System_Prompts_Avanzados.ipynb       (capitulo nuevo)
├── 12.1_Apendice_Encadenamiento_de_Prompts.ipynb
├── 12.2_Apendice_Uso_de_Herramientas.ipynb (reescrito con API moderna)
└── 12.3_Apendice_Busqueda_y_Recuperacion.ipynb
```

## Tareas Completadas

1. **Fork y reestructurar** - Archivos movidos de `Anthropic 1P/` a raiz con nombres en espanol. `AmazonBedrock/` eliminado.
2. **Capitulo 10: Pensamiento Extendido** - Extended thinking API, budget_tokens, comparaciones, 3 ejercicios.
3. **Capitulo 11: System Prompts Avanzados** - Multi-seccion XML, personas, guardrails, formato JSON, 3 ejercicios.
4. **README.md en espanol** - Tabla de contenidos, instrucciones de instalacion, estructura del curso.
5. **Modelos actualizados a Claude Opus 4.6** - Todos los notebooks usan `MODEL_NAME = "claude-opus-4-6"` definido en notebook 00.
6. **Bugs corregidos** - #56 (hints not found), #61 (modelo deprecado), #48 (hallucination explanation), #11 (typo), #10 (f-string), #43 (link 404), #2 (LICENSE).
7. **Traduccion completa** - Todos los notebooks con markdown en espanol, prompts en ingles, comentarios en espanol.
8. **Tool Use modernizado (12.2)** - Reescrito con API nativa: parametro `tools`, JSON Schema, `ToolUseBlock`, bucle agentico.

## Convenciones Tecnicas

### Modelo
- **Modelo:** `claude-opus-4-6` (Claude Opus 4.6)
- **Temperature:** 0.0 para resultados deterministicos (excepto con extended thinking donde se omite)
- **Variable:** MODEL_NAME se define en notebook 00 y se comparte via `%store`

### Idioma en notebooks
- **Markdown/explicaciones:** Espanol (sin acentos en nombres de archivo)
- **Prompts de ejemplo:** Ingles (las tecnicas son independientes del idioma)
- **Codigo/variables:** Ingles
- **hints.py:** Textos en espanol

### Patron de setup en cada notebook
```python
!pip install anthropic
import anthropic
%store -r API_KEY
%store -r MODEL_NAME
client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt, system_prompt="", prefill=""):
    # ... patron estandar
```

### Patron de calificacion
```python
def grade_exercise(text):
    # regex check
    return bool(...)

print("\n--------------------------- CALIFICACION ---------------------------")
print("Este ejercicio se ha resuelto correctamente:", grade_exercise(response))
```

### Hints
- Archivo: `hints.py` en raiz del proyecto
- Naming: `exercise_X_Y_hint` donde X=capitulo, Y=ejercicio
- Se importan con: `from hints import exercise_X_Y_hint; print(exercise_X_Y_hint)`

## Bugs del Repo Original (referencia)

| Issue | Titulo | Estado |
|-------|--------|--------|
| #56 | hints module not found | CORREGIDO (sys.path fix) |
| #61 | Tool Use appendix usa modelo deprecado | CORREGIDO (MODEL_NAME + reescritura) |
| #48 | Cap 8 conflates hallucination techniques | CORREGIDO (explicacion reescrita) |
| #11 | Typo "handilgj" en Tool Use appendix | CORREGIDO (eliminado en reescritura) |
| #10 | f-string missing en Cap 9 | CORREGIDO (f-prefix agregado) |
| #43 | Link 404 system prompts | CORREGIDO (URL actualizada) |
| #2 | Add LICENSE file | CORREGIDO (LICENSE agregado) |
| #21 | Insecure API key usage | MITIGADO (se usa %store) |
