#!/bin/bash

# common library

# terminal color
color_default="\e[39m"
color_error="\e[31m"
color_ok="\e[32m"
color_header="\e[34m"

# functions
print_header() {
  echo
  echo -e "--$color_header $1 $color_default"
}

print_check() {
  status=$?
  if [ $status -eq 0 ]
  then
    echo -e "[$color_ok v $color_default] $1"
  else
    echo -e "[$color_error x $color_default] $1"
  fi
}
