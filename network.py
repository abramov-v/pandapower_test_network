import pandapower as pp


from constants import (
    GRID_FREQUENCY,
    MV_VOLTAGE_LEVEL,
    HV_VOLTAGE_LEVEL,
    LV_VOLTAGE_LEVEL,
    GRID_NAME,
)


def create_network():
    net = pp.create_empty_network(
        name=GRID_NAME,
        f_hz=GRID_FREQUENCY,
    )

    HV_GRID_BUS = pp.create_bus(
        net,
        vn_kv=HV_VOLTAGE_LEVEL,
        type='b',
        name='HV_GRID_BUS',
    )

    HV_GRID = pp.create_ext_grid(
        net,
        bus=HV_GRID_BUS,
        vm_pu=1.0,
        name='HV_GRID',
    )

    MV_MAIN_BUS = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_MAIN_BUS',
    )

    HV_MV_TRANSFORMER = pp.create_transformer(
        net,
        HV_GRID_BUS,
        MV_MAIN_BUS,
        name='HV_MV_TRANSFORMER',
        std_type='25 MVA 110/20 kV',
    )

    HV_MV_TRANSFORMER_CB = pp.create_switch(
        net,
        MV_MAIN_BUS,
        element=HV_MV_TRANSFORMER,
        et='t',
        name='HV_MV_TRANSFORMER_CB',
        closed=True,
    )

    LV_MAIN_BUS = pp.create_bus(
        net,
        vn_kv=LV_VOLTAGE_LEVEL,
        type='b',
        name='LV_MAIN_BUS',
    )

    MV_LV_TRANSFORMER = pp.create_transformer(
        net,
        MV_MAIN_BUS,
        LV_MAIN_BUS,
        name='MV_LV_TRANSFORMER',
        std_type='0.63 MVA 20/0.4 kV',
    )

    LV_LOAD_1 = pp.create_load(
        net,
        LV_MAIN_BUS,
        p_mw=0.25,
        q_mvar=0.15,
        name='LV_LOAD_1',
    )

    MV_FEEDER_A_MID_BUS = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_A_MID_BUS',
    )

    MV_LINE_1 = pp.create_line(
        net,
        MV_MAIN_BUS,
        MV_FEEDER_A_MID_BUS,
        length_km=3.0,
        parallel=1.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_A_SECTION_1',
    )

    MV_FEEDER_A_END_BUS = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_A_END_BUS',
    )

    MV_LINE_2 = pp.create_line(
        net,
        MV_FEEDER_A_MID_BUS,
        MV_FEEDER_A_END_BUS,
        length_km=5.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_A_SECTION_2',
    )

    MV_LOAD_1 = pp.create_load(
        net,
        MV_FEEDER_A_END_BUS,
        p_mw=7.0,
        q_mvar=0.9,
        name='MV_LOAD_1',
    )

    MV_FEEDER_B_END_BUS = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_B_END_BUS',
    )

    MV_LINE_3 = pp.create_line(
        net,
        MV_MAIN_BUS,
        MV_FEEDER_B_END_BUS,
        length_km=10.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_B_SECTION_1',
    )

    MV_LOAD_2 = pp.create_load(
        net,
        MV_FEEDER_B_END_BUS,
        p_mw=5,
        q_mvar=0.8,
        name='MV_LOAD_2',
    )

    return net


def main():

    net = create_network()
    pp.runpp(net)

    print('\n' + '*' * 90)
    print('BUS RESULTS')
    print('*' * 90)

    bus_results = net.bus[['name', 'vn_kv']].join(
        net.res_bus[['vm_pu', 'va_degree', 'p_mw', 'q_mvar']]
    )
    print(bus_results)

    print('\n' + '*' * 90)
    print('LINE RESULTS')
    print('*' * 90)

    line_results = net.line[
        [
            'name',
            'std_type',
            'length_km',
            'max_i_ka',
            ]
        ].join(
        net.res_line[['i_ka', 'loading_percent', 'p_from_mw', 'q_from_mvar']]
    )
    print(line_results)

    print('\n' + '*' * 90)
    print('TRANSFORMER RESULTS')
    print('*' * 90)

    trafo_results = net.trafo[['name', 'std_type']].join(
        net.res_trafo[
            [
                'loading_percent',
                'p_hv_mw',
                'q_hv_mvar',
                'p_lv_mw',
                'q_lv_mvar',
            ]
        ]
    )
    print(trafo_results)

    print('\n' + '*' * 90)

    pp.plotting.simple_plot(
        net,
        respect_switches=True,
        line_width=1.5,
        bus_size=0.5,
        ext_grid_size=2.0,
        trafo_size=3.0,
        plot_loads=False,
        plot_gens=False,
        plot_sgens=False,
        load_size=1.0,
        gen_size=1.0,
        sgen_size=1.0,
        switch_size=2.0,
        switch_distance=1.0,
        plot_line_switches=True,
        scale_size=True,
        bus_color='b',
        line_color='grey',
        dcline_color='c',
        trafo_color='g',
        ext_grid_color='purple',
        switch_color='k',
        library='igraph',
        show_plot=True,
        ax=None,
        vsc_size=2.0,
        vsc_color='orange'
    )

    # check = pp.available_std_types(net, element='line')
    # print(check)


if __name__ == '__main__':
    main()
