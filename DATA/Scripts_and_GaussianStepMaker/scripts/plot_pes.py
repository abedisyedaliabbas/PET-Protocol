import matplotlib.pyplot as plt
import numpy as np

# ================= USER INPUT SECTION =================
# Replace the values below with your specific calculation results.
# 1. GROUND STATE (S0)
E_S0_min        = 0.00
E_S0_at_LE_geom = 0.24   # Energy of S0 at the LE optimized geometry (Fluorescence landing)
E_S0_at_CT_geom = 1.01   # Energy of S0 at the CT optimized geometry (Zig-Zag landing)

# 2. LOCALLY EXCITED STATE (LE - ORANGE)
E_VES_LE        = 2.61   # Vertical Excitation Energy
f_VES_LE        = 0.59   # Oscillator Strength
E_AES_LE        = 2.42   # Adiabatic (Relaxed) LE Energy
f_AES_LE        = 0.71   # Oscillator Strength

# 3. CHARGE TRANSFER STATE (CT - GREEN)
E_AES_CT        = 1.63   # Relaxed CT Energy
f_AES_CT        = 0.00   # Oscillator Strength
# Set E_VES_CT to a number if you found the Vertical CT state. 
# Set to None to let the script automatically estimate the curve shape.
E_VES_CT        = None   

# 4. VISUAL TUNING
WIDTH_FACTOR    = 1.5    # Adjusts curve width (Higher = Flatter)
X_POS_CT        = 1.7    # X-axis position for the CT state (Standard ~1.5 to 2.0)

MOLECULE_NAME   = "Neutral Rhodamine"
# ======================================================

def draw_fitted_curve(ax, x_points, y_points, color, label, x_range_left, x_range_right):
    """Fits a polynomial (degree 2) to 3 points to ensure the curve hits all of them."""
    coeffs = np.polyfit(x_points, y_points, 2)
    poly = np.poly1d(coeffs)
    x_vertex = x_points[0]
    x = np.linspace(x_vertex - x_range_left, x_points[-1] + x_range_right, 200)
    y = poly(x)
    ax.plot(x, y, color=color, linewidth=2.5, label=label)
    return poly

def draw_parabola(ax, x_vertex, y_vertex, x_pass, y_pass, color, label, x_range_left, x_range_right):
    """Draws a parabola. If x_pass/y_pass are given, curve hits that point."""
    if x_pass is not None and y_pass is not None:
        denom = (x_pass - x_vertex)**2
        if denom < 1e-6: denom = 1.0
        a = (y_pass - y_vertex) / denom
    else:
        a = 1.0 / WIDTH_FACTOR 
    
    x = np.linspace(x_vertex - x_range_left, x_vertex + x_range_right, 200)
    y = a * (x - x_vertex)**2 + y_vertex
    ax.plot(x, y, color=color, linewidth=2.5, label=label)

def draw_zigzag(ax, start_xy, end_xy, num_zags=8, amplitude=0.04, color='black'):
    """Draws a sharp Zig-Zag line for non-radiative decay."""
    x0, y0 = start_xy
    x1, y1 = end_xy
    dx, dy = x1 - x0, y1 - y0
    length = np.sqrt(dx**2 + dy**2)
    ux, uy = dx/length, dy/length 
    px, py = -uy, ux              
    step = length / num_zags
    points = [(x0, y0)]
    for i in range(num_zags):
        dist = (i + 0.5) * step
        bx = x0 + ux * dist
        by = y0 + uy * dist
        direction = 1 if i % 2 == 0 else -1
        zx = bx + px * amplitude * direction
        zy = by + py * amplitude * direction
        points.append((zx, zy))
    points.append((x1, y1))
    xs, ys = zip(*points)
    ax.plot(xs, ys, color=color, lw=1.5)
    ax.annotate("", xy=end_xy, xytext=points[-2],
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

def main():
    fig, ax = plt.subplots(figsize=(8.5, 6.5))

    X_GS = 0.0
    X_LE = 1.0
    X_CT = X_POS_CT

    # --- 1. DRAW CURVES ---
    # S0 (Gray) - Fits 3 points
    s0_x = [X_GS, X_LE, X_CT]
    s0_y = [E_S0_min, E_S0_at_LE_geom, E_S0_at_CT_geom]
    draw_fitted_curve(ax, s0_x, s0_y, 'silver', 'S0', 0.8, 0.4)

    # LE (Orange)
    draw_parabola(ax, X_LE, E_AES_LE, X_GS, E_VES_LE, '#FF8C00', 'LE', 1.2, 1.2)

    # CT (Green)
    draw_parabola(ax, X_CT, E_AES_CT, X_GS, E_VES_CT, '#32CD32', 'CT', 1.5, 0.8)

    # --- 2. ADD POINTS & LABELS ---
    def add_point(x, y, color, label=None, sublabel=None, top=True):
        ax.scatter(x, y, s=120, color=color, edgecolors='black', zorder=10)
        offset = 0.25 if top else -0.45
        va = 'bottom' if top else 'top'
        if label: txt = f"{label}\n{y:.2f}"
        else: txt = f"{y:.2f}"
        if sublabel: txt += f"\n{sublabel}"
        ax.text(x, y + offset, txt, ha='center', va=va, fontsize=10, fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

    # Points
    add_point(X_GS, E_S0_min, 'royalblue', top=False)
    add_point(X_GS, E_VES_LE, '#FF8C00', "VES (LE)", f"f={f_VES_LE}")
    add_point(X_LE, E_AES_LE, '#FF8C00', "AES (LE)", f"f={f_AES_LE}")
    
    # S0 Landings
    ax.scatter(X_LE, E_S0_at_LE_geom, s=120, color='royalblue', edgecolors='black', zorder=10)
    ax.text(X_LE, E_S0_at_LE_geom - 0.35, f"{E_S0_at_LE_geom:.2f}", ha='center', va='top', fontsize=10, fontweight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.5))
    
    add_point(X_CT, E_AES_CT, '#32CD32', "AES (ET)", f"f={f_AES_CT}")
    
    if E_VES_CT is not None:
        add_point(X_GS, E_VES_CT, '#32CD32', "VES (ET)", top=True)

    ax.scatter(X_CT, E_S0_at_CT_geom, s=120, color='royalblue', edgecolors='black', zorder=10)
    ax.text(X_CT, E_S0_at_CT_geom - 0.35, f"{E_S0_at_CT_geom:.2f}", ha='center', va='top', fontsize=10, fontweight='bold',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.5))

    # --- 3. ARROWS ---
    ax.annotate("", xy=(X_GS, E_VES_LE), xytext=(X_GS, E_S0_min), arrowprops=dict(arrowstyle="->", color='black', lw=2))
    ax.annotate("", xy=(X_LE, E_S0_at_LE_geom), xytext=(X_LE, E_AES_LE), arrowprops=dict(arrowstyle="->", color='black', lw=2))
    ax.annotate("", xy=(X_LE, E_AES_LE), xytext=(X_GS, E_VES_LE), arrowprops=dict(arrowstyle="->", color='black', lw=1.5, ls="--"))
    ax.annotate("", xy=(X_CT, E_AES_CT), xytext=(X_LE, E_AES_LE),
                arrowprops=dict(arrowstyle="->", color='black', lw=1.5, connectionstyle="arc3,rad=-0.3"))
    draw_zigzag(ax, (X_CT, E_AES_CT), (X_CT, E_S0_at_CT_geom))

    # --- 4. FORMATTING ---
    ax.set_ylabel("Energy Level / eV", fontsize=12)
    ax.set_xlabel("Photodeactivation pathway", fontsize=12)
    ax.set_title(MOLECULE_NAME, fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    y_max = max(E_VES_LE, E_AES_LE) + 1.2
    if E_VES_CT: y_max = max(y_max, E_VES_CT + 1.0)
    ax.set_ylim(-1.0, y_max)

    plt.tight_layout()
    
    # --- SAVE IN MULTIPLE FORMATS ---
    # Customize filename based on molecule name
    fname = "PES_" + MOLECULE_NAME.replace(" ", "_")
    plt.savefig(f"{fname}.png", dpi=300)
    plt.savefig(f"{fname}.svg", format='svg')
    plt.savefig(f"{fname}.jpg", dpi=300, format='jpg')
    
    print(f"Graphs saved as {fname}.png, .svg, and .jpg")
    plt.show()

if __name__ == "__main__":
    main()
