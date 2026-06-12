# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@FPVclass\init.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = init(a)

a.con = []
a.dat = []
a.n = 0
a.conv = []

a.Tc = []; #  indexes of the state variable Tc

a.Ig = []; #  indexes of alg. variable Ig (dc current)
a.I0 = []; #  indexes of alg. variable I0 (dc current)
a.IL = []; #  indexes of alg. variable IL (dc current)
a.Vg = []; #  indexes of alg. varibale Vg (dc voltage)
a.Eg = []; #  indexes of alg. varibale Eg (energy band gap)

a.u = []
a.store = []
