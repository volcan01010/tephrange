#! /bin/bash

nosetests --with-coverage \
          --cover-erase --cover-html \
          --cover-package tephrange $1 $2
