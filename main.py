from analysis import run_power_flow, save_results
from network import create_network


def main():
    net = create_network()
    run_power_flow(net)

    print(f"Network: {net.name}")
    print(f"Power flow converged: {net.converged}")
    print("\nBus voltage profile:")
    print(net.res_bus[["vm_pu"]])

    print("\nLine loading:")
    print(net.res_line[["loading_percent"]])

    print("\nTransformer loading:")
    print(net.res_trafo[["loading_percent"]])

    save_results(net)
    print("\nResults saved to results/")


if __name__ == "__main__":
    main()
