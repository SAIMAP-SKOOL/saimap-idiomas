# Especificación: conversión de un módulo plano a 5 subniveles (saimap-idiomas)

Transforma un módulo de inglés que hoy tiene el esquema plano de 30 ejercicios
(`json/a1/modXX.json`, `"exercises": [...30]`) al esquema de 5 subniveles de 15 ejercicios
cada uno. Lee primero `GENERACION_SPEC.md` (tipos de ejercicio, reglas de calidad, tono) —
esta spec solo cubre la reestructuración en subniveles.

## Esquema de salida

```json
{
  "id": "a1-modXX", "module": XX, "title": "...", "subtitle": "...",
  "sublevels": [
    { "n": 1, "title": "Nombre corto del bloque temático", "exercises": [ ...15... ] },
    { "n": 2, "title": "...", "exercises": [ ...15... ] },
    { "n": 3, "title": "...", "exercises": [ ...15... ] },
    { "n": 4, "title": "...", "exercises": [ ...15... ] },
    { "n": 5, "title": "...", "exercises": [ ...15... ] }
  ]
}
```

Sustituye por completo la clave `"exercises"` de nivel superior por `"sublevels"` (un módulo
no puede tener ambas a la vez). Cada subnivel lleva `"n"` (1-5), `"title"` (etiqueta corta en
español que se mostrará en el encabezado de la lección) y `"exercises"` con **exactamente 15**:
**3 match / 3 quiz / 3 gap / 3 wordbank / 3 speak**, tipos intercalados (no los agrupes por tipo).

## Cómo dividir el módulo en 5 bloques

1. Abre la tabla de las 30 palabras clave del `.md` fuente del módulo (`Tabla XX.1`) y divídela
   en **5 grupos de 6 palabras, en el mismo orden en que aparecen en la tabla**. Ese orden ya
   sigue la progresión pedagógica del libro (de lo básico a lo más específico), así que no hace
   falta reordenar por tu cuenta.
2. Ponle a cada subnivel un título corto que resuma su bloque temático (p. ej. «Presente simple:
   afirmativo», «Preposiciones de lugar en la casa»). Si el módulo tiene secciones numeradas en
   la teoría del `.md` (1., 2., 3.…), úsalas como guía para el título y para qué punto gramatical
   asociar a cada grupo de palabras — no hace falta que el número de secciones coincida con 5;
   lo importante es que cada subnivel tenga un foco temático reconocible.
3. **Regla de acumulación estricta:** el subnivel N solo puede usar vocabulario y estructuras de
   los subniveles 1..N de ESE módulo (nunca de un subnivel posterior). El subnivel 5 sí puede
   reutilizar libremente palabras de los subniveles 1-4 para dar variedad y funcionar como cierre
   del módulo.

## Cómo poblar los 15 ejercicios de cada subnivel

El módulo ya tiene 30 ejercicios buenos (los del archivo plano actual). No los deseches:
**reubica cada uno en el subnivel cuyo vocabulario/gramática le corresponda** (por el grupo de
palabras que usa), y completa lo que falte hasta llegar a 15 por subnivel con ejercicios nuevos
en el mismo estilo y nivel de exigencia. En total necesitarás generar unos 45 ejercicios nuevos
por módulo (30 reubicados + 45 nuevos = 75).

Al escribir los nuevos:
- Seguí usando exclusivamente contenido real del `.md` (vocabulario, ejemplos de la teoría,
  tablas de contraste y de errores comunes, preguntas de examen) — no inventes gramática ajena
  al módulo.
- **`match`**: 3 tarjetas de 5 parejas cada una, usando las 6 palabras del grupo del subnivel
  (rota cuál de las 6 omites en cada tarjeta para dar variedad sin repetir exactamente la misma
  tarjeta tres veces). Los subniveles 3+ pueden mezclar palabras propias con palabras de
  subniveles anteriores en la misma tarjeta (refuerzo acumulativo).
- **`quiz`**: enunciado y opciones **siempre de uso práctico** (traducir, elegir la frase
  correcta, completar una situación comunicativa) — nunca preguntes por la etiqueta gramatical
  de algo («¿qué caso/tiempo/función es X?»); eso ya se explica en `hint`/`explanation`. Varía
  el índice `correct` (0/1/2) entre los 3 quiz del subnivel: no lo dejes fijo en la misma
  posición las tres veces.
- **`gap`** y **`wordbank`**: igual que siempre — practican la gramática del bloque (huecos con
  3 opciones y frases para construir con banco de palabras + distractores plausibles).
- **`speak`**: frases cortas naturales del vocabulario ya visto hasta ese subnivel.

## Validación

Actualiza también la entrada del módulo en `D:\Usuario\SAIMAP\IDIOMAS\saimap-idiomas\json\course.json`
añadiéndole `"sublevels": 5` (junto a `"file"`), si no lo tiene ya. Al terminar, ejecuta desde
`D:\Usuario\SAIMAP\IDIOMAS\saimap-idiomas`:

```
python validate_modules.py json/a1
```

y corrige cualquier error en tus archivos hasta que salgan válidos (el validador reconoce
automáticamente el esquema de subniveles: exige 5 subniveles de 15 ejercicios con distribución
3/3/3/3/3 cada uno).
