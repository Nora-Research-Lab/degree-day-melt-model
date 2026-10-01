import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def parse_temperature_series(text):
    if text is None:
        raise ValueError("Temperature series is empty.")

    text = text.replace("−", "-").replace(" ", " ")
    tokens = text.replace(",", " ").replace(";", " ").split()

    temperatures = []
    for token in tokens:
        token = token.strip()
        if not token:
            continue

        try:
            value = float(token)
        except ValueError as exc:
            raise ValueError(f"Malformed temperature value: {token}") from exc

        if not math.isfinite(value):
            raise ValueError(f"Non-finite temperature value: {token}")

        temperatures.append(value)

    if not temperatures:
        raise ValueError("Temperature series is empty.")

    return temperatures


def classify_melt(total_melt_mm):
    if total_melt_mm < 100:
        return "Low melt season"
    if total_melt_mm <= 500:
        return "Moderate melt season"
    return "High melt season"


def compute_degree_day_melt(temperatures, melt_factor, threshold):
    if not temperatures:
        raise ValueError("Temperature series is empty.")

    try:
        melt_factor = float(melt_factor)
        threshold = float(threshold)
    except (TypeError, ValueError) as exc:
        raise ValueError("Melt factor and threshold temperature must be numeric.") from exc

    if not math.isfinite(melt_factor) or not math.isfinite(threshold):
        raise ValueError("Melt factor and threshold temperature must be finite numbers.")

    if melt_factor < 0:
        raise ValueError("Melt factor must be non-negative.")

    pdd_values = []
    melt_values = []
    cumulative_values = []
    running_melt = 0.0

    for temp in temperatures:
        try:
            temp_value = float(temp)
        except (TypeError, ValueError) as exc:
            raise ValueError("Temperature values must be finite numbers.") from exc

        if not math.isfinite(temp_value):
            raise ValueError("Temperature values must be finite numbers.")

        pdd = max(temp_value - threshold, 0.0)
        melt = melt_factor * pdd

        if not math.isfinite(pdd) or not math.isfinite(melt):
            raise ValueError("Computed degree-day or melt value is too large.")

        running_melt += melt
        if not math.isfinite(running_melt):
            raise ValueError("Cumulative melt is too large.")

        pdd_values.append(pdd)
        melt_values.append(melt)
        cumulative_values.append(running_melt)

    total_pdd = sum(pdd_values)
    total_melt = running_melt

    if not math.isfinite(total_pdd) or not math.isfinite(total_melt):
        raise ValueError("Computed melt totals are too large.")

    return {
        "total_pdd": total_pdd,
        "total_melt": total_melt,
        "classification": classify_melt(total_melt),
        "daily_melt": melt_values,
        "cumulative_melt": cumulative_values,
        "days": list(range(1, len(temperatures) + 1)),
    }


def make_melt_plot(result):
    fig, ax1 = plt.subplots(figsize=(8, 5))

    days = result["days"]
    daily_melt = result["daily_melt"]
    cumulative_melt = result["cumulative_melt"]

    ax1.bar(days, daily_melt, color="#4db8ff", alpha=0.7, label="Daily melt")
    ax1.set_xlabel("Day")
    ax1.set_ylabel("Daily melt (mm w.e.)")

    ax2 = ax1.twinx()
    ax2.plot(
        days,
        cumulative_melt,
        color="#1a1a1a",
        marker="o",
        linewidth=2,
        label="Cumulative melt",
    )
    ax2.set_ylabel("Cumulative melt (mm w.e.)")

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    ax1.set_title("Degree-Day Melt Model")
    fig.tight_layout()

    return fig


def make_error_plot(message):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.axis("off")
    ax.text(
        0.5,
        0.5,
        f"Error: {message}",
        ha="center",
        va="center",
        wrap=True,
    )
    fig.tight_layout()
    return fig
