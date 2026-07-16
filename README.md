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

**Inglés** — A1 y A2 completos (25 + 25 módulos), B1-C2 visibles pero bloqueados.
**Latín** — A1 completo (25 módulos), A2-C2 visibles pero bloqueados (A2/B1/B2 ya
tienen los libros fuente escritos; C1/C2 aún no están completos en origen).

En total: **75 módulos × 30 ejercicios = 2.250 ejercicios**, generados del contenido
real de los `.md` y validados con `validate_modules.py`.

- ✅ Mapa del curso con nodos en serpentina y desbloqueo encadenado también ENTRE niveles
  (p. ej. A2-mod01 exige completar A1-mod25)
- ✅ 5 tipos de ejercicio: emparejar vocabulario, test de 3 opciones, rellenar huecos,
  traducción/construcción con banco de palabras y **lectura en voz alta** (Web Speech API,
  con botón de omitir)
- ✅ **Sesiones de 12 ejercicios** muestreadas del banco de 30 ⇒ rejugar un módulo da ejercicios distintos
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

1. Generar el resto de niveles con subagentes (mismo proceso que A1/A2 de inglés y A1 de latín):
   - Inglés B1-C2 (100 módulos) → `GENERACION_SPEC.md`
   - Latín A2-B2 (75 módulos, libros fuente ya completos) y C1-C2 (cuando se terminen los libros) → `GENERACION_SPEC_LATIN.md`
2. Sincronizar el progreso a Firestore (`users/{hash}`) para que viaje entre dispositivos.
3. Publicar `latin/` en GitHub Pages junto al resto (ya está `saimap-idiomas` publicado para inglés)
   y enlazarlo desde la pestaña de Latín en SAIMAP Ecclesia / Lenguas Sagradas, como se hizo con inglés.
