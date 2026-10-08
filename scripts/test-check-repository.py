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
    def check_fixture(self, missing_guardrail=None, missing_document=None, missing_pipeline=False,
                      empty_pipelines=False, pipeline_note=False, helper_script=None):
        with tempfile.TemporaryDirectory(prefix="jenkins-guardrails-") as temporary:
            root = Path(temporary)
            (root / "scripts").mkdir()
            shutil.copyfile(SCRIPT, root / "scripts/check-repository.sh")
            if helper_script is not None:
                (root / "scripts/helper.sh").write_text(helper_script, encoding="utf-8")
            pipeline = root / "pipelines/example/Jenkinsfile"
            (root / "pipelines").mkdir()
            if not empty_pipelines:
                pipeline.parent.mkdir(parents=True)
                pipeline.write_text("\n".join(
                    value for value in GUARDRAILS if value != missing_guardrail
                ), encoding="utf-8")
            if pipeline_note:
                (root / "pipelines/README.md").write_text("Pipeline index\n", encoding="utf-8")
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

    def test_invalid_helper_shell_syntax_fails_with_its_path(self):
        result = self.check_fixture(helper_script="if true; then\necho incomplete\n")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("Invalid Bash syntax: scripts/helper.sh", result.stderr)

    def test_valid_helper_is_parsed_without_executing_it(self):
        result = self.check_fixture(helper_script="#!/usr/bin/env bash\nexit 42\n")
        self.assertEqual(0, result.returncode, result.stderr)

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

    def test_regular_files_in_pipeline_directory_are_not_examples(self):
        result = self.check_fixture(pipeline_note=True)
        self.assertEqual(0, result.returncode, result.stderr)

    def test_empty_pipeline_directory_fails_with_actionable_message(self):
        for pipeline_note in (False, True):
            with self.subTest(pipeline_note=pipeline_note):
                result = self.check_fixture(empty_pipelines=True, pipeline_note=pipeline_note)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("No pipeline examples found under pipelines/.", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
