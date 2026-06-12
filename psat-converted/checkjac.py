# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/checkjac.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

numjacs
fm_call('i')

print(' ')

gerr = max(abs(DAE.g))
ferr = max(abs(DAE.f))

print(['g max err = ',num2str(gerr)])
print(['f max err = ',num2str(ferr)])

if ferr > Settings.dyntol
  print('The following elements of the f vector are suspiciously high:')
  print(' ')
  v = abs(DAE.f)
  i = find(v > Settings.dyntol)
for h in range(1, len(i)+1):
    u = v(i(h))
    print(['* ', Varname.uvars{i(h)}, ' -> ', num2str(u)])
  print(' ')

if gerr > Settings.dyntol
  print('The following elements of the g vector are suspiciously high:')
  print(' ')
  v = abs(DAE.g)
  i = find(v > Settings.dyntol)
for h in range(1, len(i)+1):
    u = v(i(h))
    print(['* ', Varname.uvars{i(h) + DAE.n}, ' -> ', num2str(u)])
  print(' ')

print(' ')

print(['Fx abs err = ',num2str(max(max(abs(DAE.Fx-Fx))))])
print(['Fy abs err = ',num2str(max(max(abs(DAE.Fy-Fy))))])
print(['Gx abs err = ',num2str(max(max(abs(DAE.Gx-Gx))))])
print(['Gy abs err = ',num2str(max(max(abs(DAE.Gy-Gy))))])

print(' ')

if DAE.n 
  [i,j] = find(abs(DAE.Fx) <= Settings.dyntol)
  Fxtmp = DAE.Fx + sparse(i,j,1,DAE.n,DAE.n)
  
  [i,j] = find(abs(DAE.Fy) <= Settings.dyntol)
  Fytmp = DAE.Fy + sparse(i,j,1,DAE.n,DAE.m)
  
  [i,j] = find(abs(DAE.Gx) <= Settings.dyntol)
  Gxtmp = DAE.Gx + sparse(i,j,1,DAE.m,DAE.n)
else
  Fxtmp = 1
  Fytmp = np.ones((1,DAE.m))
  Gxtmp = np.ones((DAE.m,1))

[i,j] = find(abs(DAE.Gy) <= Settings.dyntol)
Gytmp = DAE.Gy + sparse(i,j,1,DAE.m,DAE.m)

Fxerr = max(max(abs((DAE.Fx-Fx)./Fxtmp)))
Fyerr = max(max(abs((DAE.Fy-Fy)./Fytmp)))
Gxerr = max(max(abs((DAE.Gx-Gx)./Gxtmp)))
Gyerr = max(max(abs((DAE.Gy-Gy)./Gytmp)))

print(['Fx rel err = ',num2str(Fxerr)])
print(['Fy rel err = ',num2str(Fyerr)])
print(['Gx rel err = ',num2str(Gxerr)])
print(['Gy rel err = ',num2str(Gyerr)])

print(' ')

if Fxerr > Settings.dyntol
  print('The following elements of the Fx matrix are suspiciously high:')
  print(' ')
  v = abs((DAE.Fx-Fx)./Fxtmp)
  [i, j] = find(v > Settings.dyntol)
for h in range(1, len(i)+1):
    u = v(i(h), j(h))
    print(['* ', Varname.uvars{i(h)}, ' - ', Varname.uvars{j(h)}, ' -> ', num2str(u)])
  print(' ')

if Fyerr > Settings.dyntol
  print('The following elements of the Fy matrix are suspiciously high:')
  print(' ')
  v = abs((DAE.Fy-Fy)./Fytmp)
  [i, j] = find(v > Settings.dyntol)
for h in range(1, len(i)+1):
    u = v(i(h), j(h))
    print(['* ', Varname.uvars{i(h)}, ' - ', Varname.uvars{j(h)+DAE.n}, ' -> ', num2str(u)])
  print(' ')

if Gxerr > Settings.dyntol
  print('The following elements of the Gx matrix are suspiciously high:')
  print(' ')
  v = abs((DAE.Gx-Gx)./Gxtmp)
  [i, j] = find(v > Settings.dyntol)
for h in range(1, len(i)+1):
    u = v(i(h), j(h))
    print(['* ', Varname.uvars{i(h)+DAE.n}, ' - ', Varname.uvars{j(h)}, ' -> ', num2str(u)])
  print(' ')

if Gyerr > Settings.dyntol
  print('The following elements of the Gy matrix are suspiciously high:')
  print(' ')
  v = abs((DAE.Gy-Gy)./Gytmp)
  [i, j] = find(v > Settings.dyntol)
for h in range(1, len(i)+1):
    u = v(i(h), j(h))
    print(['* ', Varname.uvars{i(h)+DAE.n}, ' - ', Varname.uvars{j(h)+DAE.n}, ' -> ', num2str(u)])
  print(' ')
