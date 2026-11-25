"""Content math, standalone build, and validation checks (standard library)."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    path = ROOT / "aprender-calculo" / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


builder = module("build_lesson")
example = module("example_riemann")


class LessonTests(unittest.TestCase):
    def setUp(self):
        self.lesson = example.lesson()

    def test_all_ten_answers_against_independent_calculations(self):
        selected = [q["options"][q["correct"]] for q in self.lesson["exercises"]]
        self.assertEqual(float(selected[0]), (6-0)/3)
        self.assertEqual(float(selected[1]), sum(5 for _ in range(4)))
        self.assertEqual(float(selected[2]), sum(i for i in range(1, 4)))
        self.assertEqual(float(selected[3]), sum(i for i in range(3)))
        self.assertEqual(float(selected[4]), sum(i*i for i in [1, 2]))
        self.assertEqual(float(selected[5].replace(",", ".")), sum(i*i for i in [0.5, 1.5]))
        self.assertEqual(selected[6], "Queda por encima del área exacta")
        self.assertEqual(float(selected[7].split()[0]), sum((t+2)*2 for t in [2, 4]))
        self.assertEqual(selected[8], "A la integral, 8/3")
        self.assertEqual(float(selected[9].replace("−", "-")), sum(-2 for _ in range(3)))
        # Check convergence independently using the sum-of-squares closed form.
        for n in [1, 2, 4, 12, 40]:
            _, area = example.plot(n)
            closed_form = (2/n)**3 * n*(n+1)*(2*n+1)/6
            self.assertAlmostEqual(area, closed_form)
            self.assertGreater(area, 8/3)
        self.assertLess(example.plot(40)[1]-8/3, example.plot(2)[1]-8/3)

    def test_build_embeds_content_without_external_assets_or_script_breakout(self):
        self.lesson["subtitle"] = '</script><script>alert("x")</script>'
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "lesson.json"
            source.write_text(json.dumps(self.lesson), encoding="utf-8")
            result = builder.build(source, Path(folder) / "nested" / "lesson.html")
            html = result.read_text(encoding="utf-8")
        self.assertNotIn('__LESSON_JSON__', html)
        self.assertNotIn(self.lesson["subtitle"], html)
        embedded = re.search(r'<script id="lesson-data" type="application/json">(.*?)</script>', html, re.S)[1]
        self.assertEqual(json.loads(embedded)["subtitle"], self.lesson["subtitle"])
        self.assertFalse(re.search(r'<(?:script|link|img)\b[^>]*(?:src|href)\s*=', html))

    def test_invalid_lesson_is_rejected(self):
        mutations = [
            lambda x: x["exercises"].pop(),
            lambda x: x["exercises"][0].update(correct=20),
            lambda x: x["exercises"][0]["feedback"].pop(),
            lambda x: x["exercises"][0].update(id="e2"),
            lambda x: x["training"][0]["steps"][0].update(options=["1", "1", "2"]),
        ]
        for mutation in mutations:
            candidate = copy.deepcopy(self.lesson)
            mutation(candidate)
            with self.assertRaises(ValueError):
                builder.validate(candidate)

    def test_active_or_external_svg_is_rejected(self):
        payloads = [
            '<script>alert(1)</script>',
            '<rect onclick="alert(1)"/>',
            '<image href="https://example.com/a.png"/>',
            '<rect fill="url(https://example.com/a)"/>',
            '<foreignObject><div>HTML</div></foreignObject>',
            '<rect style="fill:red"/>',
        ]
        for payload in payloads:
            candidate = copy.deepcopy(self.lesson)
            candidate["tutorial"][0]["svg"] = f'<svg viewBox="0 0 600 300">{payload}</svg>'
            with self.assertRaises(ValueError):
                builder.validate(candidate)

    def test_new_topic_is_not_hardcoded_in_template(self):
        self.lesson["id"] = "otro-tema"
        self.lesson["title"] = "Límites"
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "lesson.json"
            source.write_text(json.dumps(self.lesson), encoding="utf-8")
            output = builder.build(source, Path(folder) / "lesson.html").read_text(encoding="utf-8")
        data = json.loads(re.search(r'<script id="lesson-data" type="application/json">(.*?)</script>', output, re.S)[1])
        self.assertEqual(data["title"], "Límites")
        template = (ROOT / "aprender-calculo" / "assets" / "lesson.html").read_text(encoding="utf-8")
        self.assertNotIn("Riemann", template)


if __name__ == "__main__":
    unittest.main()
