# Especificación: generación de módulos de ejercicios — Latín (saimap-idiomas)

Adaptación de `GENERACION_SPEC.md` (inglés) al curso de Latín de SAIMAP Ecclesia. Lee primero
ese documento si no lo has hecho: la estructura de los 5 tipos de ejercicio, la distribución
de 30 ejercicios y las reglas de calidad son las mismas. Este documento solo cubre las
diferencias específicas del latín.

## Entrada y salida

- **Fuente:** el archivo `.md` del módulo en `D:\Usuario\SAIMAP\LIBROS DE SAIMAP\LATÍN\A1 - LATÍN\`.
  Mismo esqueleto que el inglés: Tesis + Enfoque Examen, Conceptos Clave, teoría, tabla de
  30 palabras («Latín | Español | Pronunciación»), tabla de contraste de estructuras, tabla de
  diagnóstico de errores comunes, mnemotecnias y preguntas de examen resueltas.
- **Salida:** `D:\Usuario\SAIMAP\IDIOMAS\saimap-idiomas\latin\json\a1\modXX.json` (XX con dos dígitos).
  Mismo formato de archivo que el inglés (`id`, `module`, `title`, `subtitle`, `exercises`).
  Los nombres de archivo fuente en A1 ya usan numeración 01-25 (no como A2+, que usa numeración
  global 26-50, etc. — para A1 no hay que remapear nada).

## Diferencia clave: las preguntas de examen tienen 4 opciones, no 3

Los `.md` de latín presentan las preguntas resueltas con **4 opciones (a, b, c, d)**, ya sea en
formato markdown simple o en tarjetas HTML (`<div class="question-card">`). El componente `quiz`
de la app solo admite **3 opciones**. Al convertir cada pregunta:

1. Identifica la opción correcta (marcada con ✅ o dentro de `question-option correct`).
2. De las 3 opciones incorrectas, **descarta la más floja** — la que sea obviamente absurda,
   gramaticalmente imposible a primera vista, o la que la propia justificación del libro despache
   en una frase sin verdadero valor didáctico (compara los cuatro párrafos de "Incorrecto:" del
   `.md`: el distractor con la explicación más corta/trivial suele ser el más débil).
3. Conserva la correcta + los 2 distractores que representen **confusiones reales** del
   estudiante (errores de caso, concordancia o cantidad vocálica que un hispanohablante comete
   de verdad) — son los que enseñan algo al fallarlos.
4. Reescribe `hint` y `explanation` en español, resumiendo la justificación del libro para las
   3 opciones que quedan (no hace falta mencionar la opción descartada).
5. Varía qué posición (0, 1 o 2) ocupa la correcta a lo largo del módulo — no la dejes siempre
   en el mismo índice.

Esta misma regla de recorte aplica también a los **quiz nuevos que generes** desde las tablas de
errores comunes: constrúyelos ya con 3 opciones desde el principio (no generes una cuarta para
luego descartarla).

## Regla obligatoria: el `quiz` es práctico, no de análisis gramatical

Los `.md` fuente formulan sus preguntas de examen como análisis metalingüístico: *"¿Cuál es la
función de reginae en esta oración?"* con opciones tipo *"Dativo singular (objeto indirecto)"*.
**Ese formato queda prohibido en el JSON.** La teoría y el etiquetado gramatical ya están en el
libro; el `quiz` de la app tiene que poner al alumno a **usar** el latín, no a nombrarlo.

Al convertir o crear un `quiz`, reformula siempre como una tarea de producción o reconocimiento
de uso, con las 3 opciones siendo **frases completas en latín** (o casi completas) que difieren
exactamente en el rasgo gramatical que enseña el módulo — nunca etiquetas de caso/función como
opciones.

**Transformación de ejemplo** (misma contraste gramatical, distinto envoltorio):

| ❌ Antes (análisis) | ✅ Ahora (uso) |
|---|---|
| q: *"En «Nauta reginae epistulam dat», ¿qué función cumple reginae?"* <br> opciones: `["Nominativo plural (sujeto)", "Dativo singular (objeto indirecto)", "Genitivo singular (complemento)"]` | q: *"¿Cómo se dice «El marinero le da una carta a la reina»?"* <br> opciones: `["Nauta reginam epistulam dat.", "Nauta reginae epistulam dat.", "Nauta reginae epistulam dant."]` (correct=1) |

Patrones de enunciado recomendados (calcados del estilo que ya usa el inglés en `GENERACION_SPEC.md`):
- *"¿Cuál es la traducción correcta de [frase en español]?"* con 3 frases latinas completas.
- *"Elige la frase gramaticalmente correcta."* con 3 variantes que cambian un caso/concordancia/
  conjugación.
- *"Completa la idea: [contexto breve]. ¿Cuál de estas continuaciones es correcta?"*
- Preguntas de escucha/lectura: *"¿Qué frase describe correctamente la imagen/situación: [contexto]?"*

La `explanation` sigue educando en la gramática (por qué esa desinencia, esa concordancia o ese
tiempo verbal es la correcta y las otras no), pero el **enunciado y las opciones** siempre visten
de comunicación real, no de terminología de análisis sintáctico. Aplica esto tanto a los quiz que
conviertas desde las preguntas resueltas del libro como a los que crees desde cero a partir de las
tablas de errores comunes.

## Vocabulario y campos `en`/`es`

El motor de la app es agnóstico al idioma: los campos JSON siguen llamándose `en`/`es` (`match`)
o `text`/`answer` en el idioma meta + `es` en español, exactamente igual que en inglés — pero
para latín el campo "en" contiene la palabra o frase **en latín**, no en inglés. No cambies los
nombres de los campos, solo su contenido.

- **`match`:** usa el lemma limpio como tile (p. ej. `"rosa"`, no `"rosa, -ae (f.)"`). El
  género/declinación gramatical no hace falta en la ficha de emparejar; ya se trabaja en `gap`
  y `wordbank`.
- **`gap` y `wordbank`:** aquí es donde vive la gramática real. Los blancos y los bancos de
  palabras deben testear **selección de caso** (nominativo/acusativo/genitivo/dativo/ablativo/
  vocativo según el módulo), **concordancia adjetivo-sustantivo** o **conjugación verbal**, según
  el contenido del módulo — usa directamente los ejemplos y las tablas de errores comunes del
  `.md` (p. ej. *"Agricola bon___"* con opciones `us / a / um` en el módulo de concordancia).
- **`wordbank`:** las frases de ejemplo del propio módulo (*"Nauta terram amat"*, *"Puella
  bona in silvā ambulat"*...) funcionan directamente como origen; los distractores en `tiles`
  deben ser las formas de caso incorrectas típicas del error hispanohablante (p. ej. incluir
  tanto `puellam` como `puella`/`puellae` cuando la frase requiere acusativo).
- **`speak`:** usa la **pronunciación eclesiástica** cuando el módulo distinga clásica/eclesiástica
  (la app reproduce el audio con una voz italiana, la aproximación más cercana disponible en el
  navegador a la fonética eclesiástica: c/g suaves ante e/i, v como fricativa). No hace falta
  anotar la pronunciación fonética en el JSON, solo el texto latino y su traducción en `es`.

## Resto de reglas

Igual que en `GENERACION_SPEC.md`: distribución exacta 4 match / 7 quiz / 8 gap / 7 wordbank /
4 speak, tipos intercalados, explicaciones siempre en español, progresión acumulativa (solo
gramática y vocabulario ya visto en el módulo actual o anteriores), y validar con
`python validate_modules.py latin/json/a1` antes de dar el módulo por terminado.
