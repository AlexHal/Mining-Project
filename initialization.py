from drs_env import build_env
from init_data import Dimensions, DRSState, DRSVars, Parameters, ControlVars, Configuation_expr
from evaluate_expr import evaluate_expr

def initialization_state(conf : Configuation_expr, dim: Dimensions , vars : DRSVars, params : Parameters, ctrl : ControlVars):
    state = DRSState()
    state.init(dim)
    
    state.drs_TimeOfPreviousDRSUpdate = 0.0
    state.TNOW = 0.0

    # init the RateConfigurationNumber
    state.drs_RateConfigurationNumber = int(evaluate_expr(conf.confExString_InitialRateConfigurationNumber))
    env = build_env(state, vars, params, ctrl)
    
    # init levels, timers, dynamic numerals, cat
    # Maybe cast if needed, test later
    for i, label in enumerate(vars.level_labels):
        expr = conf.confExString_InitialLevelValue[label]
        state.drs_Level[i] = evaluate_expr(expr)

    for i, label in enumerate(vars.timer_labels):
        expr = conf.confExString_InitialTimerValue[label]
        state.drs_Level[i] = evaluate_expr(expr)

    for i, label in enumerate(vars.dynamic_numerical_labels):
        expr = conf.confExString_InitialDiscretelyDynamicalNumericalVariableValue[label]
        state.drs_DiscretelyDynamicalNumericalVariable = evaluate_expr(expr)

    for i, label in enumerate(vars.categorical_labels):
        # expr = conf.confExString_InitialCategoricalVariableValue[label]
        # state.drs_CategoricalVariable[i] = evaluate_expr(expr)

        state.drs_CategoricalVariable[i] = conf.confExString_InitialCategoricalVariableValue[label]

    return state

