# -*- coding: utf-8 -*-
"""
Created on Sat May 24 23:28:37 2025
@author: ALOK KUMAR
"""

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time

def run():
    df_cache = None  # Cache for loaded dataframe

    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("Excel/CSV files", "*.xlsx *.csv")])
        file_path.set(filename)

    def process_data():
        nonlocal df_cache
        output_text.delete("1.0", tk.END)  # Clear previous results

        file = file_path.get()
        sheet = sheet_name.get()

        if not file:
            messagebox.showwarning("No file", "Please select a file.")
            return

        try:
            status_label.config(text="Processing...", fg="blue")
            root.update()
            start_time = time.time()

            # Load file if cache is empty, else use cached dataframe
            if df_cache is None:
                if file.endswith(".csv"):
                    df_cache = pd.read_csv(file)
                else:
                    df_cache = pd.read_excel(file, sheet_name=sheet)

            df = df_cache

            # Get user inputs
            smc_col = int(smc_column.get())
            rh_col = int(rh_column.get())
            atemp_col = int(atemp_column.get())
            lwet_col = int(lwet_column.get())
            time_col = int(time_column.get())

            smc_threshold = float(smc_threshold_entry.get())
            lwet_threshold = float(lwet_threshold_entry.get())
            rh_threshold = float(rh_threshold_entry.get())
            atemp_min = float(atemp_min_entry.get())
            atemp_max = float(atemp_max_entry.get())

            # Extract relevant columns
            tstep = df.iloc[:, time_col]
            smc = df.iloc[:, smc_col]
            rh = df.iloc[:, rh_col]
            atemp = df.iloc[:, atemp_col]
            lwet = df.iloc[:, lwet_col]

            ialert = dalert = palert = "null"

            # Initial 4-hour irrigation alert
            for i in range(min(4, len(smc))):
                if smc[i] <= smc_threshold:
                    if ialert != str(tstep[i])[:10]:
                        output_text.insert(tk.END, f"{tstep[i]}  →  Irrigation Required ! ! !\n")
                        ialert = str(tstep[i])[:10]

            # Main analysis loop
            for i in range(4, len(smc)):
                day = str(tstep[i])[:10]

                # Irrigation Alert
                if smc[i] <= smc_threshold:
                    if palert != day:
                        output_text.insert(tk.END, f"{tstep[i]}  →  Irrigation Required ! ! !\n")
                        palert = day

                # Disease Infestation Alert
                check = 0
                for j in range(4):
                    if (lwet[i-j] < lwet_threshold or 
                        atemp[i-j] < atemp_min or 
                        atemp[i-j] > atemp_max or 
                        rh[i-j] < rh_threshold):
                        check = 1
                        break
                if check == 0 and dalert != day:
                    output_text.insert(tk.END, f"{tstep[i]}  →  Disease Infestation Alert ! ! !\n")
                    dalert = day

            elapsed = round(time.time() - start_time, 2)
            status_label.config(text=f"Processing completed in {elapsed} seconds.", fg="green")

        except Exception as e:
            status_label.config(text="Error occurred.", fg="red")
            messagebox.showerror("Error", str(e))

    def clear_output():
        nonlocal df_cache
        output_text.delete("1.0", tk.END)
        status_label.config(text="", fg="green")
        df_cache = None  # Clear cached dataframe to force reload on next process

    root = tk.Tk()
    root.title("Irrigation Scheduling & Disease Infestation Alert System")

    file_path = tk.StringVar()
    sheet_name = tk.StringVar(value="Sheet1")

    tk.Label(root, text="Excel/CSV File:").grid(row=0, column=0)
    tk.Entry(root, textvariable=file_path, width=50).grid(row=0, column=1)
    tk.Button(root, text="Browse", command=browse_file).grid(row=0, column=2)

    tk.Label(root, text="Sheet Name:").grid(row=1, column=0)
    tk.Entry(root, textvariable=sheet_name).grid(row=1, column=1)

    labels = ["Date/Time", "Soil Moisture", "Relative Humidity", "Ambient temp.", "Leaf wetness"]
    entries = []
    for i, label in enumerate(labels):
        tk.Label(root, text=f"{label} Column Index:").grid(row=2+i, column=0)
        var = tk.StringVar()
        tk.Entry(root, textvariable=var).grid(row=2+i, column=1)
        entries.append(var)

    time_column, smc_column, rh_column, atemp_column, lwet_column = entries

    tk.Label(root, text="Soil moisture Threshold (%):").grid(row=7, column=0)
    smc_threshold_entry = tk.Entry(root)
    smc_threshold_entry.grid(row=7, column=1)

    tk.Label(root, text="Leaf Wetness Threshold (%):").grid(row=8, column=0)
    lwet_threshold_entry = tk.Entry(root)
    lwet_threshold_entry.grid(row=8, column=1)

    tk.Label(root, text="Relative Humidity Threshold (%):").grid(row=9, column=0)
    rh_threshold_entry = tk.Entry(root)
    rh_threshold_entry.grid(row=9, column=1)

    tk.Label(root, text="Ambient temperature Min (°C):").grid(row=10, column=0)
    atemp_min_entry = tk.Entry(root)
    atemp_min_entry.grid(row=10, column=1)

    tk.Label(root, text="Ambient temp. Max (°C):").grid(row=11, column=0)
    atemp_max_entry = tk.Entry(root)
    atemp_max_entry.grid(row=11, column=1)

    tk.Button(root, text="Process", command=process_data).grid(row=12, column=1)
    tk.Button(root, text="Clear", command=clear_output).grid(row=12, column=2)

    status_label = tk.Label(root, text="", fg="green")
    status_label.grid(row=13, column=0, columnspan=3)

    output_text = scrolledtext.ScrolledText(root, width=80, height=20)
    output_text.grid(row=14, column=0, columnspan=3)

    root.mainloop()

if __name__ == "__main__":
    run()
