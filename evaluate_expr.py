import math
import arena_to_python_expr
from typing import Dict
# Eval some simple arena operations
# TODO: think of the probability distributions
def MX(*args: float) -> float:
    return max(args)

def MN(*args: float) -> float:
    return min(args)

def ABS(x: float) -> float:
    return abs(x)

def Len(s: str) -> int:
    return len(s)

# A lil unsure will have to do some testing on a small arena model
def Mid(s: str, start_index : float, count : float) -> str: 
    i = max(0, int(start_index) - 1)
    return s[i:i+int(count)]


_ALLOWED_NAMES = {
    #math opp we have translated
    "ABS": ABS,
    "MX": MX,
    "MN": MN,
    "Len": Len,
    "Mid": Mid,
    "math": math,
}


# Must take into acount the current "state" of the simulation ie the curent vals of vars
def evaluate_expr(expr: str, env: Dict[str, any] = None) -> any :
    if env is None:
        env = {}
    
    to_eval = arena_to_python_expr(expr)

    # Permit normal opps
    # permit the opps we translated

    globals = {"__builtins__": {}} # we allow no normal opp only the ones we define
    globals.update(_ALLOWED_NAMES)

    return eval(to_eval, globals, env)



