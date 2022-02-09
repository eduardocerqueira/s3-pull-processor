#!/bin/bash

# prepare development environment
# how to run: sh ops/scripts/install.sh

source $(dirname "$0")/lib.sh

default_dir="$(pwd)"
venv_dir="$default_dir/venv"

main() {
  print_header "Preparing python virtual environment"
  python3 -m venv "$venv_dir" >/dev/null 2>&1
  print_check "venv initialization $venv_dir"
  $venv_dir/bin/pip install --upgrade pip >/dev/null 2>&1
  print_check "pip upgrade"
  $venv_dir/bin/pip install devpi-client setuptools_scm >/dev/null 2>&1
  print_check "pip install devpi-client setuptools_scm"

  # install
  echo -e "      ... installing s3-pull-processor"
  $venv_dir/bin/pip install --editable . >/dev/null 2>&1
  print_check "s3-pull-processor installation"

  # check
  $venv_dir/bin/s3-pull-processor --help >/dev/null 2>&1
  print_check "s3-pull-processor check"
}

# main
main
