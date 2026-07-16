# Especificación: generación de módulos de ejercicios (saimap-idiomas)

Instrucciones para generar el JSON de ejercicios de un módulo del curso de Inglés SAIMAP 2026.

## Entrada y salida

- **Fuente:** el archivo `.md` del módulo en `D:\Usuario\SAIMAP\IDIOMAS\INGLÉS\2026\{A1|A2}\`.
  Contiene: tesis, conceptos clave, teoría, tabla de 30 palabras de vocabulario (inglés/español/pronunciación),
  tabla de contraste de estructuras, tabla de diagnóstico de errores comunes, mnemotecnias y 5 preguntas de examen resueltas.
- **Salida:** un archivo JSON en `D:\Usuario\SAIMAP\IDIOMAS\saimap-idiomas\json\{a1|a2}\modXX.json`
  (XX = número de módulo con dos dígitos). JSON crudo, UTF-8, sin code fences ni comentarios.

## Estructura del archivo

```json
{
  "id": "a1-mod06",
  "module": 6,
  "title": "Nouns and Articles",
  "subtitle": "Sustantivos y Artículos",
  "exercises": [ ...exactamente 30 ejercicios... ]
}
```

`title` = título en inglés del módulo; `subtitle` = título en español (ambos según el index del nivel o el encabezado del .md).

## Distribución OBLIGATORIA de los 30 ejercicios

| Tipo | Cantidad |
|---|---|
| `match` | 4 |
| `quiz` | 7 |
| `gap` | 8 |
| `wordbank` | 7 |
| `speak` | 4 |

Intercala los tipos (no agrupes los 7 quiz seguidos): alterna para que la lección sea variada.

## Esquemas por tipo

### match — emparejar vocabulario (5 parejas, del vocabulario oficial del módulo)
```json
{ "type": "match", "prompt": "Empareja cada palabra con su traducción",
  "pairs": [ { "en": "hello", "es": "hola" }, ...5 parejas... ] }
```
Las 4 tarjetas match deben cubrir 20 palabras distintas de la tabla de vocabulario del módulo (sin repetir).

### quiz — test de 3 opciones
```json
{ "type": "quiz", "q": "Pregunta (puede ir en inglés, como las de examen del .md)",
  "options": ["opción A", "opción B", "opción C"], "correct": 0,
  "hint": "Pista breve en español que orienta sin dar la respuesta.",
  "explanation": "Explicación en español: por qué la correcta lo es y por qué se descartan las otras." }
```
- Reutiliza las 5 preguntas de examen resueltas del .md (resumiendo su justificación) + 2 nuevas creadas desde las tablas de errores comunes o la teoría.
- **Anti-length bias:** las 3 opciones con longitud y estilo similares; la correcta no puede ser sistemáticamente la más larga.
- Varía el índice `correct` entre 0, 1 y 2 a lo largo del módulo.

### gap — rellenar hueco
```json
{ "type": "gap", "text": "I am ___ teacher.", "options": ["a", "an", "the"],
  "answer": "a", "explanation": "Explicación en español." }
```
- `text` contiene exactamente un `___`. `answer` debe estar en `options` (3 opciones).
- Genera los gaps desde la tabla de diagnóstico de errores y los ejemplos de la teoría (morfología, concordancia, partículas).

### wordbank — traducción con banco de palabras
```json
{ "type": "wordbank", "prompt": "Soy estudiante", "direction": "es-en",
  "tiles": ["I", "am", "a", "student", "is", "the"],
  "answer": "I am a student", "explanation": "Explicación en español." }
```
- `prompt` = frase en español; `answer` = traducción al inglés.
- `tiles` = TODAS las palabras de `answer` en el mismo número de apariciones (si «the» aparece 2 veces en answer, debe haber 2 fichas) + 1-3 distractores plausibles (errores típicos del hispanohablante).
- La comparación ignora mayúsculas y signos, pero las fichas deben poder componer `answer` palabra por palabra separadas por espacio.
- Frases cortas (3-7 palabras), construidas SOLO con vocabulario y gramática ya vista en el módulo o en módulos anteriores.

### speak — lectura en voz alta
```json
{ "type": "speak", "text": "Hello, my name is John.", "es": "Hola, me llamo John." }
```
- Frase corta natural del módulo (de los ejemplos de la teoría). `es` = traducción.

## Reglas de calidad

1. **Todo el contenido sale del .md fuente** — no inventes gramática ni vocabulario ajeno al módulo. Las explicaciones deben reflejar las justificaciones del propio libro (choques cognitivos español-inglés).
2. Explicaciones SIEMPRE en español, concisas (1-3 frases), con los términos ingleses entre «comillas» o cursiva.
3. Dificultad de examen: incluye los errores-trampa del hispanohablante que el .md señala (calcos, concordancias, dobles negaciones...).
4. En los módulos 25 (Review), mezcla los contrastes clave de todo el nivel usando el propio contenido del .md de repaso (mapa de gramática, 5 errores críticos, test final).
5. Comprueba mentalmente que el JSON es válido antes de escribirlo (comillas escapadas, sin comas colgantes). Los textos con comillas dobles internas deben escaparse (\").
6. Progresión acumulativa: puedes usar vocabulario de módulos ANTERIORES del mismo nivel (o del nivel anterior), nunca de módulos posteriores.
