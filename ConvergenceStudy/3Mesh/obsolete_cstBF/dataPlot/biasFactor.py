import numpy as np
from scipy.optimize import fsolve


def mesh_equations(r, L, y1, N):
    if abs(r - 1.0) < 1e-10:
        return y1 * N - L
    return y1 * (r**N - 1) / (r - 1) - L


L = 0.1
# Baseline from your successful run
N_medium = 10
BF_medium = 5
r_medium = BF_medium**(1/(N_medium-1))
y1_target = L * (r_medium - 1) / (r_medium**N_medium - 1)

print(f"Target y1: {y1_target:.6f}")

for N in [7, 10, 15, 22, 30]:
    # Check if a uniform mesh is already too coarse
    y1_uniform = L / N
    if y1_uniform < y1_target:
        # We need r > 1 to stretch it
        r_sol = fsolve(mesh_equations, 1.1, args=(L, y1_target, N))[0]
        bf_sol = r_sol**(N-1)
    else:
        # Even a uniform mesh has a first cell bigger than target y1
        r_sol = fsolve(mesh_equations, 0.9, args=(L, y1_target, N))[0]
        bf_sol = (r_sol**(N-1))  # Inverting for Ansys 'Bias' logic

    print(f"N={N:2d} | BF Required: {bf_sol:.4f} | r: {r_sol:.4f} | {'DECREASING growth' if r_sol < 1 else 'INCREASING growth'}")
