# -*- coding: utf-8 -*-

from typing import Dict, Union, List, Tuple, Any

import os
import pkg_resources

from bag.util.cache import Param
from bag.design.module import Module
from bag.design.database import ModuleDB


# noinspection PyPep8Naming
class bag_testbenches_ec__mos_cascode(Module):
    """Module for library bag_testbenches_ec cell mos_cascode.

    Fill in high level description here.
    """

    yaml_file = pkg_resources.resource_filename(__name__,
                                                os.path.join('netlist_info',
                                                             'mos_cascode.yaml'))

    def __init__(self, database: ModuleDB, params: Param, **kwargs: Any) -> None:
        Module.__init__(self, self.yaml_file, database, params, **kwargs)

    @classmethod
    def get_params_info(cls) -> Dict[str, str]:
        return dict(
            mos_type="Transistor type.  Either 'pch' or 'nch'.",
            lch='Transistor length in meters.',
            intentb='Bottom transistor threshold flavor.',
            intentc='Cascode transistor threshold flavor.',
            wb='Bottom transistor width in meters or number of fins.',
            wc='Cascode transistor width in meters or number of fins.',
            fgb='Bottom transistor number of segments.',
            fgc='Cascode transistor number of segments.',
            stackb='Number of stacked bottom transistors in a segment.',
            stackc='Number of stacked bottom transistors in a segment.',
            dum_info='Dummy information data structure.',
        )

    @classmethod
    def get_default_param_values(cls) -> Dict[str, Any]:
        return dict(
            intentb='standard',
            intentc='standard',
            stackb=1,
            stackc=1,
            dum_info=None,
        )

    def design(self, mos_type: str, lch: float, intentb: str, intentc: str, wb: Union[float, int],
               wc: Union[float, int], fgb: int, fgc: int, stackb: int, stackc: int,
               dum_info: List[Tuple[Any]]) -> None:
        """Design this cascode transistor.
        """
        if fgb == 1 or fgc == 1:
            raise ValueError('Cannot make 1 finger transistor.')
        # select the correct transistor type
        if mos_type == 'pch':
            self.replace_instance_master('XB', 'BAG_prim', 'pmos4_standard')
            self.replace_instance_master('XC', 'BAG_prim', 'pmos4_standard')

        self.design_transistor('XB', wb, lch, fgb, intentb, 'midb', d='mid', g='g', s='s', b='b',
                               stack=stackb)
        self.design_transistor('XC', wc, lch, fgc, intentc, 'midc', d='d', g='c', s='mid', b='b',
                               stack=stackc)

        # handle dummy transistors
        self.design_dummy_transistors(dum_info, 'XD', 'b', 'b')
