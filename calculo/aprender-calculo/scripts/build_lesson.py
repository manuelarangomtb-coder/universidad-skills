#!/usr/bin/env python3
"""Validate a lesson and embed it in a standalone, offline HTML file."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text_field(obj, key, where):
    require(isinstance(obj, dict), f"{where}: se esperaba un objeto")
    value = obj.get(key)
    require(isinstance(value, str) and value.strip(), f"{where}.{key}: falta texto")


def items(obj, key, low, high, where):
    value = obj.get(key)
    require(isinstance(value, list) and low <= len(value) <= high,
            f"{where}.{key}: se esperan entre {low} y {high} elementos")
    return value


def illustration(obj, where):
    text_field(obj, "svg", where)
    text_field(obj, "alt", where)
    raw = obj["svg"]
    require("<!" not in raw and "<?" not in raw, f"{where}: SVG sin declaraciones ni entidades")
    root = ET.fromstring(raw)
    allowed_tags = {"svg", "g", "path", "rect", "circle", "ellipse", "line", "polyline",
                    "polygon", "text", "tspan", "title", "desc", "defs", "linearGradient",
                    "radialGradient", "stop", "clipPath", "marker"}
    require(root.tag.rsplit("}", 1)[-1] == "svg" and "viewBox" in root.attrib,
            f"{where}: SVG necesita viewBox")
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        require(tag in allowed_tags, f"{where}: elemento SVG no permitido: {tag}")
        for attr, value in element.attrib.items():
            attr = attr.rsplit("}", 1)[-1].lower()
            require(not attr.startswith("on") and attr not in {"href", "src", "style"},
                    f"{where}: atributo SVG activo: {attr}")
            normalized = re.sub(r"\s+", "", value).lower()
            require(not any(token in normalized for token in ["javascript:", "data:", "https:", "http:", "//", "\\"]),
                    f"{where}: referencia externa o activa")
            for target in re.findall(r"url\((.*?)\)", normalized):
                require(bool(re.fullmatch(r"#[a-zA-Z0-9_-]+", target)),
                        f"{where}: solo se permiten referencias SVG internas")


def question(obj, where, step=False):
    for key in ["title", "prompt"] + (["explanation"] if step else ["id", "concept"]):
        text_field(obj, key, where)
    options = items(obj, "options", 3, 5, where)
    require(all(isinstance(x, str) and x.strip() for x in options), f"{where}: opciones vacías")
    require(len(set(x.strip() for x in options)) == len(options), f"{where}: opciones duplicadas")
    correct = obj.get("correct")
    require(type(correct) is int and 0 <= correct < len(options), f"{where}: índice correcto inválido")
    feedback = items(obj, "feedback", len(options), len(options), where)
    require(all(isinstance(x, str) and x.strip() for x in feedback), f"{where}: falta retroalimentación")
    if "calculation" in obj:
        text_field(obj, "calculation", where)


def validate(lesson):
    for key in ["id", "title", "subtitle", "objective", "prerequisites", "takeaway"]:
        text_field(lesson, key, "leccion")
    for i, card in enumerate(items(lesson, "tutorial", 3, 5, "leccion")):
        for key in ["title", "body"]:
            text_field(card, key, f"tutorial[{i}]")
        if "formula" in card:
            text_field(card, "formula", f"tutorial[{i}]")
        illustration(card, f"tutorial[{i}]")
    sim = lesson.get("simulation")
    for key in ["title", "intro", "controlLabel", "question"]:
        text_field(sim, key, "simulation")
    for i, frame in enumerate(items(sim, "frames", 12, 60, "simulation")):
        for key in ["label", "description"]:
            text_field(frame, key, f"frames[{i}]")
        illustration(frame, f"frames[{i}]")
        for metric in items(frame, "metrics", 1, 4, f"frames[{i}]"):
            for key in ["label", "value"]:
                text_field(metric, key, "metric")
    for app in items(lesson, "applications", 1, 2, "leccion"):
        for key in ["title", "body"]:
            text_field(app, key, "application")
    for i, example in enumerate(items(lesson, "training", 3, 3, "leccion")):
        for key in ["title", "prompt"]:
            text_field(example, key, f"training[{i}]")
        for j, step in enumerate(items(example, "steps", 2, 8, f"training[{i}]")):
            question(step, f"training[{i}].steps[{j}]", step=True)
    ids = []
    for i, exercise in enumerate(items(lesson, "exercises", 10, 10, "leccion")):
        question(exercise, f"exercises[{i}]")
        ids.append(exercise["id"])
        for j, step in enumerate(items(exercise, "steps", 2, 8, f"exercises[{i}]")):
            question(step, f"exercises[{i}].steps[{j}]", step=True)
    require(len(set(ids)) == 10, "Los diez ejercicios necesitan identificadores distintos")


def build(source, output):
    lesson = json.loads(Path(source).read_text(encoding="utf-8"))
    validate(lesson)
    data = json.dumps(lesson, ensure_ascii=False, sort_keys=True)
    version = hashlib.sha256(data.encode()).hexdigest()[:16]
    # Prevent lesson strings from closing their JSON script element.
    data = data.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    template = (Path(__file__).resolve().parents[1] / "assets" / "lesson.html").read_text(encoding="utf-8")
    require(template.count("__LESSON_JSON__") == 1, "Marcador JSON de plantilla inválido")
    html = template.replace("__LESSON_JSON__", data).replace("__LESSON_VERSION__", version)
    target = Path(output)
    require(target.resolve() != Path(source).resolve(), "La salida HTML no puede sobrescribir el JSON de origen")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="JSON de la lección")
    parser.add_argument("--output", required=True, help="HTML autónomo de salida")
    args = parser.parse_args()
    try:
        result = build(args.source, args.output)
    except (ValueError, TypeError, OSError, ET.ParseError) as exc:
        parser.exit(1, f"No se pudo construir la lección: {exc}\n")
    print(result.resolve())


if __name__ == "__main__":
    main()
