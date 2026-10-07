#!/usr/bin/env bash
set -euo pipefail

# Resolve paths from the script so local and CI checks use the same repository.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

shopt -s nullglob
pipeline_count=0
for directory in pipelines/*; do
  [[ -d "$directory" ]] || continue
  pipeline_count=$((pipeline_count + 1))
  file="$directory/Jenkinsfile"
  if [[ ! -f "$file" ]]; then
    echo "Missing Jenkinsfile: $file" >&2
    exit 1
  fi
  for pattern in 'pipeline {' 'agent ' 'stages {' 'timeout(' \
                 'skipDefaultCheckout(' 'disableConcurrentBuilds(' 'checkout scm'; do
    if ! grep -Fq "$pattern" "$file"; then
      echo "Missing required structure or guardrail '$pattern': $file" >&2
      exit 1
    fi
  done
done

if [[ "$pipeline_count" -eq 0 ]]; then
  echo 'No pipeline examples found under pipelines/.' >&2
  exit 1
fi

for file in README.md docs/jenkins-fundamentals.md \
            docs/pipeline-review-checklist.md docs/troubleshooting.md; do
  if [[ ! -f "$file" ]]; then
    echo "Missing core documentation: $file" >&2
    exit 1
  fi
done

echo 'Repository structure and pipeline guardrails passed.'
