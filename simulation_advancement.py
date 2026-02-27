from init_data import Dimensions, DRSState, DRSVars, Parameters, ControlVars, Configuation_expr
from evaluate_expr import evaluate_expr
from drs_env import build_env

def advance_simulation(conf : Configuation_expr, state : DRSState, dim : Dimensions, vars : DRSVars, params : Parameters, ctrl : ControlVars):

    env = build_env(state, vars, params, ctrl)

    terminating = int(evaluate_expr(conf.confExString_TerminatingCondition, env)) != 0
    if terminating:
        return None

    delay_time = max(float(state.drs_DurationUntilThresholdCrossing), 0.0)
    state.TNOW += delay_time

    delta_t = state.TNOW - state.drs_TimeOfPreviousDRSUpdate
    column_key = str(int(state.drs_RateConfigurationNumber))

    # update states
    for i in range(dim.dim_NumberOfLevels):
        row_label = vars.level_labels[i]
        expr = conf.confExString_LevelRate[row_label][column_key]
        rate = float(evaluate_expr(expr, env))
        state.drs_Level[i] = state.drs_Level[i] + rate * delta_t

    for i in range(dim.dim_NumberOfTimerss):
        row_label = vars.timer_labels[i]
        expr = conf.confExString_TimerRate[row_label][column_key]
        rate = float(evaluate_expr(expr, env))
        state.drs_Timer[i] = state.drs_Timer[i] + rate * delta_t

    state.drs_TimeOfPreviousDRSUpdate = state.TNOW

    assignment_address = 0
    crossing_idx = int(state.drs_ThresholdCrossingLevelOrTimerNumber) # must > 0 given 1 based idx hence test >0
    
    # Find new ass. addr.
    if crossing_idx > 0:
        if state.drs_ThresholdIsCrossedByTimer == 0:
            row_idx = min(crossing_idx, dim.dim_NumberOfLevels)
            row_label = vars.level_labels[row_idx - 1]
            if state.drs_DirectionOfThresholdCrossing == -1:
                expr = conf.confExString_LowerLevelAssignmentAddress[row_label][column_key]
            elif state.drs_DirectionOfThresholdCrossing == 1:
                expr = conf.confExString_UpperLevelAssignmentAddress[row_label][column_key]
            else:
                expr = "0"
        else:
            row_idx = min(crossing_idx, dim.dim_NumberOfTimerss)
            row_label = vars.timer_labels[row_idx - 1]
            if state.drs_DirectionOfThresholdCrossing == -1:
                expr = conf.confExString_LowerTimerAssignmentAddress[row_label][column_key]
            elif state.drs_DirectionOfThresholdCrossing == 1:
                expr = conf.confExString_UpperTimerAssignmentAddress[row_label][column_key]
            else:
                expr = "0"

        s = str(expr).strip()
        assignment_address = 0 if s == "" or s == '""' else int(evaluate_expr(expr, env))


    return assignment_address
