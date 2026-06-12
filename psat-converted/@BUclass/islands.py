# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@BUclass\islands.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = islands(a,traceY)

if not a.n, return, end

# defining critical islanded buses
a.island = find(traceY < 1e-4)
if not isempty(a.island)
  n = len(a.island)
  if n > 10
    fm_print(['* * ',num2str(n),' buses are islanded!'])
    fm_print(['* * Type ''Bus.island'' to get islanded bus numbers.'])
  else
    fm_print(fm_strjoin(' * * Bus #', num2str(a.island),' is islanded.'))
