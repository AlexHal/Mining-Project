import threading
import tkinter as tk
from tkinter import messagebox, ttk

from bayesian_stockout_regression import optimize_critical_ore2_level
from DRS_Simulator import run_simulation
from config import ControlVars, Parameters
from init_data import DRSVars, Dimensions, load_confExStrings_from_excel


class ControlOptimizerUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Mine Control Variable Optimizer")
        self.root.geometry("800x480")

        self.conf = load_confExStrings_from_excel("MiningSystemDRS_ConfExStrings_v4.xlsx")
        self.dim = Dimensions()
        self.vars = DRSVars()
        self.params = Parameters()

        defaults = ControlVars()
        param_defaults = Parameters()

        self.critical_var = tk.StringVar(value=str(defaults.controlVariable_CriticalOre2Level))
        self.target_var = tk.StringVar(value=str(defaults.controlVariable_TargetOreStockLevel))
        self.contingency_var = tk.StringVar(value=str(defaults.controlVariable_DurationOfContingencySegments))

        self.initial_points_var = tk.StringVar(value="5")
        self.steps_var = tk.StringVar(value="20")
        self.replications_var = tk.StringVar(value="3")
        self.grid_size_var = tk.StringVar(value="250")
        self.length_scale_var = tk.StringVar(value="8000")
        self.noise_var = tk.StringVar(value="1e-6")

        self.warmup_var = tk.StringVar(value=str(param_defaults.parameter_OreToBeExtractedDuringWarmingPeriod))
        self.total_ore_var = tk.StringVar(value=str(param_defaults.parameter_TotalOreToBeExtracted))
        self.prod_campaign_var = tk.StringVar(value=str(param_defaults.parameter_DurationOfProductionCampaigns))
        self.shutdown_var = tk.StringVar(value=str(param_defaults.parameter_DurationOfShutdowns))
        self.mode_a_ore1_rate_var = tk.StringVar(value=str(param_defaults.parameter_ModeAOre1MillingRate))
        self.mode_b_ore1_rate_var = tk.StringVar(value=str(param_defaults.parameter_ModeBOre1MillingRate))

        self.status_var = tk.StringVar(value="Ready")
        self.result_var = tk.StringVar(value="No run yet.")

        self.optimize_button: ttk.Button
        self.test_button: ttk.Button
        self.build_layout()

    def build_layout(self) -> None:
        container = ttk.Frame(self.root, padding=16)
        container.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=0)
        container.rowconfigure(1, weight=0)

        controls_frame = ttk.LabelFrame(container, text="Control Variables", padding=12)
        controls_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 12))

        self.labeled_entry(controls_frame, "CriticalOre2Level", self.critical_var, 0)
        self.labeled_entry(controls_frame, "TargetOreStockLevel", self.target_var, 1)
        self.labeled_entry(controls_frame, "DurationOfContingencySegments", self.contingency_var, 2)

        params_frame = ttk.LabelFrame(container, text="Parameters (used for test run and optimization)", padding=12)
        params_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 12))

        self.labeled_entry(params_frame, "OreToBeExtractedDuringWarmingPeriod", self.warmup_var, 0)
        self.labeled_entry(params_frame, "TotalOreToBeExtracted", self.total_ore_var, 1)
        self.labeled_entry(params_frame, "DurationOfProductionCampaigns", self.prod_campaign_var, 2)
        self.labeled_entry(params_frame, "DurationOfShutdowns", self.shutdown_var, 3)
        self.labeled_entry(params_frame, "ModeAOre1MillingRate", self.mode_a_ore1_rate_var, 4)
        self.labeled_entry(params_frame, "ModeBOre1MillingRate", self.mode_b_ore1_rate_var, 5)

        opt_frame = ttk.LabelFrame(container, text="Optimization Settings", padding=12)
        opt_frame.grid(row=1, column=0, sticky="ew")

        self.labeled_entry(opt_frame, "Initial Points", self.initial_points_var, 0)
        self.labeled_entry(opt_frame, "Optimization Steps", self.steps_var, 1)
        self.labeled_entry(opt_frame, "Replications / Point", self.replications_var, 2)
        self.labeled_entry(opt_frame, "Candidate Grid Size", self.grid_size_var, 3)
        self.labeled_entry(opt_frame, "Length Scale", self.length_scale_var, 4)
        self.labeled_entry(opt_frame, "Observation Noise", self.noise_var, 5)

        right_bottom = ttk.Frame(container)
        right_bottom.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        right_bottom.columnconfigure(0, weight=1)
        right_bottom.rowconfigure(1, weight=1)

        actions = ttk.Frame(right_bottom)
        actions.grid(row=0, column=0, sticky="w", pady=(0, 10))

        self.test_button = ttk.Button(actions, text="Run Test Simulation", command=self.on_test_run)
        self.test_button.pack(side=tk.LEFT)

        self.optimize_button = ttk.Button(actions, text="Run Optimization", command=self.on_optimize)
        self.optimize_button.pack(side=tk.LEFT, padx=(8, 0))

        status_label = ttk.Label(actions, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, padx=(12, 0))

        result_frame = ttk.LabelFrame(right_bottom, text="Result", padding=12)
        result_frame.grid(row=1, column=0, sticky="nsew")

        result_label = ttk.Label(result_frame, textvariable=self.result_var, justify=tk.LEFT)
        result_label.pack(anchor=tk.W)

    def labeled_entry(self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=4)
        ttk.Entry(parent, textvariable=variable, width=22).grid(row=row, column=1, sticky=tk.W, pady=4, padx=(10, 0))

    def read_current_config(self) -> tuple[ControlVars, Parameters]:
        critical = float(self.critical_var.get())
        target = float(self.target_var.get())
        contingency = float(self.contingency_var.get())

        warmup = float(self.warmup_var.get())
        total_ore = float(self.total_ore_var.get())
        production_campaign = float(self.prod_campaign_var.get())
        shutdown = float(self.shutdown_var.get())
        mode_a_ore1_rate = float(self.mode_a_ore1_rate_var.get())
        mode_b_ore1_rate = float(self.mode_b_ore1_rate_var.get())

        if target <= 0:
            raise ValueError("TargetOreStockLevel must be > 0.")
        if critical < 0:
            raise ValueError("CriticalOre2Level must be >= 0.")
        if critical > target:
            raise ValueError("CriticalOre2Level must be <= TargetOreStockLevel.")

        ctrl = ControlVars(
            controlVariable_CriticalOre2Level=critical,
            controlVariable_TargetOreStockLevel=target,
            controlVariable_DurationOfContingencySegments=contingency,
        )

        params = Parameters(
            parameter_OreToBeExtractedDuringWarmingPeriod=warmup,
            parameter_TotalOreToBeExtracted=total_ore,
            parameter_DurationOfProductionCampaigns=production_campaign,
            parameter_DurationOfShutdowns=shutdown,
            parameter_ModeAOre1MillingRate=mode_a_ore1_rate,
            parameter_ModeBOre1MillingRate=mode_b_ore1_rate,
            parameter_ModeAOre2MillingRate=self.params.parameter_ModeAOre2MillingRate,
            parameter_ModeAContingencyOre1MillingRate=self.params.parameter_ModeAContingencyOre1MillingRate,
            parameter_ModeBOre2MillingRate=self.params.parameter_ModeBOre2MillingRate,
            parameter_ModeBContingencyOre2MillingRate=self.params.parameter_ModeBContingencyOre2MillingRate,
            parameterVector_GeostatisticalModelParameters=self.params.parameterVector_GeostatisticalModelParameters,
        )

        return ctrl, params

    def on_test_run(self) -> None:
        try:
            ctrl, params = self.read_current_config()
        except ValueError as ex:
            messagebox.showerror("Invalid Input", str(ex))
            return

        self.test_button.config(state=tk.DISABLED)
        self.optimize_button.config(state=tk.DISABLED)
        self.status_var.set("Running test simulation...")
        self.result_var.set("Running test simulation with current config values.")

        def run_job() -> None:
            try:
                result = run_simulation(
                    config=self.conf,
                    dim=self.dim,
                    vars=self.vars,
                    params=params,
                    ctrl=ctrl,
                    create_plots=False,
                )
                self.root.after(0, lambda: self.on_test_done(result))
            except Exception as ex:
                err = str(ex)
                self.root.after(0, lambda msg=err: self.on_test_failed(msg))

        threading.Thread(target=run_job, daemon=True).start()

    def on_optimize(self) -> None:
        try:
            ctrl, params = self.read_current_config()

            initial_points = int(self.initial_points_var.get())
            steps = int(self.steps_var.get())
            replications = int(self.replications_var.get())
            grid_size = int(self.grid_size_var.get())
            length_scale = float(self.length_scale_var.get())
            noise = float(self.noise_var.get())
        except ValueError as ex:
            messagebox.showerror("Invalid Input", str(ex))
            return

        self.test_button.config(state=tk.DISABLED)
        self.optimize_button.config(state=tk.DISABLED)
        self.status_var.set("Optimizing...")
        self.result_var.set("Running simulations. This can take a while.")

        def run_job() -> None:
            try:
                result = optimize_critical_ore2_level(
                    conf=self.conf,
                    dim=self.dim,
                    vars=self.vars,
                    params=params,
                    ctrl=ctrl,
                    initial_points=initial_points,
                    optimization_steps=steps,
                    replications_per_point=replications,
                    candidate_grid_size=grid_size,
                    length_scale=length_scale,
                    observation_noise=noise,
                )
                self.root.after(0, lambda: self.on_optimize_done(result))
            except Exception as ex:
                err = str(ex)
                self.root.after(0, lambda msg=err: self.on_optimize_failed(msg))

        threading.Thread(target=run_job, daemon=True).start()

    def on_optimize_done(self, result: dict) -> None:
        best_critical = float(result["best_critical_ore2_level"])
        best_output = float(result["best_mine_output"])
        samples_count = len(result.get("samples", []))

        self.critical_var.set(f"{best_critical:.4f}")

        self.result_var.set(
            "Optimization complete.\n"
            f"Best CriticalOre2Level: {best_critical:.4f}\n"
            f"Best Mine Output (Throughput): {best_output:.6f}\n"
            f"Sampled Points: {samples_count}"
        )
        self.status_var.set("Done")
        self.test_button.config(state=tk.NORMAL)
        self.optimize_button.config(state=tk.NORMAL)

    def on_optimize_failed(self, error_message: str) -> None:
        self.status_var.set("Failed")
        self.test_button.config(state=tk.NORMAL)
        self.optimize_button.config(state=tk.NORMAL)
        messagebox.showerror("Optimization Error", error_message)

    def on_test_done(self, result: dict) -> None:
        stats = result["output_statistics"]
        self.result_var.set(
            "Test simulation complete.\n"
            f"Throughput: {float(stats.Throughput):.6f}\n"
            f"PortionOfTimeInModeA: {float(stats.PortionOfTimeInModeA):.4f}\n"
            f"PortionOfTimeInModeB: {float(stats.PortionOfTimeInModeB):.4f}\n"
            f"PortionOfTimeInShutdown: {float(stats.PortionOfTimeInShutdown):.4f}"
        )
        self.status_var.set("Done")
        self.test_button.config(state=tk.NORMAL)
        self.optimize_button.config(state=tk.NORMAL)

    def on_test_failed(self, error_message: str) -> None:
        self.status_var.set("Failed")
        self.test_button.config(state=tk.NORMAL)
        self.optimize_button.config(state=tk.NORMAL)
        messagebox.showerror("Test Run Error", error_message)


def main() -> None:
    root = tk.Tk()
    app = ControlOptimizerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
