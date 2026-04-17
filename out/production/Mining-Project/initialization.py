from drs_env import build_env
from init_data import Dimensions, DRSState, DRSVars, Configuation_expr
from config import Parameters, ControlVars
from evaluate_expr import evaluate_expr

def initialization_state(conf : Configuation_expr, dim: Dimensions , vars : DRSVars, params : Parameters, ctrl : ControlVars):
    state = DRSState()
    state.init(dim)
    
    state.drs_TimeOfPreviousDRSUpdate = 0.0
    state.TNOW = 0.0

    # init the RateConfigurationNumber
    state.drs_RateConfigurationNumber = int(evaluate_expr(conf.confExString_InitialRateConfigurationNumber, {}))
    env = build_env(state, vars, params, ctrl)
    
    # init levels, timers, dynamic numerals, cat
    # Maybe cast if needed, test later
    for i, label in enumerate(vars.level_labels):
        expr = str(conf.confExString_InitialLevelValue.get(label))
        state.drs_Level[i] = float(evaluate_expr(expr, env))

    for i, label in enumerate(vars.timer_labels):
        expr = str(conf.confExString_InitialTimerValue.get(label, "0"))
        state.drs_Timer[i] = float(evaluate_expr(expr, env))

    for i, label in enumerate(vars.dynamic_numerical_labels):
        expr = str(conf.confExString_InitialDiscretelyDynamicalNumericalVariableValue.get(label))
        state.drs_DiscretelyDynamicalNumericalVariable[i] = float(evaluate_expr(expr, env))

    for i, label in enumerate(vars.categorical_labels):
        state.drs_CategoricalVariable[i] = str(conf.confExString_InitialCategoricalVariableValue.get(label))

    return state