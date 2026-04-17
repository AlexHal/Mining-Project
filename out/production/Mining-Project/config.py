from dataclasses import dataclass
from typing import Tuple


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
    parameterVector_GeostatisticalModelParameters: Tuple[float, ...] = (
        30000.0,
        50000.0,
        30.0,
        30.0,
        5.0,
        1.0,
    )


@dataclass
class ControlVars:
    controlVariable_CriticalOre2Level: float = 20000
    controlVariable_TargetOreStockLevel: float = 60000
    controlVariable_DurationOfContingencySegments: float = 1
