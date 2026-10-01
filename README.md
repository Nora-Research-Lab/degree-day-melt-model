![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Degree-Day Melt Model
 
*For glaciologists and hydrologists: enter daily temperature data and a melt factor to compute cumulative positive degree-days and snow/ice melt over a season.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Glaciology / Cryosphere
 
Functional spec:

(a) Inputs:
- A text area where the user pastes or types a time series of daily mean air temperatures (in °C), one value per line or comma-separated.
- A numeric input for the melt factor (mm/°C/day), default 5.0, with typical range 2–10, shown alongside brief guidance (snow: 3–5, ice: 6–8).
- A numeric input for the threshold temperature (in °C), default 0.0.
- A "Calculate" button.

(b) Core logic (step by step):
1. Parse the temperature list; if empty or malformed, show an error.
2. For each daily temperature T_i, compute the positive degree-day value: PDD_i = max(T_i - threshold, 0).
3. Sum all PDD_i to get total positive degree-days (PDD_total, in °C·days).
4. For each day, compute daily melt: M_i = melt_factor × PDD_i (in mm water equivalent).
5. Sum M_i to get cumulative seasonal melt (in mm w.e.).
6. Optionally compute a simple classification: if cumulative melt < 100 mm → "Low melt season"; 100–500 mm → "Moderate melt season"; >500 mm → "High melt season".
7. Generate a matplotlib figure: a line plot of cumulative melt over time (days on x-axis, cumulative melt in mm on y-axis) and a secondary plot (subplot or twin axis) of daily melt as bars.

(c) Gradio UI layout:
- Title: "Degree-Day Melt Model"
- Row 1: text box for temperature series (label "Daily mean temperatures (°C)", height enough for ~30 lines).
- Row 2: two numeric inputs side-by-side: "Melt factor (mm/°C/day)" and "Threshold temperature (°C)".
- Row 3: a "Calculate" button.
- Output area: below the button, display:
   - Three numerical readouts: Total Positive Degree-Days, Cumulative Melt (mm w.e.), Melt Season Classification.
   - A matplotlib plot showing daily melt (bar) and cumulative melt (line), with clear axis labels and legend.
- (Optional) a brief note: "Data source: typical melt factors — snow 3–5, ice 6–8."

(d) Output:
- Numbers: total PDD (to one decimal), total cumulative melt (to integer mm), classification string.
- Plot: matplotlib figure rendered in Gradio.

(e) AI/ML component: None. All calculations are deterministic and rule-based.
 
## Run it
 
```bash
docker build -t degree-day-melt-model .
docker run -p 7860:7860 degree-day-melt-model
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-10-01.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
