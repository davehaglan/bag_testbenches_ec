# -*- coding: utf-8 -*-

from pybag.enum import DesignOutput

from bag.design.database import ModuleDB

from bag_testbenches_ec.schematic.mos_analogbase import bag_testbenches_ec__mos_analogbase
from bag_testbenches_ec.schematic.mos_tb_ibias import bag_testbenches_ec__mos_tb_ibias


def test_dut_netlisting(tmpdir,
                        module_db: ModuleDB) -> None:
    """Check that testbench netlisting with static DUT works properly."""
    dut_params = dict(
        mos_type='nch',
        w=4,
        lch=10e-9,
        fg=20,
        intent='lvt',
    )
    dut_cell = 'MOS_ANALOGBASE'
    tb_params = dict(
        dut_lib=module_db.lib_name,
        dut_cell=dut_cell,
        vbias_dict={},
        ibias_dict={},
        dut_conns={},
    )
    tb_cell = 'TB_IBIAS'

    dut_fname = str(tmpdir.join('mos_analogbase.cdl'))
    tb_fname = str(tmpdir.join('mos_tb_ibias.cdl'))

    dut_master = module_db.new_master(bag_testbenches_ec__mos_analogbase, dut_params)
    cv_info_list = []
    module_db.batch_schematic([(dut_master, dut_cell)], output=DesignOutput.CDL, fname=dut_fname,
                              cv_info_out=cv_info_list)

    tb_master = module_db.new_master(bag_testbenches_ec__mos_tb_ibias, tb_params)
    module_db.batch_schematic([(tb_master, tb_cell)], output=DesignOutput.CDL,
                              fname=tb_fname, cv_info_list=cv_info_list, cv_netlist=dut_fname)

    # NOTE: right now, we just check this these functions execute without errors.
