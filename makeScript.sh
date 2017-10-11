#!/bin/bash
set -e
rm env -rf
python3 -m virtualenv env
. ./env/bin/activate
pip install praw
