from pathlib import Path

import matplotlib.pyplot as plt
import pandapower as pp


RESULTS_DIR = Path("results")


def run_power_flow(net):
    """Run a steady-state AC power-flow calculation."""
    pp.runpp(net)
    return net


def save_results(net, results_dir=RESULTS_DIR):
    """Save an interactive network view and voltage profile."""
    results_dir.mkdir(parents=True, exist_ok=True)

    pp.plotting.to_html(
        net,
        str(results_dir / "network.html"),
        respect_switches=True,
        include_lines=True,
        include_trafos=True,
        show_tables=True,
    )

    bus_names = net.bus["name"]
    voltages = net.res_bus["vm_pu"]

    plt.figure(figsize=(10, 6))
    plt.plot(bus_names, voltages, marker="o")
    plt.axhline(1.0, linestyle="--", label="Nominal voltage")
    plt.axhline(0.95, linestyle=":", label="Lower limit")
    plt.title("Bus Voltage Profile")
    plt.ylabel("Voltage (p.u.)")
    plt.xlabel("Bus")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(results_dir / "voltage_profile.png", dpi=150)
    plt.close()
