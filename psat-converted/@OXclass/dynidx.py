# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@OXclass\dynidx.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = dynidx(a)

global DAE Syn Exc

if not a.n, return, end

a.v = DAE.n+[1:a.n]';
a.If = DAE.m+[1:a.n]';
DAE.n = DAE.n + a.n
DAE.m = DAE.m + a.n

a.p = Syn.p(a.syn)
a.q = Syn.q(a.syn)
a.vref = Exc.vref(a.exc)
