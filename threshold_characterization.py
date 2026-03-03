from init_data import Dimensions, DRSState, DRSVars, Parameters, ControlVars, Configuation_expr
from evaluate_expr import evaluate_expr
from drs_env import build_env
from helpers import get_matrix_expr



def characterize_next_threshold(conf : Configuation_expr, state : DRSState, dim : Dimensions, vars : DRSVars, params : Parameters, ctrl : ControlVars):
    
    # Build env and init vals
    env = build_env(state, vars, params, ctrl)
    column_key = str(int(state.drs_RateConfigurationNumber))
    
    min_duration = float('inf')
    crossing_index = 0
    is_timer = 0
    
    # check levels
    for i in range(dim.dim_NumberOfLevels):
        try:
            row_label = vars.level_labels[i]
            rate = float(evaluate_expr(get_matrix_expr(conf.confExString_LevelRate, row_label, column_key, "0"), env))
            current_level = state.drs_Level[i]
            
            if rate < 0:
                threshold = float(evaluate_expr(get_matrix_expr(conf.confExString_LowerLevelThreshold, row_label, column_key, "0"), env))
                duration = max(0, (threshold - current_level) / rate)
            elif rate > 0:
                threshold = float(evaluate_expr(get_matrix_expr(conf.confExString_UpperLevelThreshold, row_label, column_key, "0"), env))
                duration = max(0, (threshold - current_level) / rate)
            else:
                continue
            
            if duration < min_duration:
                min_duration = duration
                crossing_index = i + 1
                is_timer = 0
        except:
            pass
    
    # search timers
    for i in range(dim.dim_NumberOfTimerss):
        try:
            row_label = vars.timer_labels[i]
            rate = float(evaluate_expr(get_matrix_expr(conf.confExString_TimerRate, row_label, column_key, "0"), env))
            current_timer = state.drs_Timer[i]
            
            if rate < 0:
                threshold = float(evaluate_expr(get_matrix_expr(conf.confExString_LowerTimerThreshold, row_label, column_key, "0"), env))
                duration = max(0, (threshold - current_timer) / rate)
            elif rate > 0:
                threshold = float(evaluate_expr(get_matrix_expr(conf.confExString_UpperTimerThreshold, row_label, column_key, "0"), env))
                duration = max(0, (threshold - current_timer) / rate)
            else:
                continue
            
            if duration < min_duration:
                min_duration = duration
                crossing_index = i + 1
                is_timer = 1
        except:
            pass
    
    # update state
    # print(min_duration)
    state.drs_DurationUntilThresholdCrossing = min_duration if min_duration != float('inf') else 99999.0
    state.drs_ThresholdCrossingLevelOrTimerNumber = crossing_index
    state.drs_ThresholdIsCrossedByTimer = is_timer
    
    # determine direction

    try:
        if is_timer == 0:
            row_label = vars.level_labels[crossing_index - 1]
            rate = float(evaluate_expr(get_matrix_expr(conf.confExString_LevelRate, row_label, column_key, "0"), env))
        else:
            row_label = vars.timer_labels[crossing_index - 1]
            rate = float(evaluate_expr(get_matrix_expr(conf.confExString_TimerRate, row_label, column_key, "0"), env))
        
        state.drs_DirectionOfThresholdCrossing = -1 if rate < 0 else (1 if rate > 0 else 0)
    except:
        state.drs_DirectionOfThresholdCrossing = 0

    return state 
