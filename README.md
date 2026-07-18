# SAIMAP Idiomas — App de práctica estilo Duolingo

App interactiva de idiomas de SAIMAP. Motor de juego único reutilizado por dos cursos
independientes (misma mecánica, JSON y validador; cada uno con su propia carpeta,
manifiesto y clave de progreso):

- **Inglés** (raíz del repo) — sobre el itinerario **Inglés Edición 2026**
  (`D:\Usuario\SAIMAP\IDIOMAS\INGLÉS\2026\`).
- **Latín** (`latin/`) — sobre los libros de **Latín — Colección Lenguas Sagradas**
  (`D:\Usuario\SAIMAP\LIBROS DE SAIMAP\LATÍN\`), con TTS/reconocimiento en `it-IT`
  como aproximación a la pronunciación eclesiástica.

## Estado del prototipo

**Inglés A1 y A2 — completos con el esquema de 5 subniveles**: 50 módulos × 75 ejercicios
(3.750 ejercicios en total). B1-C2 visibles pero bloqueados.
**Latín** — A1 completo con el esquema plano (25 módulos × 30), A2-C2 visibles pero bloqueados
(A2/B1/B2 ya tienen los libros fuente escritos; C1/C2 aún no están completos en origen).

- ✅ Mapa del curso con nodos en serpentina y desbloqueo encadenado también ENTRE niveles y
  ENTRE subniveles (p. ej. A2-mod01.1 exige completar el subnivel 25.5 de A1)
- ✅ 5 tipos de ejercicio: emparejar vocabulario, test de 3 opciones, rellenar huecos,
  traducción/construcción con banco de palabras y **lectura en voz alta** (Web Speech API,
  con botón de omitir)
- ✅ **Módulos subdivididos en 5 subniveles** (banco de 15 ejercicios cada uno, 3 por tipo,
  sesión de 10) — esquema completo en **Inglés A1 y A2**. **Latín A1** sigue con el esquema
  plano de 30 ejercicios / sesión de 12; ambos esquemas conviven sin problema dentro del mismo
  curso. Ver «Esquema de subniveles» más abajo.
- ✅ **Aprendizaje continuado (repaso espaciado):** ~3 de los 12 ejercicios de cada lección se inyectan
  de módulos ya completados, priorizando fallados > nunca vistos > más tiempo sin ver (Leitner-lite).
  Se marcan con la etiqueta «🔁 Repaso · Módulo N». El repaso nunca mete ejercicios de micrófono.
- ✅ Registro por ejercicio (visto/fallos/última vez) en localStorage → alimenta la priorización
- ✅ Mecánica de juego: 5 corazones diarios, +10 XP por acierto, racha por días, desbloqueo secuencial
- ✅ Audio TTS en aciertos y en el ejercicio de habla (idioma configurable por curso)
- ✅ Login por whitelist de Firebase (mismo patrón y proyecto que saimap-plataforma) + modo invitado

## Estructura

```
saimap-idiomas/
├── index.html, leccion.html        ← App de Inglés (raíz)
├── json/course.json, json/a1/, a2/ ← Contenido de Inglés
├── latin/
│   ├── index.html, leccion.html    ← App de Latín (mismo motor, TTS it-IT, clave localStorage propia)
│   └── json/course.json, json/a1/  ← Contenido de Latín
├── GENERACION_SPEC.md              ← Spec base de generación (inglés)
├── GENERACION_SPEC_LATIN.md        ← Diferencias para latín (recorte de quiz 4→3 opciones, foco en caso/concordancia)
└── validate_modules.py             ← Validador común, acepta cualquier carpeta: python validate_modules.py latin/json/a1
```

## Formato de ejercicio (json/a1/modXX.json)

```json
{ "type": "match",    "prompt": "...", "pairs": [{ "en": "...", "es": "..." }] }
{ "type": "quiz",     "q": "...", "options": ["a","b","c"], "correct": 0, "hint": "...", "explanation": "..." }
{ "type": "gap",      "text": "I am ___ teacher.", "options": ["a","an","the"], "answer": "a", "explanation": "..." }
{ "type": "wordbank", "prompt": "Soy estudiante", "tiles": ["I","am","a","student","is"], "answer": "I am a student", "explanation": "..." }
{ "type": "speak",    "text": "Hello, my name is John.", "es": "Hola, me llamo John." }
```

Para añadir un módulo nuevo: crear `json/a1/modXX.json` y añadirle `"file": "a1/modXX.json"`
a su entrada en `course.json`. El nodo se desbloquea al completar el módulo anterior.

## Esquema de subniveles (piloto)

Un módulo puede subdividirse en 5 subniveles en vez de tener un banco plano de 30 ejercicios.
Dos cambios sobre el formato normal:

1. En `course.json`, la entrada del módulo lleva `"sublevels": 5` (además de `file`).
2. El archivo del módulo cambia `"exercises": [...30]` por:

```json
{
  "id": "a1-mod01", "module": 1, "title": "...", "subtitle": "...",
  "sublevels": [
    { "n": 1, "title": "Saludos y despedidas", "exercises": [ ...15, 3 de cada tipo... ] },
    { "n": 2, "title": "...", "exercises": [ ...15... ] },
    { "n": 3, "title": "...", "exercises": [ ...15... ] },
    { "n": 4, "title": "...", "exercises": [ ...15... ] },
    { "n": 5, "title": "...", "exercises": [ ...15... ] }
  ]
}
```

El mapa (`index.html`) genera un nodo por subnivel (etiquetado `1.1`…`1.5`), con el mismo
desbloqueo secuencial de siempre (subnivel 2 exige completar el 1, y el módulo siguiente exige
completar el subnivel 5). El id de progreso de cada subnivel es `a1-mod01-s1`…`s5`.

La lección (`leccion.html`) detecta el parámetro `?sub=N` en la URL: si existe, sesión de
**10 ejercicios** (banco de 15, 2 huecos de repaso); si no, sigue siendo la sesión clásica de
**12** (banco de 30, 3 huecos de repaso). El repaso espaciado también funciona a esta granularidad
— un subnivel ya completado puede aparecer como repaso dentro de otro subnivel del mismo módulo
o de módulos posteriores, etiquetado «Módulo 1.2» en vez de «Módulo 1».

`validate_modules.py` reconoce ambos esquemas automáticamente (mira si el módulo tiene
`sublevels` o `exercises` de nivel superior).

## Auth y progreso

- Whitelist: apunta al proyecto Firebase `saimap-ingenieria-informatica`
  (SHA-256 del email contra la colección `whitelist`, vía REST — igual que saimap-plataforma).
  Los correos se gestionan con el `emails.txt` + `import_whitelist.js` de esa plataforma.
- Progreso (XP, racha, corazones, módulos completados): `localStorage` del navegador.
  Pendiente para producción: sincronizarlo a Firestore (`users/{hash}`) como hace la plataforma de tests.

## Ejecutar en local

Los JSON se cargan con `fetch`, así que hace falta un servidor local (no funciona con file://):

```
cd saimap-idiomas
python -m http.server 8123
```

y abrir http://localhost:8123. El reconocimiento de voz requiere Chrome/Edge y permiso de micrófono
(en localhost funciona; en producción requiere HTTPS — GitHub Pages lo cumple).

## Próximas fases

1. Decidir si Inglés A2 (y Latín) pasan también al esquema de subniveles, o si Inglés A1
   se queda como el único nivel "denso" del curso.
2. Generar el resto de niveles con subagentes (mismo proceso ya usado):
   - Inglés B1-C2 (100 módulos) → `GENERACION_SPEC.md` (+ `GENERACION_SPEC_SUBLEVELS.md` si se
     decide subdividirlos también)
   - Latín A2-B2 (75 módulos, libros fuente ya completos) y C1-C2 (cuando se terminen los libros) → `GENERACION_SPEC_LATIN.md`
3. Sincronizar el progreso a Firestore (`users/{hash}`) para que viaje entre dispositivos.
4. Publicar el cambio de Inglés A1 (subniveles) en GitHub Pages — de momento solo está en local.
5. Revisar la Tabla de vocabulario de `Inglés_A1_MOD16_PrepositionsTime.md` y
   `Inglés_A1_MOD17_TimeDaily.md`: los subagentes detectaron que las tablas de 30 palabras del
   `.md` fuente tienen placeholders sin rellenar (`word_16_1`, `traduccion_16_1`...) en vez de
   vocabulario real. Reconstruyeron el vocabulario a partir de la teoría y los ejercicios ya
   existentes, así que el juego funciona bien, pero el libro fuente en sí sigue roto en esa tabla.
