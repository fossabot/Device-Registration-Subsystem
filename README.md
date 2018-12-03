SPDX-License-Identifier: BSD-3-Clause-Clear

Copyright (c) 2018 Qualcomm Technologies, Inc.

All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the limitations in the disclaimer below) provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
## DRS-Device Registration Sub-System
Device Registration Sub-System is a part of the Device Identification, Registration and Blocking (DIRBS) System.
It used to comply type approval of imported/exported devices.

#### Directory structure
This repository contains code for **DRS** part of the **DIRBS**. It contains
* ``app/`` -- The DRS core server app, to be used as DRS Web Server including database models, apis and resources
* ``etc/`` -- Config files etc to be reside here
* ``mock/`` -- Sample data files etc which are used in app to be reside here
* ``scripts/`` -- Database migration, list generation scripts etc
* ``tests/`` -- Unit test scripts and Data

#### Prerequisites
In order to run a development environment, [Python 3.0+](https://www.python.org/download/releases/3.0/) and 
[Postgresql10](https://www.postgresql.org/about/news/1786/) we assume that these are installed.

We also assume that this repo is cloned from Github onto the local computer, it is assumed that 
all commands mentioned in this guide are run from root directory of the project and inside
```virtual environment```

On Windows, we assume that a Bash like shell is available (i.e Bash under Cygwin), with GNU make installed.

#### Starting a dev environment
The easiest and quickest way to get started is to use local-only environment (i.e everything runs locally, including
Postgresql Server). To setup the local environment, follow the section below:

##### Setting up local dev environment
For setting up a local dev environment we assume that the ```prerequisites``` are met already. To setup a local 
environment:
* Create database using Postgresql (Name and credentials should be same as in [config](mock/test-config.ini))
* Create virtual environment using **virtualenv** and activate it:
```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
Make sure that virtual-env is made using Python3 and all the required dependencies are installed.
* Run Database migrations using:
```bash
make install-db
```
This will automatically create and migrate database schemas and requirements.

* Start DRS development server using:
```bash
make start-dev
```
This will start a flask development environment for DRS.

* To run unit tests, run:
```bash
make test
```

* To lint the code using pylint, simply run:
```bash
make lint
```
---

#### Starting Dockerized Dev Environment
**Make sure you have installed [docker](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/).**

1. Build Dev Server using:
```bash
make -f docker/dev/Makefile
```
2. Build Postgres Server using:
```bash
make -f docker/postgres/Makefile
```
3. After the build process for both images is successful launch dev environment using docker-compose:
```bash
docker-compose -f docker/compose/devenv-local-db.yml run --rm --service-ports dev-shell
```
It will launch container for development server and for postgres (drs_db) and login you to the shell
of the development server.

4. Now open another terminal and login into the postgres shell:
```bash
docker exec -it drs_db bash
```

5. Checkout into the postgres shell:
```bash
gosu postgres psql
```

6. On the postgres shell, create a role **drs** with login:
```bash
CREATE ROLE drs WITH login;
```

7. On the postgres shell, create database named **drs**:
```bash
CREATE database drs OWNER drs;
```

8. Now switch to the server shell, and install database:
```bash
make install-db
```

After these steps are completed successfully, you can run test or start development server etc on the shell.

---


#### Bumping version number
We follow [Semantic Versioning](http://semver.org/) for DRS.
To change the releases number simply edit ```app/metadata.py``` and pump the version number.

---

#### Other Helpful Commands

To clean the extra and un-necessary directories in the project:
```bash
make clean
```

To clean the python compiled files from the project:
```bash
make clean-pyc
```

To install a fresh database:
```bash
make install-db
```

To Upgrade already installed database:
```bash
make upgrade-db
```
To configure
To create distribution files:
```bash
make dist
```

To generate full registration list for DIRBS Core:
```bash
make genlist-full
```

To generate delta registration list for DIRBS Core:
```bash
make genlist-delta
```

To run unit and regression tests:
```bash
make test
```

To run code linting:
```bash
make lint
```
