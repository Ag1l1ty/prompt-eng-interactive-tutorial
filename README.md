# Tutorial Interactivo de Ingenieria de Prompts con Claude

> Basado en el [tutorial original de Anthropic](https://github.com/anthropics/prompt-eng-interactive-tutorial) - Traducido al espanol, actualizado a Claude Opus 4.6, y ampliado con capitulos nuevos.

## Introduccion

Este curso te proporciona una comprension paso a paso de como disenar prompts optimos para Claude. Al completar este curso, seras capaz de:

- Dominar la estructura basica de un buen prompt
- Reconocer modos de fallo comunes y aprender las tecnicas '80/20' para abordarlos
- Entender las fortalezas y debilidades de Claude
- Construir prompts solidos desde cero para casos de uso comunes
- Usar pensamiento extendido (extended thinking) para problemas complejos
- Disenar system prompts avanzados para aplicaciones de produccion

## Requisitos Previos

- Una **API key de Anthropic** - puedes obtener una en la [Consola de Anthropic](https://console.anthropic.com/)
- Python 3.8+
- Familiaridad basica con Jupyter Notebooks

## Como Empezar

### Opcion 1: Web App (Recomendado)

La forma mas facil de usar el tutorial es la **web app interactiva** con Streamlit:

1. Clona el repositorio y ejecuta la app:
```bash
git clone https://github.com/Ag1l1ty/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial
pip install -r streamlit_app/requirements.txt
streamlit run streamlit_app/app.py
```

2. Ingresa tu API key de Anthropic en la barra lateral
3. Navega por los capitulos y completa los ejercicios interactivos

Tambien puedes deployar la app gratis en [Streamlit Cloud](https://streamlit.io/cloud) conectando tu fork del repositorio.

### Opcion 2: Jupyter Notebooks

1. Clona este repositorio:
```bash
git clone https://github.com/Ag1l1ty/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Abre Jupyter y comienza con el notebook `00_Tutorial_Como_Empezar.ipynb`:
```bash
jupyter notebook
```

4. En el notebook 00, configura tu API key y ejecuta las celdas en orden.

### Opcion 3: Google Colab

1. Sube todos los archivos `.ipynb` y `hints.py` a tu Google Drive o directamente a Colab
2. Abre `00_Tutorial_Como_Empezar.ipynb` en Colab
3. Configura tu API key y sigue las instrucciones

## Estructura del Curso

Cada capitulo consiste en una **leccion** y un conjunto de **ejercicios** interactivos. Se recomienda seguir el curso en orden.

### Principiante
| Capitulo | Tema | Archivo |
|----------|------|---------|
| 1 | Estructura Basica de Prompts | `01_Estructura_Basica_de_Prompts.ipynb` |
| 2 | Ser Claro y Directo | `02_Ser_Claro_y_Directo.ipynb` |
| 3 | Asignacion de Roles | `03_Asignacion_de_Roles.ipynb` |

### Intermedio
| Capitulo | Tema | Archivo |
|----------|------|---------|
| 4 | Separar Datos de Instrucciones | `04_Separar_Datos_de_Instrucciones.ipynb` |
| 5 | Formato de Output y Hablar por Claude | `05_Formato_de_Output_y_Hablar_por_Claude.ipynb` |
| 6 | Precognicion (Pensar Paso a Paso) | `06_Precognicion_Pensar_Paso_a_Paso.ipynb` |
| 7 | Uso de Ejemplos (Few-Shot) | `07_Uso_de_Ejemplos_Few_Shot.ipynb` |

### Avanzado
| Capitulo | Tema | Archivo |
|----------|------|---------|
| 8 | Evitar Alucinaciones | `08_Evitar_Alucinaciones.ipynb` |
| 9 | Prompts Complejos desde Cero | `09_Prompts_Complejos_desde_Cero.ipynb` |
| 10 | Pensamiento Extendido (Extended Thinking) | `10_Pensamiento_Extendido.ipynb` |
| 11 | System Prompts Avanzados | `11_System_Prompts_Avanzados.ipynb` |

### Apendices
| Apendice | Tema | Archivo |
|----------|------|---------|
| 12.1 | Encadenamiento de Prompts | `12.1_Apendice_Encadenamiento_de_Prompts.ipynb` |
| 12.2 | Uso de Herramientas (Tool Use) | `12.2_Apendice_Uso_de_Herramientas.ipynb` |
| 12.3 | Busqueda y Recuperacion | `12.3_Apendice_Busqueda_y_Recuperacion.ipynb` |

## Notas Tecnicas

- Este curso utiliza **Claude Opus 4.6** (`claude-opus-4-6`) con temperature 0 para resultados deterministicos
- Todas las tecnicas de este curso tambien se aplican a otros modelos de la familia Claude (Sonnet 4.5, Haiku 4.5)
- Los prompts de ejemplo se mantienen en **ingles** ya que las tecnicas de ingenieria de prompts son independientes del idioma
- Las explicaciones, instrucciones y comentarios estan en **espanol**

## Recursos Adicionales

- [Documentacion de Anthropic](https://docs.anthropic.com/)
- [API de Messages](https://docs.anthropic.com/claude/reference/messages_post)
- [Guia de Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [Clave de respuestas (original en ingles)](https://docs.google.com/spreadsheets/d/1jIxjzUWG-6xBVIa2ay6yDpLyeuOh_hR_ZB75a47KX_E/edit?usp=sharing)

## Atribucion

Este tutorial es una adaptacion al espanol del [Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) original de Anthropic. Se ha actualizado a modelos actuales (Claude Opus 4.6), se han corregido bugs conocidos, y se han agregado dos capitulos nuevos sobre Pensamiento Extendido y System Prompts Avanzados.

## Licencia

MIT License - Ver [LICENSE](LICENSE) para mas detalles.
