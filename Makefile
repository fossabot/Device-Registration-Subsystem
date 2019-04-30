# DRS makefile.
# Copyright (c) 2018 Qualcomm Technologies, Inc.
# All rights reserved.
# Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
# * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
# THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

#
# Device Registration System Makefile
#

.PHONY: clean-pyc dist install-db start-dev, genlist-delta, genlist-full, test, lint
.EXPORT_ALL_VARIABLES:
FLASK_ENV = development
FLASK_DEBUG = True

clean: clean-pyc
	rm	-rf dist .cache migrations drs.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name *pyc | grep __pycache__ | xargs rm -rf

start-dev:
	pip3 install -r requirements.txt
	flask run -h 0.0.0.0 -p 5000

install-db:
	python3 manage.py db init
	python3 manage.py db migrate
	python3 manage.py db upgrade
	python3 manage.py seed-db
	python3 manage.py install-db

upgrade-db:
	python3 manage.py db migrate
	python3 manage.py db upgrade
	python3 manage.py install-db

dist: clean-pyc
	rm -rf dist
	python3 setup.py bdist_wheel
	cp -a etc dist/
	cp -a requirements.txt dist/
	cp -a scripts dist/
	cp -a manage.py dist/

genlist-delta:
	python3 manage.py genlist

genlist-full:
	python3 manage.py genlist --list full

test:
	pip3 install -r test_requirements.txt
	python3 setup.py develop
	py.test --verbose

lint:
	pip3 install pylint
	pylint --verbose app/* scripts/* tests/* manage.py setup.py
