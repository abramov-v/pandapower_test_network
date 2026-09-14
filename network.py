import pandapower as pp

from constants import (
    GRID_FREQUENCY,
    GRID_NAME,
    HV_VOLTAGE_LEVEL,
    LV_VOLTAGE_LEVEL,
    MV_VOLTAGE_LEVEL,
)


def create_network():
    """Create the HV/MV/LV test network."""
    net = pp.create_empty_network(name=GRID_NAME, f_hz=GRID_FREQUENCY)

    hv_grid_bus = pp.create_bus(
        net, vn_kv=HV_VOLTAGE_LEVEL, type="b", name="HV_GRID_BUS"
    )
    pp.create_ext_grid(net, bus=hv_grid_bus, vm_pu=1.0, name="HV_GRID")

    mv_main_bus = pp.create_bus(
        net, vn_kv=MV_VOLTAGE_LEVEL, type="b", name="MV_MAIN_BUS"
    )

    hv_mv_transformer = pp.create_transformer(
        net,
        hv_grid_bus,
        mv_main_bus,
        name="HV_MV_TRANSFORMER",
        std_type="25 MVA 110/20 kV",
    )
    pp.create_switch(
        net,
        mv_main_bus,
        element=hv_mv_transformer,
        et="t",
        name="HV_MV_TRANSFORMER_CB",
        closed=True,
    )

    lv_main_bus = pp.create_bus(
        net, vn_kv=LV_VOLTAGE_LEVEL, type="b", name="LV_MAIN_BUS"
    )

    mv_feeder_a_mid_bus = pp.create_bus(
        net, vn_kv=MV_VOLTAGE_LEVEL, type="b", name="MV_FEEDER_A_MID_BUS"
    )
    pp.create_line(
        net,
        mv_main_bus,
        mv_feeder_a_mid_bus,
        length_km=3.0,
        std_type="184-AL1/30-ST1A 20.0",
        name="FEEDER_A_SECTION_1",
    )

    mv_feeder_a_end_bus = pp.create_bus(
        net, vn_kv=MV_VOLTAGE_LEVEL, type="b", name="MV_FEEDER_A_END_BUS"
    )
    pp.create_line(
        net,
        mv_feeder_a_mid_bus,
        mv_feeder_a_end_bus,
        length_km=3.0,
        std_type="184-AL1/30-ST1A 20.0",
        name="FEEDER_A_SECTION_2",
    )
    pp.create_load(
        net, mv_feeder_a_end_bus, p_mw=10.0, q_mvar=1.0, name="MV_LOAD_1"
    )

    mv_feeder_b_end_bus = pp.create_bus(
        net, vn_kv=MV_VOLTAGE_LEVEL, type="b", name="MV_FEEDER_B_END_BUS"
    )
    pp.create_line(
        net,
        mv_main_bus,
        mv_feeder_b_end_bus,
        length_km=6.0,
        std_type="184-AL1/30-ST1A 20.0",
        name="FEEDER_B_SECTION_1",
    )
    pp.create_load(
        net, mv_feeder_b_end_bus, p_mw=7.0, q_mvar=0.9, name="MV_LOAD_2"
    )
    pp.create_sgen(
        net, bus=mv_feeder_b_end_bus, p_mw=1.5, q_mvar=0.0, name="PV_FEEDER_B"
    )

    mv_feeder_c_mid_bus = pp.create_bus(
        net, vn_kv=MV_VOLTAGE_LEVEL, type="b", name="MV_FEEDER_C_MID_BUS"
    )
    pp.create_line(
        net,
        mv_main_bus,
        mv_feeder_c_mid_bus,
        length_km=2.0,
        std_type="184-AL1/30-ST1A 20.0",
        name="FEEDER_C_SECTION_1",
    )
    pp.create_transformer(
        net,
        mv_feeder_c_mid_bus,
        lv_main_bus,
        name="MV_LV_TRANSFORMER",
        std_type="0.63 MVA 20/0.4 kV",
    )
    pp.create_load(
        net, lv_main_bus, p_mw=0.25, q_mvar=0.15, name="LV_LOAD_1"
    )

    return net
