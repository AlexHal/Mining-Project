from init_data import load_confExStrings_from_excel,  Dimensions, DRSState, DRSVars, Parameters, Configuation_expr, ControlVars
from initialization import initialization_state
from threshold_characterization import characterize_next_threshold
from simulation_advancement import advance_simulation
from rate_configuration import update_rate_config
from assignment_execution import assign_execute

def main():
    config = load_confExStrings_from_excel("MiningSystemDRS_ConfExStrings_v4.xlsx")
    dim = Dimensions()
    vars = DRSVars()
    params = Parameters()
    ctrl = ControlVars()

    state = initialization_state(config, dim, vars, params, ctrl)

    characterize_next_threshold(config, state, dim, vars, params, ctrl)
    # improve logic, remove second while loop
    while True:
        ass_info = advance_simulation(config, state, dim, vars, params, ctrl)

        if ass_info is None: #terminated
            break

        while ass_info == 0:
            update_rate_config(config, state, dim, vars, params, ctrl)
            characterize_next_threshold(config, state, dim, vars, params, ctrl)
            ass_info = advance_simulation(config, state, dim, vars, params, ctrl)


        assign_execute(config, state, dim, vars, params, ctrl, ass_info)
        