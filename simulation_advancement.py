from init_data import Dimensions, DRSState, DRSVars, Parameters, ControlVars, Configuation_expr
from evaluate_expr import evaluate_expr
from drs_env import build_env
from helpers import get_matrix_expr


def advance_simulation(conf: Configuation_expr, state: DRSState, dim: Dimensions, vars: DRSVars, params: Parameters, ctrl: ControlVars):

    # check termination
    env = build_env(state, vars, params, ctrl)
    terminating = int(evaluate_expr(conf.confExString_TerminatingCondition, env)) != 0
    if terminating:
        return None

    # time++
    delay_time = max(float(state.drs_DurationUntilThresholdCrossing), 0.0)
    state.TNOW += delay_time
    delta_t = state.TNOW - state.drs_TimeOfPreviousDRSUpdate

    column_key = str(int(state.drs_RateConfigurationNumber))

    # rebuild env with updated time
    env = build_env(state, vars, params, ctrl)

    # update states
    for i in range(dim.dim_NumberOfLevels):
        row_label = vars.level_labels[i]
        expr = get_matrix_expr(conf.confExString_LevelRate, row_label, column_key, "0")
        rate = float(evaluate_expr(expr, env))
        state.drs_Level[i] = state.drs_Level[i] + rate * delta_t


    for i in range(dim.dim_NumberOfTimerss):
        row_label = vars.timer_labels[i]
        expr = get_matrix_expr(conf.confExString_TimerRate, row_label, column_key, "0")
        rate = float(evaluate_expr(expr, env))
        state.drs_Timer[i] = state.drs_Timer[i] + rate * delta_t

    # Find new ass. addr.
    assignment_address = 0
    crossing_idx = int(state.drs_ThresholdCrossingLevelOrTimerNumber)

    if crossing_idx > 0:
        if state.drs_ThresholdIsCrossedByTimer == 0:
            row_idx = min(crossing_idx, dim.dim_NumberOfLevels)
            row_label = vars.level_labels[row_idx - 1]
            if state.drs_DirectionOfThresholdCrossing == -1:
                expr = get_matrix_expr(conf.confExString_LowerLevelAssignmentAddress, row_label, column_key, "0")
            elif state.drs_DirectionOfThresholdCrossing == 1:
                expr = get_matrix_expr(conf.confExString_UpperLevelAssignmentAddress, row_label, column_key, "0")
            else:
                expr = "0"
        else:
            row_idx = min(crossing_idx, dim.dim_NumberOfTimerss)
            row_label = vars.timer_labels[row_idx - 1]
            if state.drs_DirectionOfThresholdCrossing == -1:
                expr = get_matrix_expr(conf.confExString_LowerTimerAssignmentAddress, row_label, column_key, "0")
            elif state.drs_DirectionOfThresholdCrossing == 1:
                expr = get_matrix_expr(conf.confExString_UpperTimerAssignmentAddress, row_label, column_key, "0")
            else:
                expr = "0"

        s = str(expr).strip()
        assignment_address = 0 if s == "" or s == '""' else int(evaluate_expr(expr, env))

    return assignment_address