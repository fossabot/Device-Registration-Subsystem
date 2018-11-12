"""
DRS configuration file parser.
Copyright (c) 2018 Qualcomm Technologies, Inc.
 All rights reserved.
 Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the
 limitations in the disclaimer below) provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following
 disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
 disclaimer in the documentation and/or other materials provided with the distribution.
 * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or promote
 products derived from this software without specific prior written permission.
 NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED BY
 THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
 TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
"""
import yaml

from app.logger import DRSLogger


class ParseException(Exception):
    """Indicates that there was an exception encountered when parsing the DRS config file."""
    pass


class ConfigParser:
    """Class to parse the DRS YAML config and turn it into python config object."""

    def __init__(self):
        """Constructor."""
        self.logger = DRSLogger().get_logger()

    def parse_config(self):
        """Helper method to parse the config file from the disk."""
        try:
            cfg = yaml.safe_load(open('etc/config.yml'))
            if cfg is None:
                self.logger.error('Error in parsing config file @ etc/config.yml')
                raise ParseException('Error in parsing config file @ etc/config.yml')
            self.logger.debug('successfully parsed DRS config @ etc/config.yml')
            return cfg
        except yaml.YAMLError as e:
            self.logger.error('Error in parsing config file @ etc/config.yml')
            raise ParseException(str(e))
        except IOError:
            self.logger.error('config file does not exists @ etc/config.yml')
            raise ParseException('config file does not exists @ etc/config.yml')
