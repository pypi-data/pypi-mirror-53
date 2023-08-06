# -*- coding: utf-8 -*-
import os
import click
import six

try:
    from .ml_sentry import sentry_capture_exceptions
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences
    from ml_sentry import sentry_capture_exceptions


class ApiException(Exception):
    pass


class InvalidJsonOutput(Exception):
    pass


class _ApiCall(object):
    def __init__(self, cli, command_cli, *commands, **kwargs):
        self._cli = cli
        self._commands = commands
        config_file = kwargs.pop('config_file', None)
        self._config_file = config_file
        self._command_cli = command_cli

    @sentry_capture_exceptions
    def __call__(self, *args, **kwargs):
        from missinglink.commands.global_cli import set_pre_call_hook, setup_pre_call

        set_pre_call_hook(setup_pre_call)

        return self._run(*args, **kwargs)

    def _get_param(self, key):
        for param in self._command_cli.params:
            name = '--' + key if isinstance(param, click.Option) else key
            if name in param.opts or name in param.secondary_opts:
                return param

    @classmethod
    def __make_arg_list(cls, key, val, param):
        if isinstance(val, (list, tuple)):
            if len(val) > 1 and not param.multiple:
                raise AttributeError('parameter %s does not support multiple' % (key,))

            return val

        return [val]

    def __validate_param(self, key):
        param = self._get_param(key)

        if param is None:
            raise AttributeError('api %s() does not have "%s" kwarg' % ('.'.join(self._commands), key))

        return param

    @classmethod
    def __process_bool_param(cls, val, key, param):
        flag = key
        if isinstance(param, click.Option) and param.is_bool_flag and not val:
            if param.secondary_opts:
                flag = param.secondary_opts[0]
                val = True
            else:
                val = None

        if isinstance(param, click.Option) and not flag.startswith('--'):
            flag = '--' + key

        return val, flag

    @classmethod
    def __make_list_if_needed(cls, val):
        return val if isinstance(val, (list, tuple)) else [val]

    def __convert_to_arg(self, cmd_args, key, val):
        key = key.replace('_', '-')

        param = self.__validate_param(key)

        val, flag = self.__process_bool_param(val, key, param)

        val = self.__make_arg_list(key, val, param)

        for single_val in val:
            if single_val is None:
                continue

            if isinstance(param, click.Option):
                cmd_args.append(flag)

                if param.is_bool_flag:
                    continue

            cmd_args.extend([str(single_val_item) for single_val_item in self.__make_list_if_needed(single_val)])

    def _convert_to_args(self, *args, **kwargs):
        cmd_args = ['--output-format', 'json', '--store-result', '--skip-version-check', '--disable-interactive']

        if self._config_file is not None:
            cmd_args.extend(['--config-file', self._config_file])

        for cmd in self._commands:
            cmd_args.append(str(cmd))

        for val in args:
            cmd_args.append(str(val))

        for key, val in kwargs.items():
            self.__convert_to_arg(cmd_args, key, val)

        return cmd_args

    def _run(self, *args, **kwargs):
        cmd_args = self._convert_to_args(*args, **kwargs)
        try:
            return self._cli.main(cmd_args, standalone_mode=False)
        except click.exceptions.MissingParameter as ex:
            type_param = 'arg' if isinstance(ex.param, click.Argument) else 'kwarg'
            six.raise_from(ValueError('required %s %s is missing' % (type_param, ex.param.human_readable_name.lower())),
                           None)


class _ApiProxy(object):
    def __init__(self, cli, *commands, **kwargs):
        self._cli = cli
        self._commands = list(commands) or []
        config_ctx = kwargs.pop('config_ctx', None)
        self._config_ctx = config_ctx or {}

    def _append_command(self, name):
        commands = self._commands[:]
        name = name.replace('_', '-')
        commands.append(name)

        return commands

    def _find_cli(self, name):
        current_cli = self._cli

        for current_cmd in self._append_command(name):
            if current_cmd in current_cli.commands:
                current_cli = current_cli.commands[current_cmd]
                continue

            raise AttributeError('command %s not found' % name)

        return current_cli

    @sentry_capture_exceptions
    def __getattr__(self, name):
        cli = self._find_cli(name)

        commands = self._append_command(name)
        proxy = _ApiProxy(self._cli, *commands, config_ctx=self._config_ctx)
        if isinstance(cli, click.Group):
            return proxy

        return _ApiCall(self._cli, cli, *commands, **self._config_ctx)


__as_api = None


# This function is duplicate as we cannot put it in a shared file and import
# The import of the shared file (which will be under missinglink.commands
# will trigger the load of the missinglink namespace that will load the missinglink.sdk
# and we will missing the by the time the function below will be executed the
# global exception hook will be already installed by the SDK
def disable_sdk_disable_exception_hook():
    os.environ['MISSINGLINKAI_DISABLE_EXCEPTION_HOOK'] = '1'
    os.environ['ML_DISABLE_LOGGING_HOOK'] = '1'


def as_api(config_file=None):
    global __as_api

    if __as_api is not None:
        return __as_api

    @sentry_capture_exceptions
    def __init_as_api():
        from missinglink.commands import cli, add_commands
        from missinglink.core.context import Expando

        add_commands()

        obj = Expando()
        obj.output_result = True

        config_ctx = {
            'config_file': config_file,
            'obj': obj
        }

        return _ApiProxy(cli, config_ctx=config_ctx)

    disable_sdk_disable_exception_hook()

    __as_api = __init_as_api()

    return __as_api


if __name__ == '__main__':
    as_api().run.xp(
        no_source=True,
        command=['python', '/mnt/gluster/shares/WP2_Analysis/WP2_models/temp_amit/agrinet/awsome/test.py'])
