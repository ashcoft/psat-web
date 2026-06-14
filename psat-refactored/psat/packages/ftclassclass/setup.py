# Module: psat.packages.ftclassclass.setup
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = setup(a)

global Bus

if isempty(a.con)
  a.store = []
  return

a.n = len(a.con(:,1))
[a.bus,a.vbus] = getbus(Bus,a.con(:,1))

# fault occurrence and clearing times
idx = find(a.con(:,5) == 0)
if not isempty(idx)
  a.con(idx,5) = 1e-6
  a.con(idx,6) = a.con(idx,6)+1e-6

# consistency of clearing times
idx = find((a.con(:,6) - a.con(:,5)) < 0)
if not isempty(idx)
  fm_print('Warning: The fault clearing time must be greater than the fault time',2)
  a.con(idx,6) = a.con(idx,6) + a.con(idx,5)
  fm_print(fm_strjoin('         Fault #',int2str(idx), ...
                 ' at bus #',Bus.names(a.bus(idx)), ...
                 ': clearing time changed to <', ...
                 num2str(a.con(idx,6)), '> s.'))

# fault status:
#
# 0 before and after fault
# 1 during fault

a.u = np.zeros((a.n,1))

# dat:
#
# 1.  fault conductance
# 2.  fault susceptance

z = a.con(:,7) + i*a.con(:,8)
z(find(abs(z) == 0)) = i*1e-6
y = conj(1./z)

a.dat= [real(y), imag(y)]

a.store = a.con