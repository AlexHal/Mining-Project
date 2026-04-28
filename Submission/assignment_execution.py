from init_data import Dimensions, DRSState, DRSVars, Configuation_expr
from config import Parameters, ControlVars
from evaluate_expr import evaluate_expr
from drs_env import build_env


def assign_execute(conf: Configuation_expr, state: DRSState, dim: Dimensions, vars: DRSVars, params: Parameters, ctrl: ControlVars, assignment_address):

    max_len = int(dim.dim_MaxLengthOfAssignmentSequences)
    external_code_number = 0
    if assignment_address != 0:
        row = conf.confExString_AssignmentSequence.get(f"Assignment Sequence {int(assignment_address)}")
    else:
        row = {}
    for index in range(1, max_len + 1):

        command = str(list(row.values())[index-1])[1:-1] if index <= len(list(row.values())) else ""
        if command == "":
            return None  # end of sequence

        token = command[0:1]
        env = build_env(state, vars, params, ctrl)
        idx_expr = command[1:4] if len(command) >= 4 else ""
        payload = command[5:] if len(command) > 5 else ""
        target_idx = int(idx_expr)

        if token == "L":
            if 1 <= target_idx <= len(state.drs_Level):
                state.drs_Level[target_idx - 1] = float(evaluate_expr(payload, env))
        elif token == "T":
            if 1 <= target_idx <= len(state.drs_Timer):
                state.drs_Timer[target_idx - 1] = float(evaluate_expr(payload, env))
        elif token == "N":
            if 1 <= target_idx <= len(state.drs_DiscretelyDynamicalNumericalVariable):
                state.drs_DiscretelyDynamicalNumericalVariable[target_idx - 1] = float(evaluate_expr(payload, env))
        elif token == "C":
            if 1 <= target_idx <= len(state.drs_CategoricalVariable):
                state.drs_CategoricalVariable[target_idx - 1] = payload
        elif token == "E":
            external_code_number = target_idx
            run_external_code(external_code_number, state, dim, vars, params, ctrl)

    return {
        "assignment_address": assignment_address,
        "external_code_number": external_code_number,
    }



def run_external_code(code_number: int, state: DRSState, dim: Dimensions, vars: DRSVars, params: Parameters, ctrl: ControlVars):
    if code_number == 0:
        return
    if code_number == 1:
        external_code_1(state, dim, vars, params, ctrl)
    elif code_number == 2:
        external_code_2(state, dim, vars, params, ctrl)


def external_code_1(state: DRSState, dim: Dimensions, vars: DRSVars, params: Parameters, ctrl: ControlVars):
    return


def external_code_2(state: DRSState, dim: Dimensions, vars: DRSVars, params: Parameters, ctrl: ControlVars):
    return