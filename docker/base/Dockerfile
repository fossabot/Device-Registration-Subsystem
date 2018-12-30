#
# Base Dockerfile for DRS
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
FROM ubuntu:18.10

# Set environment (set proper unicode locale, hush debconfig, etc.
# Set PATH so that subsequent pip3 commands install into virtualenv.
# activate command does not work within Docker for some reason
ENV DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PATH=/home/drs/drs-venv/bin:$PATH \
    GOSU_VERSION=1.10

#
# - Set default shell to bash,
# - Update package lists
# - Install APT depdendencies
#
RUN set -x && \
    unlink /bin/sh; ln -s bash /bin/sh && \
    apt-get -q update && \
    apt-get -q install -y --no-install-recommends locales apt-utils git libpq-dev python3-pip \
                                                  python3-venv zip unzip wget default-jre-headless build-essential \
                                                  python3-dev vim nano gnupg && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#
# Set default locale
#
RUN update-locale LC_ALL=C.UTF-8 LANG=C.UTF-8

# Install gosu
RUN set -x && \
    wget -q -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)" && \
    chmod +x /usr/local/bin/gosu && \
    gosu nobody true

# Create non-root drs user
RUN set -x && \
    groupadd -g 9001 drs && \
    useradd -m -d /home/drs -s /bin/bash -u 9001 -g 9001 drs


#
# - Create DRS virtualenv
# - Upgrade pip and install wheel
# - Fix permissions, as pip3 installs are being done as root here
# - Make sure that a .drsenv file is always sourced into the environment if present. This file
#   contains environment variables like DRS_DB_HOSTNAME if they were provided when the processing container
#   was started
#
RUN set -x && \
    echo 'test -z "$VIRTUAL_ENV" && source /home/drs/drs-venv/bin/activate' >> /home/drs/.bashrc && \
    pyvenv /home/drs/drs-venv && \
    pip3 install --upgrade pip setuptools && \
    pip3 install wheel && \
    chown -R drs.drs /home/drs/.bashrc /home/drs/drs-venv && \
    echo 'if [ -f /home/drs/.drsenv ]; then source /home/drs/.drsenv; fi' >> /home/drs/drs-venv/bin/activate


# Create log volume dir and make sure it has the correct permissions
RUN set -x && \
    mkdir -p /var/log/drs && \
    chown -R drs.drs /var/log/drs

# Mark log volume
VOLUME ["/var/log/drs"]

# Override in child container
CMD ["gosu", "drs", "/bin/bash"]