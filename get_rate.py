# get 

# OreExtraction_Rate
# OreExtractedFromCurrentParcel_Rate
# OreStock_Rate
# Ore1Stock_Rate
# Ore2Stock_Rate

# TimeExecutedInCurrentCampaignOrShutdown_Rate
# TimeExecutedInCurrentContingencySegment_Rate
# TimeInModeA_Rate
# TimeInModeAContingency_Rate
# TimeInModeAMineSurging_Rate
# TimeInModeB_Rate
# TimeInModeBContingency_Rate
# TimeInModeBMineSurging_Rate
# TimeInShutdown_Rate

# Must add error handling

from init_data import Configuation_expr, DRSVars
from evaluate_expr import evaluate_expr
from typing import Dict

def get_level_rate(conf: Configuation_expr, vars: DRSVars, level_index_1based: int, rate_config_name: str, env: Dict[str, any]):
    level_label =  vars.level_labels[level_index_1based - 1]
    expr = conf.confExString_LevelRate[level_label][rate_config_name]
    return evaluate_expr(expr)


def get_timer_rate(conf: Configuation_expr, vars: DRSVars, level_index_1based: int, rate_config_name: str, env: Dict[str, any]):
    level_label =  vars.level_labels[level_index_1based - 1]
    expr = conf.confExString_LevelRate[level_label][rate_config_name]
    return evaluate_expr(expr)