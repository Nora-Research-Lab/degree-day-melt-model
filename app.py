import os

os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib

matplotlib.use("Agg")

import gradio as gr
from degree_day_melt_model import (
    compute_degree_day_melt,
    make_error_plot,
    make_melt_plot,
    parse_temperature_series,
)


def calculate(temp_text, melt_factor, threshold):
    try:
        temperatures = parse_temperature_series(temp_text)
        result = compute_degree_day_melt(temperatures, melt_factor, threshold)
        fig = make_melt_plot(result)

        return (
            round(result["total_pdd"], 1),
            int(round(result["total_melt"])),
            result["classification"],
            fig,
        )
    except Exception as exc:
        try:
            fig = make_error_plot(str(exc))
        except Exception:
            fig = None

        return None, None, str(exc), fig


with gr.Blocks(title="Degree-Day Melt Model") as demo:
    gr.Markdown("# Degree-Day Melt Model")

    temp_box = gr.Textbox(
        label="Daily mean temperatures (°C)",
        lines=30,
        placeholder=(
            "Enter one value per line or comma-separated values, e.g.:\n"
            "-2.0\n"
            "0.5\n"
            "3.2\n"
            "..."
        ),
    )

    with gr.Row():
        melt_factor = gr.Number(
            label="Melt factor (mm/°C/day)",
            value=5.0,
            step=0.1,
        )
        threshold = gr.Number(
            label="Threshold temperature (°C)",
            value=0.0,
            step=0.1,
        )

    gr.Markdown("Typical melt factors: snow 3–5, ice 6–8.")

    calc_btn = gr.Button("Calculate")

    with gr.Row():
        total_pdd = gr.Number(
            label="Total Positive Degree-Days (°C·days)",
            precision=1,
        )
        total_melt = gr.Number(
            label="Cumulative Melt (mm w.e.)",
            precision=0,
        )
        classification = gr.Textbox(label="Melt Season Classification")

    plot = gr.Plot(label="Daily and Cumulative Melt")

    calc_btn.click(
        fn=calculate,
        inputs=[temp_box, melt_factor, threshold],
        outputs=[total_pdd, total_melt, classification, plot],
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
