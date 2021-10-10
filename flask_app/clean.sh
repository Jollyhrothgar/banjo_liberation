#!/bin/bash
# Cleans up project of all generated files.
unset FLASK_APP
unset FLASK_ENV

rm -rf build
rm -rf dist
rm -rf bl.egg-info
