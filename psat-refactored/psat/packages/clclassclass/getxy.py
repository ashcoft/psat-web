# Module: psat.packages.clclassclass.getxy
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function [x,y] = getxy(a,bus,x,y)

global Exc Svc

if not a.n, return, end

buses = np.zeros((a.n,1))
buses(a.exc) = Exc.bus(a.con(a.exc,2))
buses(a.svc) = Svc.bus(a.con(a.svc,2))

h = find(ismember(buses,bus))

if not isempty(h)
  x = [x; a.Vs(h)]