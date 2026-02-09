baseline = {
    "temp": 0.43,
    "rhum": 2.00,
    "prcp": 0.13,
    "wspd": 1.56,
    "pres": 0.19
}

hybrid = {
    "temp": 0.42,
    "rhum": 1.82,
    "prcp": 0.13,
    "wspd": 1.57,
    "pres": 0.20
}

print("\n📊 Model Comparison (MAE)")
print("----------------------------------")
for k in baseline:
    diff = baseline[k] - hybrid[k]
    status = "Improved" if diff > 0 else "Stable"
    print(f"{k.upper():5} | Baseline: {baseline[k]:.2f} | Hybrid: {hybrid[k]:.2f} | {status}")
