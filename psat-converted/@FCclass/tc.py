# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@FCclass\tc.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function T = tc(a,T,T0,Tn)

idx = find(T == 0)
if idx
  T(idx) = T0
  warn(a,idx, ['Time constant ', Tn, ...
               ' cannot be zero. ', ...
               Tn, ' = ', num2str(T0), ...
               ' s will be used.'])
