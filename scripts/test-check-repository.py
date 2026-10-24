"""Exercise the shell guardrails against isolated repositories, without Jenkins."""

import shutil
import os
import re
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
                      empty_pipelines=False, pipeline_note=False, helper_script=None,
                      commented_guardrail=None, checkout_option="skipDefaultCheckout(true)"):
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
                    "    // " + value if value == commented_guardrail else
                    checkout_option if value == "skipDefaultCheckout(true)" else value
                    for value in GUARDRAILS if value != missing_guardrail
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

    def test_disabled_checkout_option_fails_even_when_its_name_is_present(self):
        result = self.check_fixture(checkout_option="skipDefaultCheckout(false)")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertIn("Implicit checkout must be disabled: pipelines/example/Jenkinsfile", result.stderr)

    def test_enabled_checkout_option_accepts_default_and_explicit_true(self):
        for option in ("skipDefaultCheckout()", "skipDefaultCheckout( true )"):
            with self.subTest(option=option):
                result = self.check_fixture(checkout_option=option)
                self.assertEqual(0, result.returncode, result.stderr)

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

    def test_full_line_comments_cannot_satisfy_any_required_guardrail(self):
        for guardrail in GUARDRAILS:
            with self.subTest(guardrail=guardrail):
                result = self.check_fixture(commented_guardrail=guardrail)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("Missing required structure or guardrail", result.stderr)
                self.assertIn("pipelines/example/Jenkinsfile", result.stderr)

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


class DockerPushShellTests(unittest.TestCase):
    def test_build_rejects_missing_configuration_and_preserves_docker_failure(self):
        source = (SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile").read_text(encoding="utf-8")
        build = source.split("stage('Build Docker Image')", 1)[1].split("stage('Inspect Image')", 1)[0]
        command = re.search(r"sh '''(.*?)'''", build, re.DOTALL).group(1)
        for variable in ("GIT_COMMIT", "IMAGE_NAME", "IMAGE_TAG", None):
            for unset in (False, True):
                with self.subTest(variable=variable, unset=unset), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    harness = root / "build.sh"
                    harness.write_text('docker() { echo called > calls.txt; return 7; }\n' + command,
                                       encoding="utf-8")
                    environment = dict(os.environ, GIT_COMMIT="abc123", IMAGE_NAME="fixture/image", IMAGE_TAG="42")
                    if variable:
                        if unset:
                            environment.pop(variable)
                        else:
                            environment[variable] = ""
                    result = subprocess.run([BASH, harness.as_posix()], cwd=root, env=environment,
                                            capture_output=True, text=True, timeout=10)
                    if variable:
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(variable + " must be set", result.stderr)
                        self.assertFalse((root / "calls.txt").exists())
                    else:
                        self.assertEqual(7, result.returncode, result.stderr)
                        self.assertTrue((root / "calls.txt").exists())

    def test_inspection_rejects_incomplete_configuration_before_docker_and_preserves_docker_failure(self):
        source = (SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile").read_text(encoding="utf-8")
        inspection = source.split("stage('Inspect Image')", 1)[1].split("stage('Push Docker Image')", 1)[0]
        command = re.search(r"sh '''(.*?)'''", inspection, re.DOTALL).group(1)
        for variable in ("GIT_COMMIT", "IMAGE_NAME", "IMAGE_TAG", None):
            for unset in (False, True):
                with self.subTest(variable=variable, unset=unset), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    harness = root / "inspect.sh"
                    harness.write_text('docker() { echo called > calls.txt; return 7; }\n' + command,
                                       encoding="utf-8")
                    environment = dict(os.environ, GIT_COMMIT="abc123", IMAGE_NAME="fixture/image", IMAGE_TAG="42")
                    if variable:
                        if unset:
                            environment.pop(variable)
                        else:
                            environment[variable] = ""
                    result = subprocess.run([BASH, harness.as_posix()], cwd=root, env=environment,
                                            capture_output=True, text=True, timeout=10)
                    if variable:
                        self.assertNotEqual(0, result.returncode)
                        self.assertIn(variable + " must be set", result.stderr)
                        self.assertFalse((root / "calls.txt").exists())
                    else:
                        self.assertEqual(7, result.returncode, result.stderr)
                        self.assertTrue((root / "calls.txt").exists())
                        self.assertNotIn("Image revision does not match", result.stderr)

    def test_image_inspection_requires_matching_source_revision_before_push(self):
        source = (SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile").read_text(encoding="utf-8")
        inspection = source.split("stage('Inspect Image')", 1)[1].split("stage('Push Docker Image')", 1)[0]
        command = re.search(r"sh '''(.*?)'''", inspection, re.DOTALL).group(1)
        for revision, expected_status in (("abc123", 0), ("other-commit", 1), ("", 1), ("<no value>", 1)):
            with self.subTest(revision=revision), tempfile.TemporaryDirectory(prefix="jenkins-inspect-") as temporary:
                root = Path(temporary)
                harness = root / "inspect.sh"
                harness.write_text('docker() { printf "%s\\n" "$@" > arguments.txt; '
                                   'printf "%s" "$FIXTURE_REVISION"; }\n' + command, encoding="utf-8")
                result = subprocess.run([BASH, harness.as_posix()], cwd=root,
                                        env=dict(os.environ, GIT_COMMIT="abc123", FIXTURE_REVISION=revision,
                                                 IMAGE_NAME="fixture/image", IMAGE_TAG="42"),
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(expected_status, result.returncode, result.stderr)
                self.assertEqual(["image", "inspect", "--format",
                                  '{{ index .Config.Labels "org.opencontainers.image.revision" }}',
                                  "fixture/image:42"],
                                 (root / "arguments.txt").read_text(encoding="utf-8").splitlines())
                if expected_status:
                    self.assertIn("Image revision does not match", result.stderr)

    def test_image_build_records_the_checked_out_commit_as_an_oci_label(self):
        source = (SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile").read_text(encoding="utf-8")
        build = source.split("stage('Build Docker Image')", 1)[1].split("stage('Inspect Image')", 1)[0]
        command = re.search(r"sh '''(.*?)'''", build, re.DOTALL).group(1)
        with tempfile.TemporaryDirectory(prefix="jenkins-docker-build-") as temporary:
            root = Path(temporary)
            harness = root / "build.sh"
            harness.write_text('docker() { printf "%s\\n" "$@" > arguments.txt; }\n' + command,
                               encoding="utf-8")
            revision = "abc123def456"
            result = subprocess.run([BASH, harness.as_posix()], cwd=root,
                                    env=dict(os.environ, GIT_COMMIT=revision,
                                             IMAGE_NAME="fixture/image", IMAGE_TAG="42"),
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual(["build", "--label", "org.opencontainers.image.revision=" + revision,
                              "-t", "fixture/image:42", "."],
                             (root / "arguments.txt").read_text(encoding="utf-8").splitlines())

    def test_registry_configuration_is_scoped_to_the_push_workspace(self):
        source = (SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile").read_text(encoding="utf-8")
        self.assertIn('withEnv(["DOCKER_CONFIG=${pwd(tmp: true)}/docker-config"])', source)
        self.assertNotIn("sh 'docker logout || true'", source)

    def test_verified_jars_are_required_and_fingerprinted_before_image_build(self):
        source = (SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile").read_text(encoding="utf-8")
        application = source.split("stage('Build Application')", 1)[1].split("stage('Build Docker Image')", 1)[0]
        self.assertIn("./mvnw -B --no-transfer-progress verify", application)
        self.assertRegex(application, r"success\s*\{\s*archiveArtifacts artifacts: 'target/\*\.jar', "
                                     r"fingerprint: true, allowEmptyArchive: false")

    def run_push(self, login_status, password="fixture-password", push_status=0, logout_status=0,
                 invalid_variable=None, unset=False, xtrace=False):
        pipeline = SCRIPT.parent.parent / "pipelines/docker-image/Jenkinsfile"
        source = pipeline.read_text(encoding="utf-8")
        blocks = re.findall(r"sh '''(.*?)'''", source, re.DOTALL)
        push_blocks = [block for block in blocks if "docker login" in block]
        self.assertEqual(1, len(push_blocks), "Expected one registry login shell block")
        with tempfile.TemporaryDirectory(prefix="jenkins-docker-push-") as temporary:
            root = Path(temporary)
            # Shell function shadows Docker: no registry, credentials or daemon needed.
            harness = root / "push.sh"
            harness.write_text('''docker() {
  [ "$DOCKER_CONFIG" = "$EXPECTED_DOCKER_CONFIG" ] || return 90
  printf '%s\\n' "$1" >> calls.txt
  if [ "$1" = login ]; then
    cat >password.txt
    return "$LOGIN_STATUS"
  fi
  if [ "$1" = push ]; then return "$PUSH_STATUS"; fi
  if [ "$1" = logout ]; then return "$LOGOUT_STATUS"; fi
  return 0
}
''' + push_blocks[0], encoding="utf-8")
            environment = dict(os.environ, LOGIN_STATUS=str(login_status),
                               PUSH_STATUS=str(push_status), LOGOUT_STATUS=str(logout_status),
                               DOCKER_CONFIG=str(root / "docker-config"),
                               EXPECTED_DOCKER_CONFIG=str(root / "docker-config"),
                               REGISTRY_PASSWORD=password, REGISTRY_USERNAME="fixture-user",
                               IMAGE_NAME="fixture/image", IMAGE_TAG="42")
            if invalid_variable:
                if unset:
                    environment.pop(invalid_variable, None)
                else:
                    environment[invalid_variable] = ""
            result = subprocess.run([BASH, *(["-x"] if xtrace else []), harness.as_posix()], cwd=root, env=environment,
                                    capture_output=True, text=True, timeout=10)
            if invalid_variable:
                self.assertNotEqual(0, result.returncode)
                self.assertIn(invalid_variable + " must be set", result.stderr)
                self.assertFalse((root / "calls.txt").exists(), "Docker must not run with incomplete configuration")
                self.assertNotIn(password, result.stdout + result.stderr)
                return result, []
            calls = (root / "calls.txt").read_text(encoding="utf-8").splitlines()
            self.assertEqual(password.encode("utf-8"), (root / "password.txt").read_bytes())
            self.assertNotIn(password, result.stdout + result.stderr)
            return result, calls

    def test_missing_registry_workspace_stops_before_login_push_or_logout(self):
        for unset in (False, True):
            with self.subTest(unset=unset):
                self.run_push(0, invalid_variable="DOCKER_CONFIG", unset=unset)

    def test_inherited_shell_tracing_cannot_expose_registry_password(self):
        for login_status in (0, 7):
            with self.subTest(login_status=login_status):
                result, calls = self.run_push(login_status, password="private-registry-secret", xtrace=True)
                self.assertEqual(login_status, result.returncode, result.stderr)
                self.assertEqual(["login", "push", "logout"] if login_status == 0 else ["login", "logout"], calls)

    def test_missing_or_empty_configuration_stops_before_any_docker_call(self):
        for variable in ("IMAGE_NAME", "IMAGE_TAG", "REGISTRY_USERNAME", "REGISTRY_PASSWORD"):
            for unset in (False, True):
                with self.subTest(variable=variable, unset=unset):
                    self.run_push(0, invalid_variable=variable, unset=unset)

    def test_failed_login_stops_before_push(self):
        result, calls = self.run_push(7)
        self.assertEqual(7, result.returncode, result.stderr)
        self.assertEqual(["login", "logout"], calls)

    def test_successful_login_allows_one_push(self):
        result, calls = self.run_push(0)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["login", "push", "logout"], calls)

    def test_failed_push_logs_out_and_preserves_the_push_exit_code(self):
        result, calls = self.run_push(0, push_status=8, logout_status=9)
        self.assertEqual(8, result.returncode, result.stderr)
        self.assertEqual(["login", "push", "logout"], calls)

    def test_logout_failure_does_not_turn_a_successful_push_into_failure(self):
        result, calls = self.run_push(0, logout_status=9)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(["login", "push", "logout"], calls)

    def test_password_is_forwarded_literally_without_echo_option_or_escape_handling(self):
        for password in ("-n", r"fixture\cpassword", "fixture%spassword", "fixture\npassword"):
            with self.subTest(password=password):
                result, calls = self.run_push(0, password)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertEqual(["login", "push", "logout"], calls)


if __name__ == "__main__":
    unittest.main(verbosity=2)
