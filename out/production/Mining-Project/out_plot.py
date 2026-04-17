import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def plot_modes(time_series: list, rate_config_series: list):
    """
    Plot 1: Modes Plot
    Stair-step series showing which mode is active over time.
      Mode A     (configs 1,2,3) -> plotted at y=3
      Mode B     (configs 4,5,6) -> plotted at y=2
      Shutdown   (config  7    ) -> plotted at y=1
    """
    rc = rate_config_series

    mode_a    = [3 * ((r == 1) + (r == 2) + (r == 3)) for r in rc]
    mode_b    = [2 * ((r == 4) + (r == 5) + (r == 6)) for r in rc]
    shutdown  = [1 * (r == 7) for r in rc]

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.step(time_series, mode_a, where="post", label="Mode A", linewidth=1.5)
    ax.step(time_series, mode_b, where="post", label="Mode B", linewidth=1.5)
    ax.step(time_series, shutdown, where="post", label="Shutdown", linewidth=1.5)

    ax.set_title("Modes Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Mode")

    ax.set_xlim(0, max(time_series) if time_series else 1000)
    ax.set_ylim(0, 4)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Shutdown", "Mode B", "Mode A"])

    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_ore_levels(time_series: list, ore_stock_series: list, ore1_stock_series: list, ore2_stock_series: list):
    """
    Plot 2: Ore Level Plot
    Three series of stockpile levels (in thousands).
    """
    total_k = [v / 1000 for v in ore_stock_series]
    ore1_k  = [v / 1000 for v in ore1_stock_series]
    ore2_k  = [v / 1000 for v in ore2_stock_series]

    fig, ax = plt.subplots(figsize=(12, 4))

    ax.plot(time_series, total_k, label="Total Ore Stockpile", linewidth=1.5)
    ax.plot(time_series, ore1_k, label="Ore 1 Stockpile", linewidth=1.5)
    ax.plot(time_series, ore2_k, label="Ore 2 Stockpile", linewidth=1.5, color="pink")

    ax.set_title("Ore Level Plot")
    ax.set_xlabel("Time")
    ax.set_ylabel("Level (thousands)")

    ax.set_xlim(0, max(time_series) if time_series else 1000)
    ax.set_ylim(0, 80)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))

    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig