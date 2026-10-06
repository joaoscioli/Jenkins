"""Exercise the shell guardrails against isolated repositories, without Jenkins."""

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().with_name("check-repository.sh")
BASH = shutil.which("bash")
GUARDRAILS = (
    "pipeline {", "agent any", "stages {", "timeout(time: 5)",
    "skipDefaultCheckout(true)", "disableConcurrentBuilds()", "checkout scm",
)
DOCUMENTS = (
    "README.md", "docs/jenkins-fundamentals.md",
    "docs/pipeline-review-checklist.md", "docs/troubleshooting.md",
)


class RepositoryGuardrailTests(unittest.TestCase):
    def check_fixture(self, missing_guardrail=None, missing_document=None, missing_pipeline=False):
        with tempfile.TemporaryDirectory(prefix="jenkins-guardrails-") as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            shutil.copyfile(SCRIPT, root / "scripts/check-repository.sh")
            pipeline = root / "pipelines/example/Jenkinsfile"
            pipeline.parent.mkdir(parents=True)
            pipeline.write_text("\n".join(
                value for value in GUARDRAILS if value != missing_guardrail
            ), encoding="utf-8")
            for document in DOCUMENTS:
                if document != missing_document:
                    path = root / document
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("Fixture\n", encoding="utf-8")
            if missing_pipeline:
                (root / "pipelines/new-example").mkdir()
            # Deliberately run outside the fixture root to exercise path resolution.
            if BASH is None:
                self.fail("Bash must be installed and available on PATH")
            return subprocess.run(
                [BASH, (root / "scripts/check-repository.sh").as_posix()],
                cwd=SCRIPT.parent, capture_output=True, text=True, timeout=10,
            )

    def test_complete_repository_passes_from_another_directory(self):
        result = self.check_fixture()
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("guardrails passed", result.stdout)

    def test_every_missing_guardrail_fails_with_the_file_and_rule(self):
        for guardrail in GUARDRAILS:
            with self.subTest(guardrail=guardrail):
                result = self.check_fixture(missing_guardrail=guardrail)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("Missing required structure or guardrail", result.stderr)
                pattern = guardrail.split("(")[0] + "(" if "(" in guardrail else guardrail.split("any")[0].strip()
                self.assertIn(pattern, result.stderr)
                self.assertIn("pipelines/example/Jenkinsfile", result.stderr)

    def test_every_missing_core_document_fails_with_its_path(self):
        for document in DOCUMENTS:
            with self.subTest(document=document):
                result = self.check_fixture(missing_document=document)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("Missing core documentation: " + document, result.stderr)

    def test_new_pipeline_directory_requires_a_jenkinsfile(self):
        result = self.check_fixture(missing_pipeline=True)
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("Missing Jenkinsfile: pipelines/new-example/Jenkinsfile", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
