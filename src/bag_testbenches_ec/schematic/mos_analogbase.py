# -*- coding: utf-8 -*-

from typing import Dict, Union, List, Tuple, Any

import os
import pkg_resources

from bag.util.cache import Param
from bag.design.module import Module
from bag.design.database import ModuleDB


# noinspection PyPep8Naming
class bag_testbenches_ec__mos_analogbase(Module):
    """Module for library bag_testbenches_ec cell mos_analogbase.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'mos_analogbase.yaml'))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            mos_type="Transistor type.  Either 'pch' or 'nch'.",
            w='Transistor width in meters or number of fins.',
            lch='Transistor length in meters.',
            fg='Transistor number of segments.',
            intent='Transistor threshold flavor.',
            stack='Number of stacked transistors in a segment.',
            dum_info='Dummy information data structure.',
        )

    @classmethod
    def get_default_param_values(cls) -> Dict[str, Any]:
        return dict(
            intent='standard',
            stack=1,
            dum_info=None,
        )

    def design(self, mos_type: str, w: Union[float, int], lch: float, fg: int, intent: str,
               stack: int, dum_info: List[Tuple[Any]]) -> None:
        """Design a single transistor for characterization purposes.

        Parameters
        ----------
        mos_type : str
            the transistor type.  Either 'nch' or 'pch'.
        w : Union[float, int]
            transistor width, in fins or meters.
        lch : float
            transistor channel length, in meters.
        fg : int
            number of fingers.
        intent : str
            transistor threshold flavor.
        stack : int
            number of transistors in a stack.
        dum_info : List[Tuple[Any]]
            the dummy information data structure.
        """
        self.design_transistor('XM', w, lch, fg, intent, 'mid', d='d', g='g', s='s', b='b',
                               stack=stack)
        # handle dummy transistors
        self.design_dummy_transistors(dum_info, 'XD', 'b', 'b')
