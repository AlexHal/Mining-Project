from typing import Dict, Any
from init_data import  DRSState, DRSVars, Parameters, ControlVars


def build_env(state : DRSState, vars : DRSVars, params : Parameters, ctrl : ControlVars) -> Dict[str, Any]:
    env: Dict[str, Any] = {}

    env["drs_RateConfigurationNumber"] = state.drs_RateConfigurationNumber
    env["drs_TimeOfPreviousDRSUpdate"] = state.drs_TimeOfPreviousDRSUpdate
    env["drs_DurationUntilThresholdCrossing"] = state.drs_DurationUntilThresholdCrossing
    env["drs_ThresholdCrossingLevelOrTimerNumber"] = state.drs_ThresholdCrossingLevelOrTimerNumber
    env["drs_ThresholdIsCrossedByTimer"] = state.drs_ThresholdIsCrossedByTimer
    env["drs_DirectionOfThresholdCrossing"] = state.drs_DirectionOfThresholdCrossing

    env["TNOW"] = state.TNOW

    # Dynamic vars
    for i, label in enumerate(vars.level_labels):
        env[label] = state.drs_Level[i]
    for i, label in enumerate(vars.timer_labels):
        env[label] = state.drs_Timer[i]
    for i, label in enumerate(vars.ddnv_labels):
        env[label] = state.drs_DiscretelyDynamicalNumericalVariable[i]
    for i, label in enumerate(vars.categorical_labels):
        env[label] = state.drs_CategoricalVariable[i]

# Test which i need here
    env.update(params.__dict__)
    env.update(ctrl)

    return env