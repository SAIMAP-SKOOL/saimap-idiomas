# Especificación: generación de módulos del curso Biblia (saimap-idiomas/biblia)

Instrucciones para generar el JSON de ejercicios de un módulo del curso **Biblia · Canon y Apócrifos** de SAIMAP Ecclesia.

## Fuente

- **Texto de referencia:** la Sagrada Biblia de la Conferencia Episcopal Española, consultada en
  `https://www.conferenciaepiscopal.es/biblia/{libro}/` (misma edición que enlazan los "Libro Completo" de la academia en Skool).
- La CEE es la **fuente de verdad para los hechos**: personajes, acontecimientos, orden narrativo,
  referencias (Gén 3:15) y grafías oficiales de nombres propios (Nahún, Henoc, Guijón, Abrahán...).
- **Copyright:** la traducción CEE está protegida. Las preguntas y explicaciones son SIEMPRE redacción
  propia; las citas literales se limitan a versículos célebres, breves (una frase), con su referencia.
  Nunca convertir capítulos enteros en ejercicios de texto literal.

## Estructura del curso

- `biblia/json/course.json` replica el orden de la academia en Skool: Pentateuco → Históricos →
  Sapienciales y Poéticos → Proféticos → Evangelios → Hechos → Corpus Paulino → Cartas Católicas →
  Cartas de San Juan → Judas → Apocalipsis → Textos Apócrifos (nivel final, se genera el último).
- **Peso variable por libro:** cada libro se divide en módulos según su extensión y densidad —
  4-5 módulos los monumentales (Génesis, Éxodo, Salmos, Isaías), 2-3 los medianos (Samuel, Reyes,
  Evangelios, Romanos, Hechos), 1 los breves (profetas menores, cartas cortas). Cada módulo es una
  **unidad narrativa o temática** (p. ej. «Génesis I — La Creación y la Caída», Gén 1–4), nunca un
  reparto mecánico de capítulos.
- Salida: `biblia/json/{nivel}/modXX.json` (nivel = código del bloque en minúsculas: pen, his, sap...).

## Estructura del archivo

```json
{
  "id": "pen-mod01",
  "module": 1,
  "title": "Génesis I — La Creación y la Caída",
  "subtitle": "Génesis 1–4",
  "exercises": [ ...exactamente 30 ejercicios... ]
}
```

`subtitle` = rango de capítulos o descripción breve del módulo.

## Distribución OBLIGATORIA de los 30 ejercicios (sin `speak`)

| Tipo | Cantidad |
|---|---|
| `match` | 4 |
| `quiz` | 9 |
| `gap` | 9 |
| `wordbank` | 8 |

Intercala los tipos y sigue el orden narrativo del texto (los ejercicios de Gén 1 antes que los de Gén 4).
La sesión del motor es de 10 ejercicios, con 2 huecos (20%) de repaso espaciado de módulos anteriores
(`SESSION_SIZE = 10`, `REVIEW_SLOTS = 2` en `leccion.html`) — el repaso lo gestiona el motor, no el JSON.

## Esquemas por tipo

Los campos son los mismos del motor común (ver `GENERACION_SPEC.md` de la raíz). Particularidades bíblicas:

### match — emparejar (5 parejas; `en` = columna izquierda, `es` = columna derecha)
Usos: día de la creación ↔ obra, personaje ↔ descripción, elemento ↔ significado, frase ↔ quien la
pronuncia, libro ↔ grupo. Las 5 respuestas de la derecha deben ser inequívocas (nunca dos izquierdas
que compartan la misma derecha válida).

### quiz — test de 3 opciones
De contenido: acontecimientos, personajes, causas, lugares. `hint` orienta sin dar la respuesta;
`explanation` cita la referencia (Gén 4:15) y aclara por qué se descartan las otras opciones.
Anti-length bias y `correct` repartido entre 0, 1 y 2.

### gap — completar el texto (un `___`, 3 opciones)
Frases célebres breves o datos del relato. Los distractores, plausibles (p. ej. «limo» de la Vulgata
frente al «polvo» de la CEE).

### wordbank — reconstruir el pasaje
`prompt` = referencia + contexto («Gén 4:9 · La respuesta de Caín…»); `answer` = versículo célebre
BREVE (5-9 palabras, sin signos problemáticos); `tiles` = todas las palabras de `answer` (repetidas
según aparezcan) + 1-3 distractores plausibles. Solo versículos famosos; el resto de la memorización
es de contenido, no literal.

## Reglas de calidad

1. Todos los hechos salen del texto bíblico verificado en la CEE — no inventar datos, nombres ni referencias.
2. Explicaciones SIEMPRE con la referencia bíblica (libro capítulo:versículo), 1-3 frases.
3. Grafías de nombres propios según la CEE (coinciden con los títulos de la academia en Skool).
4. Tono ecuménico y didáctico: las lecturas tradicionales cristianas (protoevangelio, Trinidad en el
   «hagamos») se presentan como «la tradición cristiana lee aquí…».
5. Progresión acumulativa: un módulo puede aludir a módulos anteriores, nunca a posteriores.
6. Validar con `python validate_modules.py biblia/json/pen` antes de dar por terminado un módulo.
