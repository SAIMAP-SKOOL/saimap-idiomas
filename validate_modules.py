# -*- coding: utf-8 -*-
"""Valida los JSON de módulos de saimap-idiomas contra la especificación.

Uso:  python validate_modules.py [carpeta_json ...]
Sin argumentos valida json/a1 y json/a2.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

EXPECTED = {"match": 4, "quiz": 7, "gap": 8, "wordbank": 7, "speak": 4}
TOTAL = 30

# Curso Biblia (biblia/json/...): sin ejercicios speak
EXPECTED_BIBLIA = {"match": 4, "quiz": 9, "gap": 9, "wordbank": 8}

# Módulos subdivididos en 5 subniveles (banco más pequeño por subnivel, sesión de 10 en vez de 12)
EXPECTED_SUB = {"match": 3, "quiz": 3, "gap": 3, "wordbank": 3, "speak": 3}
TOTAL_SUB = 15
SUBLEVELS_COUNT = 5


def norm(s):
    s = s.lower()
    s = re.sub(r"[.,!?;:'\"«»“”‘’¿¡-]", "", s)
    return re.sub(r"\s+", " ", s).strip()


def validate_exercise(ex, i):
    errs = []
    t = ex.get("type")
    if t == "match":
        pairs = ex.get("pairs", [])
        if len(pairs) != 5:
            errs.append(f"[{i}] match: {len(pairs)} parejas (deben ser 5)")
        for p in pairs:
            if not p.get("en") or not p.get("es"):
                errs.append(f"[{i}] match: pareja incompleta {p}")
    elif t == "quiz":
        opts = ex.get("options", [])
        if len(opts) != 3:
            errs.append(f"[{i}] quiz: {len(opts)} opciones (deben ser 3)")
        c = ex.get("correct")
        if not isinstance(c, int) or not 0 <= c <= 2:
            errs.append(f"[{i}] quiz: correct={c} inválido")
        if not ex.get("explanation"):
            errs.append(f"[{i}] quiz: falta explanation")
    elif t == "gap":
        text = ex.get("text", "")
        if text.count("___") != 1:
            errs.append(f"[{i}] gap: el texto debe contener exactamente un ___")
        opts = ex.get("options", [])
        if len(opts) != 3:
            errs.append(f"[{i}] gap: {len(opts)} opciones (deben ser 3)")
        if ex.get("answer") not in opts:
            errs.append(f"[{i}] gap: answer «{ex.get('answer')}» no está en options")
    elif t == "wordbank":
        answer_words = norm(ex.get("answer", "")).split(" ")
        tiles = [norm(w) for w in ex.get("tiles", [])]
        pool = list(tiles)
        for w in answer_words:
            if w in pool:
                pool.remove(w)
            elif w:  # norm puede dejar fichas de solo signos como cadena vacía
                errs.append(f"[{i}] wordbank: la palabra «{w}» de answer no está en tiles")
        if len(ex.get("tiles", [])) <= len([w for w in answer_words if w]):
            errs.append(f"[{i}] wordbank: no hay distractores (tiles <= palabras de answer)")
        if not ex.get("explanation"):
            errs.append(f"[{i}] wordbank: falta explanation")
    elif t == "speak":
        if not ex.get("text"):
            errs.append(f"[{i}] speak: falta text")
        if not ex.get("es"):
            errs.append(f"[{i}] speak: falta es")
    else:
        errs.append(f"[{i}] tipo desconocido: {t}")
    return errs


def validate_exercise_list(exs, expected, total, prefix=""):
    errs = []
    if len(exs) != total:
        errs.append(f"{prefix}{len(exs)} ejercicios (deben ser {total})")
    counts = {}
    for i, ex in enumerate(exs):
        counts[ex.get("type")] = counts.get(ex.get("type"), 0) + 1
        errs.extend(f"{prefix}{e}" for e in validate_exercise(ex, i))
    for t, n in expected.items():
        if counts.get(t, 0) != n:
            errs.append(f"{prefix}distribución: {t}={counts.get(t, 0)} (esperado {n})")
    return errs


def validate_file(path):
    errs = []
    try:
        mod = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"JSON inválido: {e}"]
    for field in ("id", "module", "title", "subtitle"):
        if field not in mod:
            errs.append(f"falta el campo «{field}»")

    if "sublevels" in mod:
        sls = mod["sublevels"]
        if "exercises" in mod:
            errs.append("un módulo no puede tener a la vez «sublevels» y «exercises» de nivel superior")
        if len(sls) != SUBLEVELS_COUNT:
            errs.append(f"{len(sls)} subniveles (deben ser {SUBLEVELS_COUNT})")
        for sl in sls:
            n = sl.get("n", "?")
            for field in ("n", "title", "exercises"):
                if field not in sl:
                    errs.append(f"subnivel {n}: falta el campo «{field}»")
            errs.extend(validate_exercise_list(sl.get("exercises", []), EXPECTED_SUB, TOTAL_SUB, prefix=f"subnivel {n}: "))
    else:
        exs = mod.get("exercises")
        if exs is None:
            errs.append("falta el campo «exercises» (o «sublevels»)")
        else:
            expected = EXPECTED_BIBLIA if "biblia" in str(path).lower() else EXPECTED
            errs.extend(validate_exercise_list(exs, expected, TOTAL))
    return errs


def main():
    base = Path(__file__).parent / "json"
    dirs = [Path(a) for a in sys.argv[1:]] or [base / "a1", base / "a2"]
    total_files, bad = 0, 0
    for d in dirs:
        for f in sorted(d.glob("mod*.json")):
            total_files += 1
            errs = validate_file(f)
            if errs:
                bad += 1
                print(f"✗ {f.parent.name}/{f.name}")
                for e in errs[:12]:
                    print(f"    - {e}")
            else:
                print(f"✓ {f.parent.name}/{f.name}")
    print(f"\n{total_files - bad}/{total_files} archivos válidos")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
