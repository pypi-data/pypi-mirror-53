import codecs
import logging
import logging.config
import sys
import time
from pathlib import Path

import ruamel.yaml
from EasyCo import ConfigFile, PathContainer

from HABApp.__version__ import __VERSION__
from HABApp.runtime import FileEventTarget
from ._conf_mqtt import Mqtt
from ._conf_openhab import Openhab
from .default_logfile import get_default_logfile

_yaml_param = ruamel.yaml.YAML(typ='safe')
_yaml_param.default_flow_style = False
_yaml_param.default_style = False
_yaml_param.width = 1000000
_yaml_param.allow_unicode = True
_yaml_param.sort_base_mapping_type_on_output = False


log = logging.getLogger('HABApp.Config')


class AbsolutePathExpected(Exception):
    pass


class InvalidConfigException(Exception):
    pass


class Directories(PathContainer):
    logging: Path = 'log'
    rules: Path = 'rules'
    lib: Path = 'lib'
    param: Path = 'param'

    def on_all_values_set(self):
        try:
            if not self.rules.is_dir():
                self.rules.mkdir()
            if not self.logging.is_dir():
                self.logging.mkdir()
        except Exception as e:
            log.error(e)


class HABAppConfigFile(ConfigFile):
    directories = Directories()
    mqtt = Mqtt()
    openhab = Openhab()


class Config(FileEventTarget):

    def __init__(self, runtime, config_folder : Path):

        import HABApp.runtime
        assert isinstance(runtime, HABApp.runtime.Runtime)
        self.__runtime = runtime

        assert isinstance(config_folder, Path)
        assert config_folder.is_dir(), config_folder
        self.folder_conf = config_folder
        self.file_conf_habapp  = self.folder_conf / 'config.yml'
        self.file_conf_logging = self.folder_conf / 'logging.yml'

        # these are the accessible config entries
        self.config = HABAppConfigFile()
        self.directories = self.config.directories
        self.mqtt = self.config.mqtt
        self.openhab = self.config.openhab

        # if the config does not exist it will be created
        self.__check_create_logging()

        # folder watcher
        self.__runtime.folder_watcher.watch_folder(
            folder=self.folder_conf,
            file_ending='.yml',
            event_target=self
        )

        # Load Config initially
        self.first_start = True
        try:
            # try load logging config first. If we use abs path we can log errors when loading config.yml
            self.add_file(self.file_conf_logging)
            self.add_file(self.file_conf_habapp)
        except AbsolutePathExpected:
            self.add_file(self.file_conf_habapp)
            self.add_file(self.file_conf_logging)
        self.first_start = False

    def add_file(self, path: Path):
        self.reload_file(path)

    def reload_file(self, path: Path):
        if path.name == 'config.yml':
            self.load_cfg()
        if path.name == 'logging.yml':
            self.load_log()

    def remove_file(self, path: Path):
        pass

    def __check_create_logging(self):
        if self.file_conf_logging.is_file():
            return None

        print(f'Creating {self.file_conf_logging.name} in {self.file_conf_logging.parent}')
        with self.file_conf_logging.open('w', encoding='utf-8') as file:
            file.write(get_default_logfile())

        time.sleep(0.1)
        return None

    def load_cfg(self):
        # We always try to create the dummy config
        # # File has to exist - check because we also get FileDelete events
        # if not self.file_conf_habapp.is_file():
        #     return

        self.config.load(self.file_conf_habapp)

        # Set path for libraries
        if self.directories.lib.is_dir():
            lib_path = str(self.directories.lib)
            if lib_path not in sys.path:
                sys.path.insert(0, lib_path)
                log.debug( f'Added library folder "{lib_path}" to path')

        # check if folders exist and print warnings
        if not self.directories.rules.is_dir():
            log.warning( f'Folder for rules files does not exist: {self.directories.rules}')

        log.debug('Loaded HABApp config')
        return None

    def load_log(self):
        # File has to exist - check because we also get FileDelete events
        if not self.file_conf_logging.is_file():
            return None

        with self.file_conf_logging.open('r', encoding='utf-8') as file:
            cfg = _yaml_param.load(file)

        # fix filenames
        for handler, handler_cfg in cfg.get('handlers', {}).items():

            # fix encoding for FileHandlers - we always log utf-8
            if 'file' in handler_cfg.get('class', '').lower():
                enc = handler_cfg.get('encoding', '')
                if enc != 'utf-8':
                    handler_cfg['encoding'] = 'utf-8'

            if 'filename' not in handler_cfg:
                continue

            # make Filenames absolute path in the log folder if not specified
            p = Path(handler_cfg['filename'])
            if not p.is_absolute():
                # Our log folder ist not yet converted to path -> it is not loaded yet
                if isinstance(self.directories.logging, str):
                    raise AbsolutePathExpected()

                # Use defined parent folder
                p = (self.directories.logging / p).resolve()
                handler_cfg['filename'] = str(p)

            # Delete old Log-Files on startup
            if self.first_start and p.is_file():
                try:
                    # default is utf-8 logging so we write BOM
                    with open(p, mode='wb') as f:
                        f.write(codecs.BOM_UTF8)
                finally:
                    pass

        # load prepared logging
        try:
            logging.config.dictConfig(cfg)
        except Exception as e:
            print(f'Error loading logging config: {e}')
            return None

        log.debug('Loaded logging config')
        logging.getLogger('HABApp').info(f'HABApp Version {__VERSION__}')
        return None
