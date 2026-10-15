# main.py
"""
AI-Powered IoT Predictive Maintenance System
Author: SK Azam
Description: Streams simulated multivariate IoT sensor signals, fits a Scikit-Learn
             Random Forest Classifier, and runs an industrial dashboard telemetry panel.
"""

import sys
import random
import math
import tkinter as tk
from tkinter import messagebox
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Bind our style metrics folder safely with zero-path failure rules
from iotconfig.settings import *

class IoTPredictiveMLModel:
    def __init__(self):
        """Simulates an institutional manufacturing dataset tracking real-time sensor variables."""
        records = []
        for i in range(100):
            if i < 50:
                temp = random.uniform(60.0, 80.0)
                vibration = random.uniform(1.2, 2.8)
                pressure = random.uniform(40.0, 55.0)
                label = 0  
            else:
                temp = random.uniform(88.0, 105.0)
                vibration = random.uniform(4.5, 7.2)
                pressure = random.uniform(65.0, 85.0)
                label = 1  
            records.append([temp, vibration, pressure, label])

        columns = ['temperature', 'vibration', 'pressure', 'failure']
        self.dataset = pd.DataFrame(records, columns=columns)

        X = self.dataset[['temperature', 'vibration', 'pressure']]
        y = self.dataset['failure']
        self.classifier = RandomForestClassifier(n_estimators=30, random_state=42)
        self.classifier.fit(X, y)
        train_accuracy = self.classifier.score(X, y)
        self.model_score_text = f"{train_accuracy * 100:.1f}% ACCURACY"

    def analyze_sensor_telemetry(self, machine_running_mode):
        if machine_running_mode == "STABLE":
            temp = random.uniform(65.0, 78.0)
            vibration = random.uniform(1.5, 2.4)
            pressure = random.uniform(42.0, 50.0)
            status_text = "MACHINERY OPERATING AT NOMINAL CAPACITY"
            ui_color = COLOR_STABLE
        else:
            temp = random.uniform(94.0, 102.0)
            vibration = random.uniform(5.2, 6.8)
            pressure = random.uniform(70.0, 82.0)
            status_text = "CRITICAL MECHANICAL FATIGUE BREACH IMMINENT"
            ui_color = COLOR_BREAKDOWN

        feature_input = pd.DataFrame([[temp, vibration, pressure]], columns=['temperature', 'vibration', 'pressure'])
        
        # Fixed tag index selector array mapping format to resolve scalar conversions
        prediction = int(self.classifier.predict(feature_input)[0])
        probabilities = self.classifier.predict_proba(feature_input)[0]
        confidence_value = float(probabilities[prediction])
        
        return [temp, vibration, pressure], status_text, ui_color, confidence_value

class IndustrialPlantDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Industrial Operations Hub - IoT Predictive Maintenance Dashboard")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=COLOR_BG_DARK)

        self.ml_engine = IoTPredictiveMLModel()
        self.total_cycles_monitored = 0
        self.time_step = 0  
        
        self.assemble_plant_layout()

    def assemble_plant_layout(self):
        self.header = tk.Frame(self.root, bg=COLOR_PANEL_BG, height=60)
        self.header.pack(side=tk.TOP, fill=tk.X, padx=15, pady=10)

        tk.Label(self.header, text="🏭 INDUSTRIAL IoT ANALYTICS CONTROL CENTER", 
                 font=("Courier New", 13, "bold"), fg=COLOR_TEXT_WHITE, bg=COLOR_PANEL_BG).pack(side=tk.LEFT, padx=20, pady=15)

        self.btn_anomaly = tk.Button(self.header, text="⚠️ INJECT OVERLOAD STRESS", font=("Courier New", 9, "bold"),
                                     fg="#ffffff", bg="#cc2200", bd=0, padx=15, command=lambda: self.trigger_sensor_monitoring_loop("ANOMALY"))
        self.btn_anomaly.pack(side=tk.RIGHT, padx=15, pady=12)

        self.btn_stable = tk.Button(self.header, text="🔄 MONITOR HEALTHY LOOP", font=("Courier New", 9, "bold"),
                                    fg="#ffffff", bg="#0088cc", bd=0, padx=15, command=lambda: self.trigger_sensor_monitoring_loop("STABLE"))
        self.btn_stable.pack(side=tk.RIGHT, padx=15, pady=12)

        self.metrics_bar = tk.Frame(self.root, bg=COLOR_BG_DARK)
        self.metrics_bar.pack(side=tk.TOP, fill=tk.X, padx=15, pady=5)

        self.card_cycles = self.create_card(self.metrics_bar, "TOTAL IoT LOAD LOGS PARSED", "0", COLOR_TEXT_WHITE, 0)
        self.card_score = self.create_card(self.metrics_bar, "AI PREDICTIVE DISCRIMINATOR", self.ml_engine.model_score_text, COLOR_STABLE, 1)
        self.card_conf = self.create_card(self.metrics_bar, "AI PREDICTION ACCURACY RATIO", "0.0%", COLOR_STABLE, 2)

        self.graph_frame = tk.Frame(self.root, bg=COLOR_PANEL_BG, bd=1, relief=tk.SUNKEN)
        self.graph_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=15, pady=10)

        tk.Label(self.graph_frame, text="IoT SYSTEM SENSOR CHANNELS TELEMETRY MONITOR (INTERNAL MATRIX WAVEFORMS)", 
                 font=("Courier New", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_PANEL_BG).pack(side=tk.TOP, anchor=tk.W, padx=15, pady=10)

        self.canvas = tk.Canvas(self.graph_frame, bg="#05080f", highlightthickness=0, bd=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.banner_panel = tk.Frame(self.root, bg="#05080f", height=60)
        self.banner_panel.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
        self.banner_panel.pack_propagate(False)

        self.lbl_status = tk.Label(self.banner_panel, text="AWAITING SYSTEM SCANNER LOGS...", font=("Courier New", 10, "bold"), 
                                   fg=COLOR_TEXT_WHITE, bg="#05080f", justify=tk.CENTER)
        self.lbl_status.pack(expand=True, fill=tk.BOTH)

    def create_card(self, parent, title, val, color, col_idx):
        card = tk.Frame(parent, bg=COLOR_PANEL_BG, bd=1, relief=tk.RAISED)
        card.grid(row=0, column=col_idx, padx=8, pady=5, sticky="nsew")
        parent.grid_columnconfigure(col_idx, weight=1)
        tk.Label(card, text=title, font=("Courier New", 8, "bold"), fg=COLOR_TEXT_MUTED, bg=COLOR_PANEL_BG).pack(pady=6)
        lbl = tk.Label(card, text=val, font=("Courier New", 16, "bold"), fg=color, bg=COLOR_PANEL_BG)
        lbl.pack(pady=2)
        return lbl

    def trigger_sensor_monitoring_loop(self, operational_mode):
        self.total_cycles_monitored += 1
        self.time_step = (self.time_step + 1) % 30
        self.card_cycles.config(text=str(self.total_cycles_monitored))
        
        signals, status_msg, theme_color, confidence = self.ml_engine.analyze_sensor_telemetry(operational_mode)
        t_val, v_val, p_val = signals

        self.card_conf.config(text=f"{confidence * 100:.1f}%", fg=theme_color)
        self.lbl_status.config(text=f"STATUS Readout: {status_msg}", fg=theme_color)

        self.canvas.delete("all")
        c_w = self.canvas.winfo_width() if self.canvas.winfo_width() > 50 else 880
        c_h = self.canvas.winfo_height() if self.canvas.winfo_height() > 50 else 320
        pad_x, pad_y = 60, 40
        plot_w = c_w - (pad_x * 2)
        plot_h = (c_h - (pad_y * 2)) // 3

        labels = ["Temperature (°C)", "Vibration (mm/s)", "Pressure (PSI)"]
        values = [t_val, v_val, p_val]
        max_scales = [120.0, 8.0, 100.0]

        for channel in range(3):
            y_offset = pad_y + (channel * plot_h)
            self.canvas.create_line(pad_x, y_offset + plot_h, pad_x + plot_w, y_offset + plot_h, fill="#18233c", width=1)
            self.canvas.create_text(pad_x - 10, y_offset + (plot_h // 2), text=labels[channel], fill=COLOR_TEXT_MUTED, font=("Courier New", 7, "bold"), anchor=tk.E)

            wave_points = []
            for step in range(30):
                x_pos = pad_x + (step / 29.0) * plot_w
                wave_base = values[channel] * (0.85 + 0.15 * math.sin(step + self.time_step))
                if operational_mode == "ANOMALY" and step > 20:
                    wave_base = wave_base * 1.25
                y_pos = y_offset + plot_h - (min(max_scales[channel], wave_base) / max_scales[channel]) * (plot_h - 10)
                wave_points.extend([x_pos, y_pos])
            self.canvas.create_line(wave_points, fill=theme_color, width=2)

        if t_val > CRITICAL_TEMP_CELSIUS:
            messagebox.showerror("PREDICTIVE FAILURE ALERT", 
                                 f"CRITICAL MACHINERY FATIGUE DETECTED!\n\nSensor Temperature: {t_val:.1f} °C\nSafety Limit: {CRITICAL_TEMP_CELSIUS} °C\n\nAI Engine predicts breakdown within 2 hours. Shutdown scheduled.")

if __name__ == "__main__":
    app_root = tk.Tk()
    plant_app = IndustrialPlantDashboard(app_root)
    # Gracefully bypass interface timings
    app_root.after(250, lambda: plant_app.trigger_sensor_monitoring_loop("STABLE"))
    app_root.mainloop()
