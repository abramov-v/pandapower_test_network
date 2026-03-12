import pandapower as pp
import matplotlib.pyplot as plt


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

    hv_grid_bus = pp.create_bus(
        net,
        vn_kv=HV_VOLTAGE_LEVEL,
        type='b',
        name='HV_GRID_BUS',
    )

    pp.create_ext_grid(
        net,
        bus=hv_grid_bus,
        vm_pu=1.0,
        name='HV_GRID',
    )

    mv_main_bus = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_MAIN_BUS',
    )

    hv_mv_transformer = pp.create_transformer(
        net,
        hv_grid_bus,
        mv_main_bus,
        name='HV_MV_TRANSFORMER',
        std_type='25 MVA 110/20 kV',
    )

    pp.create_switch(
        net,
        mv_main_bus,
        element=hv_mv_transformer,
        et='t',
        name='HV_MV_TRANSFORMER_CB',
        closed=True,
    )

    lv_main_bus = pp.create_bus(
        net,
        vn_kv=LV_VOLTAGE_LEVEL,
        type='b',
        name='LV_MAIN_BUS',
    )

    mv_feeder_a_mid_bus = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_A_MID_BUS',
    )

    pp.create_line(
        net,
        mv_main_bus,
        mv_feeder_a_mid_bus,
        length_km=3.0,
        parallel=1.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_A_SECTION_1',
    )

    mv_feeder_a_end_bus = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_A_END_BUS',
    )

    pp.create_line(
        net,
        mv_feeder_a_mid_bus,
        mv_feeder_a_end_bus,
        length_km=3.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_A_SECTION_2',
    )

    pp.create_load(
        net,
        mv_feeder_a_end_bus,
        p_mw=10.0,
        q_mvar=1.0,
        name='MV_LOAD_1',
    )

    mv_feeder_b_end_bus = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_B_END_BUS',
    )

    pp.create_line(
        net,
        mv_main_bus,
        mv_feeder_b_end_bus,
        length_km=6.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_B_SECTION_1',
    )

    pp.create_load(
        net,
        mv_feeder_b_end_bus,
        p_mw=7.0,
        q_mvar=0.9,
        name='MV_LOAD_2',
    )

    mv_feeder_c_mid_bus = pp.create_bus(
        net,
        vn_kv=MV_VOLTAGE_LEVEL,
        type='b',
        name='MV_FEEDER_C_MID_BUS',
    )

    pp.create_line(
        net,
        mv_main_bus,
        mv_feeder_c_mid_bus,
        length_km=2.0,
        parallel=1.0,
        std_type='184-AL1/30-ST1A 20.0',
        name='FEEDER_C_SECTION_1',
    )

    pp.create_transformer(
        net,
        mv_feeder_c_mid_bus,
        lv_main_bus,
        name='MV_LV_TRANSFORMER',
        std_type='0.63 MVA 20/0.4 kV',
    )

    pp.create_load(
        net,
        lv_main_bus,
        p_mw=0.25,
        q_mvar=0.15,
        name='LV_LOAD_1',
    )

    pp.create_sgen(
        net,
        bus=mv_feeder_b_end_bus,
        p_mw=1.5,
        q_mvar=0.0,
        name='PV_FEEDER_B',
    )

    return net


def main():

    net = create_network()
    pp.runpp(net)

    print('\n' + '-' * 90)
    print('BUS RESULTS')
    print('-' * 90)

    bus_results = net.bus[['name', 'vn_kv']].join(
        net.res_bus[['vm_pu', 'p_mw', 'q_mvar']]
    )
    print(bus_results)

    print('\n' + '-' * 90)
    print('LINE RESULTS')
    print('-' * 90)

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

    print('\n' + '-' * 90)
    print('TRANSFORMER RESULTS')
    print('-' * 90)

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

    print('\n' + '-' * 90)

    pp.plotting.to_html(
        net,
        'D:\\Projects\\test_projects_2026\\pandapower_test\\results.html',
        respect_switches=True,
        include_lines=True,
        include_trafos=True,
        show_tables=True,
    )

    pp.plotting.simple_plot(
        net,
        respect_switches=True,
        line_width=1.5,
        bus_size=0.5,
        ext_grid_size=2.0,
        trafo_size=3.0,
        plot_loads=False,
        plot_gens=False,
        plot_sgens=True,
        load_size=1.0,
        gen_size=1.0,
        sgen_size=2.0,
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
    # получить напряжения
    bus_names = net.bus['name']
    voltages = net.res_bus['vm_pu']

    plt.figure(figsize=(10, 6))

    plt.plot(bus_names, voltages, marker='o')

    plt.axhline(1.0, linestyle='--', label='Nominal voltage')
    plt.axhline(0.95, linestyle=':', label='Lower limit')

    plt.title('Bus Voltage Profile')
    plt.ylabel('Voltage (p.u.)')
    plt.xlabel('Bus')

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
