from dataclasses import dataclass
from init_data import DRSState, DRSVars
from config import Parameters


@dataclass
class OutputStatistics:
    PortionOfTimeInModeA: float
    PortionOfTimeInModeAContingency: float
    PortionOfTimeInModeAMineSurging: float
    PortionOfTimeInModeB: float
    PortionOfTimeInModeBContingency: float
    PortionOfTimeInModeBMineSurging: float
    PortionOfTimeInShutdown: float
    Throughput: float

# Avoid div by 0
def safe_div(numerator: float, denominator: float) -> float:
    if denominator == 0.0:
        return 0.0
    return numerator / denominator


# simple computation
def compute_output_statistics(state: DRSState, vars: DRSVars, params: Parameters) -> OutputStatistics:
    timer_index = {label: i for i, label in enumerate(vars.timer_labels)}
    # print(timer_index)
    time_mode_a = float(state.drs_Timer[timer_index["TimeInModeA_Timer"]])
    time_mode_a_contingency = float(state.drs_Timer[timer_index["TimeInModeAContingency_Timer"]])
    time_mode_a_mine_surging = float(state.drs_Timer[timer_index["TimeInModeAMineSurging_Timer"]])
    time_mode_b = float(state.drs_Timer[timer_index["TimeInModeB_Timer"]])
    time_mode_b_contingency = float(state.drs_Timer[timer_index["TimeInModeBContingency_Timer"]])
    time_mode_b_mine_surging = float(state.drs_Timer[timer_index["TimeInModeBMineSurging_Timer"]])
    time_shutdown = float(state.drs_Timer[timer_index["TimeInShutdown_Timer"]])

    total_time_in_modes = (
        time_mode_a
        + time_mode_a_contingency
        + time_mode_a_mine_surging
        + time_mode_b
        + time_mode_b_contingency
        + time_mode_b_mine_surging
        + time_shutdown
    )

    total_time_excluding_shutdown = (
        time_mode_a
        + time_mode_a_contingency
        + time_mode_a_mine_surging
        + time_mode_b
        + time_mode_b_contingency
        + time_mode_b_mine_surging
    )

    ore_extraction_level = float(state.drs_Level[0])
    ore_extracted_after_warmup = ore_extraction_level - float(params.parameter_OreToBeExtractedDuringWarmingPeriod)

# So far feels like i have an error in my stats, need to debug with arena
    return OutputStatistics(
        PortionOfTimeInModeA=safe_div(time_mode_a, total_time_in_modes),
        PortionOfTimeInModeAContingency=safe_div(time_mode_a_contingency, total_time_in_modes),
        PortionOfTimeInModeAMineSurging=safe_div(time_mode_a_mine_surging, total_time_in_modes),
        PortionOfTimeInModeB=safe_div(time_mode_b, total_time_in_modes),
        PortionOfTimeInModeBContingency=safe_div(time_mode_b_contingency, total_time_in_modes),
        PortionOfTimeInModeBMineSurging=safe_div(time_mode_b_mine_surging, total_time_in_modes),
        PortionOfTimeInShutdown=safe_div(time_shutdown, total_time_in_modes),
        Throughput=safe_div(ore_extracted_after_warmup, total_time_excluding_shutdown),
    )
