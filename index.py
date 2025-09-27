import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

# Driver assumption data
data = {
    "Driver": ["ESG Mandates", "ESG Mandates", "PLI Modernization", "PLI Modernization",
               "Tariffs", "Tariffs", "OT/IT Convergence", "OT/IT Convergence"],
    "CAGR (%)": [18, 24, 19, 23, 21, 23, 20, 22],
    "2030 TAM (₹B)": [68, 98, 72, 94, 83, 94, 77, 88]
}

df = pd.DataFrame(data)

# Map drivers to numeric for surface plotting
driver_map = {d: i for i, d in enumerate(df["Driver"].unique())}
df["Driver_num"] = df["Driver"].map(driver_map)

# Create grid
x = np.linspace(df["CAGR (%)"].min(), df["CAGR (%)"].max(), 50)
y = np.linspace(df["Driver_num"].min(), df["Driver_num"].max(), 50)
X, Y = np.meshgrid(x, y)

# Interpolate TAM values
Z = griddata(
    (df["CAGR (%)"], df["Driver_num"]), 
    df["2030 TAM (₹B)"], 
    (X, Y), 
    method='cubic'
)

# 3D surface
fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis")])

# Update layout
fig.update_layout(
    title="PMEA TAM Sensitivity Surface (Drivers vs CAGR vs TAM)",
    scene=dict(
        xaxis_title="CAGR (%)",
        yaxis=dict(
            title="Driver",
            tickvals=list(driver_map.values()), 
            ticktext=list(driver_map.keys())
        ),
        zaxis_title="2030 TAM (₹B)"
    )
)

fig.show()

# Save interactive chart as HTML
fig.write_html("index.html", include_plotlyjs="cdn")
