#!/usr/bin/env bash

[ "v"`python3 setup.py --version` == `git describe` ]
exit $?