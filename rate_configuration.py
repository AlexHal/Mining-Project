from init_data import Dimensions, DRSState, DRSVars, Parameters, ControlVars, Configuation_expr
from evaluate_expr import evaluate_expr
from drs_env import build_env
from helpers import get_matrix_expr

# Implementing
# drs_RateConfigurationNumber
# 	(drs_ThresholdIsCrossedByTimer == 0)*(drs_DirectionOfThresholdCrossing == -1)*Eval(confExString_LowerLevelResultantRateConfiguration(MN(drs_ThresholdCrossingLevelOrTimerNumber,dim_NumberOfLevels),drs_RateConfigurationNumber))
#  + (drs_ThresholdIsCrossedByTimer == 0)*(drs_DirectionOfThresholdCrossing == 1)*Eval(confExString_UpperLevelResultantRateConfiguration(MN(drs_ThresholdCrossingLevelOrTimerNumber,dim_NumberOfLevels),drs_RateConfigurationNumber))
#  + (drs_ThresholdIsCrossedByTimer == 1)*(drs_DirectionOfThresholdCrossing == -1)*Eval(confExString_LowerTimerResultantRateConfiguration(MN(drs_ThresholdCrossingLevelOrTimerNumber,dim_NumberOfTimers),drs_RateConfigurationNumber))
#  + (drs_ThresholdIsCrossedByTimer == 1)*(drs_DirectionOfThresholdCrossing == 1)*Eval(confExString_UpperTimerResultantRateConfiguration(MN(drs_ThresholdCrossingLevelOrTimerNumber,dim_NumberOfTimers),drs_RateConfigurationNumber))
# Cant ask eval to take care of this without introducing lambda expr, hence will just hard code the logic

# Careful we are working with dicts not arrays....
def update_rate_config(conf : Configuation_expr, state : DRSState, dim : Dimensions, vars : DRSVars, params : Parameters, ctrl : ControlVars):
    env = build_env(state, vars, params, ctrl)

    column_key = str(int(state.drs_RateConfigurationNumber))
    crossing_idx = int(state.drs_ThresholdCrossingLevelOrTimerNumber)
    if crossing_idx <= 0:
        return state.drs_RateConfigurationNumber
    
    if state.drs_ThresholdIsCrossedByTimer == 0:
        idx = min(crossing_idx, dim.dim_NumberOfLevels)
        row_label = vars.level_labels[idx-1]
        if state.drs_DirectionOfThresholdCrossing == -1:
            expr = get_matrix_expr(conf.confExString_LowerLevelResultantRateConfiguration, row_label, column_key, "")
        else:
            expr = get_matrix_expr(conf.confExString_UpperLevelResultantRateConfiguration, row_label, column_key, "")
    else:
        idx = min(crossing_idx, dim.dim_NumberOfTimerss)
        row_label = vars.timer_labels[idx-1]
        if state.drs_DirectionOfThresholdCrossing == -1:
            expr = get_matrix_expr(conf.confExString_LowerTimerResultantRateConfiguration, row_label, column_key, "")
        else:
            expr = get_matrix_expr(conf.confExString_UpperTimerResultantRateConfiguration, row_label, column_key, "")

    # clean expr, think of "" cells
    s = str(expr).strip()
    if s == "" or s == '""':
        return state.drs_RateConfigurationNumber
    
    new_column_key = int(evaluate_expr(expr, env))
    state.drs_RateConfigurationNumber = new_column_key

    return new_column_key

