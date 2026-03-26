from dataclasses import replace
from math import erf, exp, pi, sqrt
from random import Random
from typing import Dict, List, Tuple
import random
import numpy as np

from config import ControlVars, Parameters
from init_data import Configuation_expr, DRSVars, Dimensions
from DRS_Simulator import run_simulation



# For simplicity set variance to 1 for the whole problem


def normal_pdf(z: float) -> float:
    return exp(-0.5 * z * z) / sqrt(2.0 * pi)


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + erf(z / sqrt(2.0)))


def rbf_kernel(x1: float, x2: float, length_scale: float) -> float:
    delta = x1 - x2
    return exp(-0.5 * (delta * delta) / (length_scale * length_scale))


def expected_improvement(mean: float, best_y: float, xi: float = 0.01) -> float:
    improvement = best_y - mean - xi
    return improvement * normal_cdf(improvement) + normal_pdf(improvement)

def eval_candidate(
    conf: Configuation_expr,
    dim: Dimensions,
    vars: DRSVars,
    params: Parameters,
    ctrl: ControlVars,
    critical_ore2_level: float,
    replications: int,
    seed_base: int,
) -> float:
    # add some noise
    rng = Random(seed_base)
    seeds = [rng.randint(1, 10_000_000) for _ in range(replications)]

    objective_sum = 0.0
    for seed in seeds:
        sim_ctrl = replace(ctrl, controlVariable_CriticalOre2Level=critical_ore2_level)

        random.seed(seed)
        sim_result = run_simulation(
            config=conf,
            dim=dim,
            vars=vars,
            params=params,
            ctrl=sim_ctrl,
            create_plots=False,
        )
        throughput = float(sim_result["output_statistics"].Throughput)
        objective_sum += -float(throughput)

    return objective_sum / float(replications)


def gp_posterior_predictive(
    x_train: List[float],
    y_train: List[float],
    x_query: float,
    length_scale: float,
    noise: float,
) -> Tuple[float, float]:
    n = len(x_train)
    if n == 0:
        return 0.0
    
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    diff = x_train[:, None] - y_train[None, :]
    k_mat = np.exp(-0.5 * diff ** 2 / length_scale ** 2 )

    np.fill_diagonal(k_mat, k_mat.diagonal() + noise)

    k_star = np.exp(-0.5 * (x_train - x_query)**2 / length_scale**2)

    alpha = np.linalg.solve(k_mat, y_train).tolist()

    return float(k_star @ alpha)



def optimize_critical_ore2_level(
    conf: Configuation_expr,
    dim: Dimensions,
    vars: DRSVars,
    params: Parameters,
    ctrl: ControlVars,
    initial_points: int = 5,
    optimization_steps: int = 20,
    replications_per_point: int = 3,
    candidate_grid_size: int = 250,
    length_scale: float = 8000.0,
    observation_noise: float = 1e-6,
    random_seed: int = 42,
) -> Dict[str, object]:
    bounds = (5000.0, float(ctrl.controlVariable_TargetOreStockLevel))
    low, high = bounds
    if low >= high:
        raise ValueError("Invalid bounds: lower bound must be less than upper bound.")
    if initial_points < 2:
        raise ValueError("initial_points must be at least 2.")

    x_samples: List[float] = []
    y_samples: List[float] = []

    for i in range(initial_points):
        x = low + (high - low) * (i / float(initial_points - 1))
        y = eval_candidate(
            conf=conf,
            dim=dim,
            vars=vars,
            params=params,
            ctrl=ctrl,
            critical_ore2_level=x,
            replications=replications_per_point,
            seed_base=random_seed + i,
        )
        x_samples.append(x)
        y_samples.append(y)

    for step in range(optimization_steps):
        best_observed = min(y_samples)
        candidate_x = None
        candidate_ei = -1.0

        for grid_i in range(candidate_grid_size):
            xq = low + (high - low) * (grid_i / float(candidate_grid_size - 1))
            if any(abs(xq - x_prev) < 1e-9 for x_prev in x_samples):
                continue

            mean = gp_posterior_predictive(
                x_train=x_samples,
                y_train=y_samples,
                x_query=xq,
                length_scale=length_scale,
                noise=observation_noise,
            )
            ei = expected_improvement(mean, best_observed)
            if ei > candidate_ei:
                candidate_ei = ei
                candidate_x = xq

        if candidate_x is None:
            break

        candidate_y = eval_candidate(
            conf=conf,
            dim=dim,
            vars=vars,
            params=params,
            ctrl=ctrl,
            critical_ore2_level=candidate_x,
            replications=replications_per_point,
            seed_base=random_seed + initial_points + step,
        )
        x_samples.append(candidate_x)
        y_samples.append(candidate_y)

    best_idx = min(range(len(y_samples)), key=lambda i: y_samples[i])
    best_level = x_samples[best_idx]
    best_throughput = -y_samples[best_idx]

    return {
        "best_critical_ore2_level": best_level,
        "best_mine_output": best_throughput,
        "samples": list(zip(x_samples, y_samples)),
    }


def main() -> None:
    from init_data import load_confExStrings_from_excel

    conf = load_confExStrings_from_excel("MiningSystemDRS_ConfExStrings_v4.xlsx")
    dim = Dimensions()
    vars = DRSVars()
    params = Parameters()
    ctrl = ControlVars()


    result = optimize_critical_ore2_level(conf, dim, vars, params, ctrl)

    print("Best controlVariable_CriticalOre2Level:", result["best_critical_ore2_level"])
    print("Best mine output (Throughput):", result["best_mine_output"])

if __name__ == "__main__":
    main()
