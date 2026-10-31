#!/usr/bin/env bash
set -euo pipefail

# Resolve paths from the script so local and CI checks use the same repository.
cd "$(dirname "${BASH_SOURCE[0]}")/.."

shopt -s nullglob
for script in scripts/*.sh; do
  if ! bash -n "$script"; then
    echo "Invalid Bash syntax: $script" >&2
    exit 1
  fi
done

pipeline_count=0
for directory in pipelines/*; do
  [[ -d "$directory" ]] || continue
  pipeline_count=$((pipeline_count + 1))
  file="$directory/Jenkinsfile"
  if [[ ! -f "$file" ]]; then
    echo "Missing Jenkinsfile: $file" >&2
    exit 1
  fi
  # A disabled guardrail in a full-line Groovy comment must not satisfy the gate.
  active_lines=$(sed '/^[[:space:]]*\/\//d' "$file")
  for pattern in 'pipeline {' 'agent ' 'stages {' 'timeout(' \
                 'skipDefaultCheckout(' 'disableConcurrentBuilds(' 'checkout scm'; do
    if ! grep -Fq "$pattern" <<< "$active_lines"; then
      echo "Missing required structure or guardrail '$pattern': $file" >&2
      exit 1
    fi
  done
  # Keep this intentionally narrow: examples use a positive literal time first.
  if ! grep -Eq 'timeout\([[:space:]]*time[[:space:]]*:[[:space:]]*[1-9][0-9]*[[:space:]]*[,)]' <<< "$active_lines"; then
    echo "Timeout must start with a positive integer time: $file" >&2
    exit 1
  fi
  if ! grep -Eq 'skipDefaultCheckout\([[:space:]]*(true[[:space:]]*)?\)' <<< "$active_lines"; then
    echo "Implicit checkout must be disabled: $file" >&2
    exit 1
  fi
  if ! grep -Eq 'disableConcurrentBuilds\([[:space:]]*(abortPrevious[[:space:]]*:[[:space:]]*false[[:space:]]*)?\)' <<< "$active_lines"; then
    echo "Concurrent builds must queue without aborting the active build: $file" >&2
    exit 1
  fi
  # Examples use canonical literal TimeUnit names; dynamic units need native validation.
  if grep -Eq "timeout\([^)]*unit[[:space:]]*:" <<< "$active_lines" &&
     ! grep -Eq "timeout\([^)]*unit[[:space:]]*:[[:space:]]*'(NANOSECONDS|MICROSECONDS|MILLISECONDS|SECONDS|MINUTES|HOURS|DAYS)'[[:space:]]*\)" <<< "$active_lines"; then
    echo "Timeout unit must be a supported literal TimeUnit: $file" >&2
    exit 1
  fi
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
