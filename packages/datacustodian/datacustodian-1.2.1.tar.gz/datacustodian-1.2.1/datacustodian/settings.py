import yaml
import logging
from os import path
from attrdict import AttrDict

from datacustodian.utility import relpath
from datacustodian.io import read

log = logging.getLogger(__name__)

specs = {}
"""dict: keys are component names; values are a `dict` with component specs.
"""
app_specs = {}
"""dict: keys are one of ['dlt','package','db','ipfs','overrides','server','auth'];
values are the specifications from those sections of the application specs.
"""
override_files = {}
"""dict: keys are module FQNs; values are the full paths to the override
file for that module.
"""

def calc_override_path(module_fqn):
    """Makes sure that the path for the override file has been set correctly.

    Args:
        module_fqn (str): FQN of the module attr to retrieve overrides for.
    """
    global override_files
    target = override_files.get(module_fqn)
    if target is None:
        target = path.join(app_specs["overrides"], f"{module_fqn}.yml")
        override_files[module_fqn] = target

    return target

def get_overrides(module_fqn):
    """Retrieves the set of overrided settings for the given module.

    Args:
        module_fqn (str): FQN of the module attr to retrieve overrides for.
    """
    target = calc_override_path(module_fqn)
    if not path.isfile(target):
        return {}

    with open(target) as f:
        r = yaml.load(f, Loader=yaml.FullLoader)
    log.debug(f"Retrieved overrides for {module_fqn} as {r}.")
    return r

def save_overrides(module_fqn, overrides):
    """Saves the specified overrides `dict` to persistent storage.

    .. note:: This does not update the actual live configuration of the module,
        it only persists the contents of the `overrides` dictionary to disk.

    Args:
        module_fqn (str): FQN of the module attr to save overrides for.
        overrides (dict): overridden configuration propertes for this module
            attribute.
    """
    target = calc_override_path(module_fqn)
    with open(target, 'w') as f:
        f.write(yaml.dump(overrides, Dumper=yaml.Dumper))

def load(specfile, asattr=True):
    """Recursively loads the specificied specfile into a :class:`attrdict.AttrDict`.

    Args:
        specfile (str): path to the specification YML file; may be relative.
        asattr (bool): when True, return the spec as a :class:`AttrDict`;
            otherwise, return as-is.
    """
    context, sfile = path.split(path.abspath(specfile))
    spec = read(context, path.splitext(sfile)[0])

    if asattr:
        return AttrDict(spec)
    else:
        return spec
