from init_data import load_confExStrings_from_excel, Dimensions, DRSState, DRSVars, Parameters, Configuation_expr, ControlVars
from initialization import initialization_state
from threshold_characterization import characterize_next_threshold
from simulation_advancement import advance_simulation
from rate_configuration import update_rate_config
from assignment_execution import assign_execute
from output_statistics import compute_output_statistics
from out_plot import plot_modes, plot_ore_levels


def main():
    config = load_confExStrings_from_excel("MiningSystemDRS_ConfExStrings_v4.xlsx")
    dim = Dimensions()
    vars = DRSVars()
    params = Parameters()
    ctrl = ControlVars()

    state = initialization_state(config, dim, vars, params, ctrl)

    # --- time-series collectors ---
    time_series = []
    rate_config_series = []
    ore_stock_series = []
    ore1_stock_series = []
    ore2_stock_series = []

    def record(state: DRSState):
        time_series.append(state.TNOW)
        rate_config_series.append(state.drs_RateConfigurationNumber)
        ore_stock_series.append(state.drs_Level[2])   # OreStock_Level
        ore1_stock_series.append(state.drs_Level[3])  # Ore1Stock_Level
        ore2_stock_series.append(state.drs_Level[4])  # Ore2Stock_Level

    # Record initial state
    record(state)

    characterize_next_threshold(config, state, dim, vars, params, ctrl)

    # Main loop
    while True:
        assignment_address = advance_simulation(config, state, dim, vars, params, ctrl)

        if assignment_address is None:
            record(state)  # capture final state before exit
            break

        record(state)  # record after time advances, before assignments change state

        # maybe add a record in ass exe given that w have a loop in it
        assign_execute(config, state, dim, vars, params, ctrl, assignment_address)
        update_rate_config(config, state, dim, vars, params, ctrl)
        characterize_next_threshold(config, state, dim, vars, params, ctrl)

    stats = compute_output_statistics(state, vars, params)

    # --- plots ---
    fig1 = plot_modes(time_series, rate_config_series)
    fig1.savefig("output_plot/modes_plot.png", dpi=150)

    fig2 = plot_ore_levels(time_series, ore_stock_series, ore1_stock_series, ore2_stock_series)
    fig2.savefig("output_plot/ore_level_plot.png", dpi=150)

    return {
        "state": state,
        "output_statistics": stats,
    }


if __name__ == "__main__":
    result = main()
    for k, v in result["output_statistics"].__dict__.items():
        print(f"{k}: {v}")