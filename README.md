# run_concurrently — Java runner for DRS simulations

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