from typing import Dict, Any
from dataclasses import asdict, is_dataclass
from init_data import DRSState, DRSVars, Parameters, ControlVars
from helpers import index_getter

#  TODO: build dynamic env once everything works.

def build_env(state: DRSState, vars: DRSVars, params: Parameters, ctrl: ControlVars = None) -> Dict[str, Any]:
    env: Dict[str, Any] = {}

    env["drs_RateConfigurationNumber"] = state.drs_RateConfigurationNumber
    env["drs_TimeOfPreviousDRSUpdate"] = state.drs_TimeOfPreviousDRSUpdate
    env["drs_DurationUntilThresholdCrossing"] = state.drs_DurationUntilThresholdCrossing
    env["drs_ThresholdCrossingLevelOrTimerNumber"] = state.drs_ThresholdCrossingLevelOrTimerNumber
    env["drs_ThresholdIsCrossedByTimer"] = state.drs_ThresholdIsCrossedByTimer
    env["drs_DirectionOfThresholdCrossing"] = state.drs_DirectionOfThresholdCrossing
    env["TNOW"] = state.TNOW
    # print(state.TNOW)
    
    
    # 1-based aray accessor only needed for DDNV given excel sheet
    # env["drs_Level"] =  index_getter(state.drs_Level)
    # print(env["drs_Level"])
    # env["drs_Timer"] =  index_getter(state.drs_Timer)
    env["drs_DiscretelyDynamicalNumericalVariable"] =  index_getter(state.drs_DiscretelyDynamicalNumericalVariable)
    # env["drs_CategoricalVariable"] =  index_getter(state.drs_CategoricalVariable)


    for i, label in enumerate(vars.level_labels):
        value = state.drs_Level[i]
        env[label] = value
        if label.endswith("_Level"):
            env[label[:-6]] = value

    for i, label in enumerate(vars.timer_labels):
        value = state.drs_Timer[i]
        env[label] = value
        if label.endswith("_Timer"):
            env[label[:-6]] = value

    for i, label in enumerate(vars.dynamic_numerical_labels):
        env[label] = state.drs_DiscretelyDynamicalNumericalVariable[i]

    for i, label in enumerate(vars.categorical_labels):
        env[label] = state.drs_CategoricalVariable[i]

    raw_params = asdict(params)
    for k, v in raw_params.items():
        # must have more logic given that one of the params is a tupple
        if isinstance(v, (list, tuple)):
            env[k] =  index_getter(v)
        else:
            env[k] = v


    env.update(asdict(ctrl))

    return env