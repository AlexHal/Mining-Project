# run_concurrently — Java runner for DRS simulations

Python Config
- Simulation constants are now defined in `config.py`:
	- `Parameters`
	- `ControlVars`

Bayesian Stockout Regression
- Use `bayesian_stockout_regression.py` to tune `controlVariable_CriticalOre2Level`.
- The optimizer:
	- Runs repeated simulations at candidate critical-ore2 levels.
	- Computes a stockout score from `Ore2Stock_Level` deficits.
	- Fits a Gaussian-process Bayesian regression surrogate.
	- Selects new candidates with expected improvement.

Run optimizer
```bash
python bayesian_stockout_regression.py
```

Control Variable UI
- Desktop UI to set control variables and run optimization.
- Constraint enforced in UI: `CriticalOre2Level <= TargetOreStockLevel`.
- Optimizer bound is also set to `[0, TargetOreStockLevel]`.

Run UI
```bash
python control_optimizer_ui.py
```

Overview
- Small Java helper that runs `DRS_Simulator.py` multiple times in parallel 

Compile
```bash
javac run_concurrently.java
```

Run
```bash
# Usage: java run_concurrently <numRuns> <numThreads> [pythonCmd]
# Example: run 20 independent sims using 4 worker threads, calling `python` from PATH
java run_concurrently 20 4 python

# If you need to call a specific python executable, pass its path:
java run_concurrently 50 8 "C:/Python/Python313/python.exe"
```