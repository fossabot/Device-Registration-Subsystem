#
# Dockerfile to build Docker API image for DIRBS-DRS
#
# Copyright (c) 2018 Qualcomm Technologies, Inc.
#
# All rights reserved.
#
#
#
# Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
# limitations in the disclaimer below) provided that the following conditions are met:
#
#
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
#
# * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
# THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

FROM drs-base

# install postgresql client
RUN set -x && \
    echo 'deb http://apt.postgresql.org/pub/repos/apt/ cosmic-pgdg main' > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get -q update --fix-missing && \
    apt-get -q install -y --no-install-recommends postgresql rsync wget unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# create directories
RUN set -x && \
    mkdir -p /home/drs/app && \
    mkdir -p /home/drs/tests && \
    mkdir -p /home/drs/etc && \
    mkdir -p /home/drs/scripts

# Copy all the necessary file
COPY requirements.txt setup.py README.md docker/prd/api/uwsgi.ini /home/drs/
COPY app /home/drs/app/
COPY tests /home/drs/tests/
COPY test_requirements.txt pytest.ini /home/drs/
COPY manage.py .pylintrc Makefile /home/drs/
COPY etc /home/drs/etc/
COPY scripts /home/drs/scripts

# install dependencies
RUN set -x && \
    pip3 install -r /home/drs/requirements.txt && \
    pip3 install uwsgi==2.0.15 && \
    pip3 install uwsgitop==0.10 && \
    pip3 uninstall -y simplejson && \
    chown -R drs.drs /home/drs/drs-venv && \
    chmod 755 /home/drs/drs-venv/bin/uwsgitop

# copy other file
COPY docker/prd/api/entrypoint.sh /entrypoint.sh

# make sure permissions are right on entrypoint
RUN set -x && chmod a+x /entrypoint.sh

# Expose port 5000 for API server
EXPOSE 5000

# set entry point
ENTRYPOINT ["/entrypoint.sh"]

# set command
CMD ["gosu", "drs", "uwsgi", "--ini", "/home/drs/uwsgi.ini"]
