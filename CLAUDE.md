# CLAUDE.md - Contexto del Proyecto

## Resumen del Proyecto

Fork en espanol del tutorial interactivo de ingenieria de prompts de Anthropic.
- **Repo original:** `anthropics/prompt-eng-interactive-tutorial`
- **Repo destino:** `Ag1l1ty/prompt-eng-interactive-tutorial`
- **Objetivo:** Traducir, actualizar a Claude Opus 4.6, corregir bugs, y agregar capitulos nuevos.

## Estado del Repositorio

- **Directorio local:** `/Users/agilitychanges/prompt-eng-interactive-tutorial`
- **Remote `origin`:** `https://github.com/Ag1l1ty/prompt-eng-interactive-tutorial.git` (NO EXISTE AUN en GitHub - hay que crearlo)
- **Remote `upstream`:** `https://github.com/anthropics/prompt-eng-interactive-tutorial.git`
- **Branch:** `master`
- **IMPORTANTE:** Todo el trabajo esta local, NADA se ha pusheado. Hay cambios staged, unstaged y archivos untracked.

## Estructura de Archivos (actual, en disco)

```
prompt-eng-interactive-tutorial/
├── .gitignore
├── LICENSE                                          (nuevo, untracked)
├── README.md                                        (modificado, unstaged)
├── requirements.txt                                 (nuevo, untracked)
├── hints.py                                         (renombrado desde AmazonBedrock/utils/, modificado)
├── 00_Tutorial_Como_Empezar.ipynb                   (renombrado + modificado)
├── 01_Estructura_Basica_de_Prompts.ipynb            (renombrado + modificado)
├── 02_Ser_Claro_y_Directo.ipynb                     (renombrado + modificado)
├── 03_Asignacion_de_Roles.ipynb                     (renombrado + modificado)
├── 04_Separar_Datos_de_Instrucciones.ipynb          (renombrado + modificado)
├── 05_Formato_de_Output_y_Hablar_por_Claude.ipynb   (renombrado + modificado)
├── 06_Precognicion_Pensar_Paso_a_Paso.ipynb         (renombrado + modificado)
├── 07_Uso_de_Ejemplos_Few_Shot.ipynb                (renombrado + modificado)
├── 08_Evitar_Alucinaciones.ipynb                    (renombrado + modificado)
├── 09_Prompts_Complejos_desde_Cero.ipynb            (renombrado + modificado)
├── 10_Pensamiento_Extendido.ipynb                   (NUEVO, untracked - Cap nuevo)
├── 11_System_Prompts_Avanzados.ipynb                (NUEVO, untracked - Cap nuevo)
├── 12.1_Apendice_Encadenamiento_de_Prompts.ipynb    (renombrado + modificado)
├── 12.2_Apendice_Uso_de_Herramientas.ipynb          (renombrado + modificado)
├── 12.3_Apendice_Busqueda_y_Recuperacion.ipynb      (renombrado + modificado)
├── Anthropic 1P/   (directorio original, staged para eliminacion)
└── AmazonBedrock/  (directorio original, staged para eliminacion)
```

## Plan de Tareas

### Completadas
1. **Fork y reestructurar el repositorio** - Archivos movidos de `Anthropic 1P/` a raiz con nombres en espanol. `AmazonBedrock/` eliminado. TODO STAGED pero NO COMMITEADO.
2. **Crear Capitulo 10: Pensamiento Extendido** - `10_Pensamiento_Extendido.ipynb` creado. Cubre extended thinking API, budget_tokens, comparaciones con/sin thinking, 3 ejercicios.
3. **Crear Capitulo 11: System Prompts Avanzados** - `11_System_Prompts_Avanzados.ipynb` creado. Cubre multi-seccion XML, personas, guardrails, formato JSON, 3 ejercicios.
4. **Escribir README.md en espanol** - README completo con tabla de contenidos, instrucciones de instalacion, estructura del curso.

### En Progreso (donde se bloqueo la sesion anterior)
5. **Actualizar modelos a Claude Opus 4.6** - Los notebooks deben usar `claude-opus-4-6` como MODEL_NAME. Verificar que TODOS los notebooks usen este modelo consistentemente. El notebook 00 define MODEL_NAME que se comparte via `%store`.
6. **Corregir bugs conocidos del repo original** - Issues a corregir:
   - **#56**: `hints` module not found - CORREGIDO: hints.py movido a raiz + sys.path fix en notebooks
   - **#61**: Appendix Tool Use usa modelo deprecado `claude-3-sonnet-20240229` - Actualizar a `claude-opus-4-6`
   - **#48**: Cap 8 hallucination example conflates two techniques - Revisar y separar las tecnicas
   - **#11**: Typo "handilgj" en 10.2 Appendix Tool Use - Corregir typo
   - **#10**: f-string missing en 09_Complex_Prompts - Verificar y corregir
   - **#43**: Link roto 404 a how-to-use-system-prompts - Actualizar URL
7. **Traducir todos los notebooks a espanol** - Instrucciones y explicaciones en espanol, prompts de ejemplo en ingles. Cada notebook tiene:
   - Titulos/headers en espanol
   - Explicaciones/texto markdown en espanol
   - Prompts de ejemplo en INGLES (intencionalmente)
   - Funciones de calificacion con mensajes en espanol
   - Hints en hints.py en espanol

### Pendiente
8. **Modernizar apendice de Tool Use (12.2)** - Actualizar a la API moderna de tool_use de Anthropic. El original usa un modelo deprecado y posiblemente una API vieja.

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
- Hints para capitulos 10 y 11 ya agregados al archivo

## Bugs del Repo Original (referencia)

| Issue | Titulo | Estado en nuestro fork |
|-------|--------|----------------------|
| #56 | hints module not found | CORREGIDO (sys.path fix) |
| #61 | Tool Use appendix usa modelo deprecado | POR VERIFICAR en 12.2 |
| #48 | Cap 8 conflates hallucination techniques | POR REVISAR |
| #11 | Typo "handilgj" en Tool Use appendix | POR VERIFICAR en 12.2 |
| #10 | f-string missing en Cap 9 | POR VERIFICAR |
| #43 | Link 404 system prompts | POR VERIFICAR en 01 |
| #2 | Add LICENSE file | CORREGIDO (LICENSE agregado) |
| #21 | Insecure API key usage | PARCIAL (se usa %store) |

## Proximos Pasos (orden sugerido)

1. Crear el repositorio en GitHub (`Ag1l1ty/prompt-eng-interactive-tutorial`)
2. Commitear TODO el trabajo actual y pushear
3. Verificar y completar actualizacion de modelos a Opus 4.6 en todos los notebooks
4. Verificar y corregir cada bug listado arriba
5. Completar traduccion de notebooks restantes
6. Modernizar apendice Tool Use (12.2)
