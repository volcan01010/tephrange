#! /bin/bash

nosetests --with-coverage \
          --cover-erase --cover-html \
          --cover-package travdist $1 $2
