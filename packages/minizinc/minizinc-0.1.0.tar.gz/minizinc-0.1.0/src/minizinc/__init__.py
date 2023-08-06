#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Optional, Type

from .driver import Driver, find_driver
from .error import MiniZincError
from .instance import Instance as GenInstance
from .model import Method, Model
from .result import Result, Status
from .solver import Solver

Instance: Type[GenInstance]

#: Default MiniZinc driver used by the python package
default_driver: Optional[Driver] = find_driver()
if default_driver is not None:
    default_driver.make_default()
else:
    import warnings

    warnings.warn(
        "MiniZinc was not found on the system: no default driver could be initialised",
        RuntimeWarning,
    )

__all__ = [
    "default_driver",
    "find_driver",
    "Driver",
    "Instance",
    "Method",
    "MiniZincError",
    "Model",
    "Result",
    "Solver",
    "Status",
]
