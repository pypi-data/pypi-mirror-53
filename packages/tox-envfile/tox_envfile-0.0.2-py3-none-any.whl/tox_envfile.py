import os.path

import dotenv
import pluggy

hookimpl = pluggy.HookimplMarker("tox")


@hookimpl
def tox_configure(config):
    envvars = dotenv.dotenv_values(os.path.join(config.toxinidir, ".devdata.env"))

    for env in config.envlist:
        for name, value in envvars.items():
            config.envconfigs[env].setenv[name] = value
