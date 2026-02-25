from dataclasses import dataclass, field
from typing import Dict, List, Tuple


# Expressions
@dataclass
class Configuation_expr:

    # Scalar
    confExString_TerminatingCondition: str
    confExString_InitialRateConfigurationNumber: str = "1"
    
    # Vector // we must init to empty // dict[label] -> expr_str
    confExString_InitialLevelValue: Dict[str, str] = field(default_factory=dict)
    confExString_InitialTimerValue: Dict[str, str] = field(default_factory=dict)
    confExString_InitialDiscretelyDynamicalNumericalVariableValue: Dict[str, str] = field(default_factory=dict)
    confExString_InitialCategoricalVariableValue: Dict[str, str] = field(default_factory=dict)

    # Matrix dict[row_label][col_label] -> expr_str
    confExString_LevelRate: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_LowerLevelThreshold: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_UpperLevelThreshold: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_LowerLevelResultantRateConfiguration: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_UpperLevelResultantRateConfiguration: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_LowerLevelAssignmentAddress: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_UpperLevelAssignmentAddress: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_TimerRate: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_LowerTimerThreshold: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_UpperTimerThreshold: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_LowerTimerResultantRateConfiguration: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_UpperTimerResultantRateConfiguration: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_LowerTimerAssignmentAddress: Dict[str, Dict[str, str]] = field(default_factory=dict)
    confExString_UpperTimerAssignmentAddress: Dict[str, Dict[str, str]] = field(default_factory=dict)
    
    confExString_AssignmentSequence: Dict[str, Dict[str, str]] = field(default_factory=dict)


#order matters since we do drs_timer(int)
#Now we want to be able to search here quickly. sooo maybe a dict with L/T/N/C as a first char.  similar to the last decide of the model
# may simplify some work later on 
@dataclass(frozen=True)
class DRSVars:

    # Levels
    level_labels: Tuple[str, ...] = (
        "OreExtraction_Level",
        "OreExtractedFromCurrentParcel_Level",
        "OreStock_Level",
        "Ore1Stock_Level",
        "Ore2Stock_Level",
    )

    # Timers
    timer_labels: Tuple[str, ...] = (
        "TimeExecutedInCurrentCampaignOrShutdown_Timer",
        "TimeExecutedInCurrentContingencySegment_Timer",
        "TimeInModeA_Timer",
        "TimeInModeAContingency_Timer",
        "TimeInModeAMineSurging_Timer",
        "TimeInModeB_Timer",
        "TimeInModeBContingency_Timer",
        "TimeInModeBMineSurging_Timer",
        "TimeInShutdown_Timer"
    )
    
    dynamic_numerical_labels: Tuple[str, ...] = (
        "MassOfCurrentParcel",
        "PercentageOfOre2InCurrentParcel",
        "NextParcelIsNewFacies"
    )

    # Since we had cat. in the decide of the last part of the model
    categorical_labels: Tuple[str, ...] = ("DummerCategorical")

    def build_dicts(self) -> Dict[str, Tuple[str, int]]:
        # L : level, T : Timer, N : dynamic.., C : catego.

        m: Dict[str, Tuple[str, int]] = {}
        for i, s in enumerate(self.level_labels):
            m[s] = ("L", i)
        for i, s in enumerate(self.timer_labels):
            m[s] = ("T", i)
        for i, s in enumerate(self.dynamic_numerical_labels):
            m[s] = ("N", i)
        for i, s in enumerate(self.categorical_labels):
            m[s] = ("C", i)

        return m




# Variables

@dataclass
class Dimensions:
    dim_NumberOfLevels: int = 5
    dim_NumberOfTimerss: int = 9
    dim_NumberOfDiscretelyDynamicalNumericalVariabless: int = 3
    dim_NumberOfCategoricalVariabless: int # was 1 on arena, should be 0/null will test all and see
    dim_NumberOfRateConfigurationss: int = 7
    dim_NumberOfAssignmentSequenceAddressess: int = 6
    dim_MaxLengthOfAssignmentSequences: int = 7


@dataclass
class DRSState:
    drs_RateConfigurationNumber: int = 1
    drs_TimeOfPreviousDRSUpdate: float = 0.0 # we start at 0
    drs_DurationUntilThresholdCrossing: float = 99999.0
    drs_ThresholdCrossingLevelOrTimerNumber: int
    drs_ThresholdIsCrossedByTimer: int
    drs_DirectionOfThresholdCrossing: int
    
    drs_Level: List[float]
    drs_Timer: List[float]
    drs_DiscretelyDynamicalNumericalVariable: List[float]
    drs_CategoricalVariable: List[str]

    TNOW: float = 0.0

    def init(self, dim : Dimensions):
        self.drs_Level = [0.0] * dim.dim_NumberOfLevels
        self.drs_Timer = [0.0] * dim.dim_NumberOfLevels
        self.drs_DiscretelyDynamicalNumericalVariable = [0.0] * dim.dim_NumberOfDiscretelyDynamicalNumericalVariabless
        self.drs_CategoricalVariable = [0.0] * dim.dim_NumberOfCategoricalVariabless


@dataclass
class Parameters:
    parameter_OreToBeExtractedDuringWarmingPeriod: float = 600000
    parameter_TotalOreToBeExtracted: float = 6600000
    parameter_DurationOfProductionCampaigns: float = 34
    parameter_DurationOfShutdowns: float = 1
    parameter_ModeAOre1MillingRate: float = 3600
    parameter_ModeAOre2MillingRate: float = 2400
    parameter_ModeAContingencyOre1MillingRate: float = 3900 
    parameter_ModeBOre1MillingRate: float = 4600
    parameter_ModeBOre2MillingRate: float = 800
    parameter_ModeBContingencyOre2MillingRate: float = 2500 
    parameterVector_GeostatisticalModelParameters: Tuple[float, ...] = (30000.0, 50000.0, 30.0, 30.0, 5.0, 1.0)

@dataclass
class ControlVars:
    controlVariable_CriticalOre2Level: float = 20400
    controlVariable_TargetOreStockLevel: float = 60000
    controlVariable_DurationOfContingencySegments: float = 1