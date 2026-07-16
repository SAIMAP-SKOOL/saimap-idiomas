# SAIMAP Idiomas — App de práctica estilo Duolingo

Prototipo de la app interactiva de idiomas de SAIMAP, construida sobre el itinerario
de **Inglés Edición 2026** (`D:\Usuario\SAIMAP\IDIOMAS\INGLÉS\2026\`).

## Estado del prototipo

- ✅ Mapa del curso completo (A1 y A2 con 25 nodos cada uno en serpentina; B1-C2 visibles pero bloqueados)
- ✅ **A1 completo (25 módulos) y A2 completo (25 módulos)** con banco de 30 ejercicios por módulo
  (1.500 ejercicios generados del contenido real de los .md, validados con validate_modules.py)
- ✅ Desbloqueo encadenado también ENTRE niveles: A2-mod01 exige completar A1-mod25
- ✅ 5 tipos de ejercicio: emparejar vocabulario, test de 3 opciones, rellenar huecos,
  traducción con banco de palabras y **lectura en voz alta** (Web Speech API, con botón de omitir)
- ✅ **Sesiones de 12 ejercicios** muestreadas del banco de 30 ⇒ rejugar un módulo da ejercicios distintos
- ✅ **Aprendizaje continuado (repaso espaciado):** ~3 de los 12 ejercicios de cada lección se inyectan
  de módulos ya completados, priorizando fallados > nunca vistos > más tiempo sin ver (Leitner-lite).
  Se marcan con la etiqueta «🔁 Repaso · Módulo N». El repaso nunca mete ejercicios de micrófono.
- ✅ Registro por ejercicio (visto/fallos/última vez) en localStorage → alimenta la priorización
- ✅ Mecánica de juego: 5 corazones diarios, +10 XP por acierto, racha por días, desbloqueo secuencial
- ✅ Audio TTS (inglés) en aciertos y en el ejercicio de habla
- ✅ Login por whitelist de Firebase (mismo patrón y proyecto que saimap-plataforma) + modo invitado

## Estructura

```
saimap-idiomas/
├── index.html        ← Login + mapa del curso (árbol de módulos)
├── leccion.html      ← Reproductor de lecciones (los 5 tipos de ejercicio)
└── json/
    ├── course.json   ← Manifiesto: niveles, módulos, qué está desbloqueado
    └── a1/
        ├── mod01.json … mod05.json   ← Ejercicios por módulo
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

1. Generar B1, B2, C1 y C2 (100 módulos) con subagentes: la especificación está en
   `GENERACION_SPEC.md` y la validación en `validate_modules.py` (mismo proceso que A1/A2).
2. Sincronizar el progreso a Firestore (`users/{hash}`) para que viaje entre dispositivos.
3. Publicar en GitHub Pages (repo separado, acceso por link directo, como el resto de SAIMAP).
