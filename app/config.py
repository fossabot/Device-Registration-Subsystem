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

    def __init__(self, path):
        """Constructor."""
        self.logger = DRSLogger().get_logger()
        self.config_path = path

    def parse_config(self):
        """Helper method to parse the config file from the disk."""
        try:
            cfg = yaml.safe_load(open(self.config_path))
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


class ConfigApp:
    """Class to configure app object by loading yml configuration"""

    def __init__(self, app, config):
        """Constructor."""
        self.app = app
        self.config = config

    def database_uri(self):
        database_config = self.config.get('database')
        return 'postgres://{0}:{1}@{2}:{3}/{4}'.format(
            database_config.get('user', 'postgres'),
            database_config.get('password', ''),
            database_config.get('host', 'localhost'),
            database_config.get('port', 5432),
            database_config.get('database', 'postgres')
        )

    def load_config(self):
        """Method to load all the config to app object."""
        global_config = self.config.get('global')
        lists_config = self.config.get('lists')
        database_config = self.config.get('database')

        self.app.config['DRS_UPLOADS'] = global_config.get('upload_directory')  # file upload dir
        self.app.config['DRS_LISTS'] = lists_config.get('path')  # lists dir
        self.app.config['STRICT_HTTPS'] = self.config.get('server')['restrict_https']
        self.app.config['CORE_BASE_URL'] = global_config.get('core_api_v2')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = self.database_uri()
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_POOL_SIZE'] = database_config.get('pool_size')
        self.app.config['SQLALCHEMY_POOL_RECYCLE'] = database_config.get('pool_recycle')
        self.app.config['SQLALCHEMY_MAX_OVERFLOW'] = database_config.get('max_overflow')
        self.app.config['SQLALCHEMY_POOL_TIMEOUT'] = database_config.get('pool_timeout')
        # app.config['MAX_CONTENT_LENGTH'] = 28 * 3 * 1024 * 1024
        return self.app
