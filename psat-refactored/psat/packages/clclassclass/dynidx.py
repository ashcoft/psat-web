# Module: psat.packages.clclassclass.dynidx
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

function a = dynidx(a)

global DAE Exc Svc Cac Syn

if not a.n, return, end

a.Vs = DAE.n + [1:a.n]';
DAE.n = DAE.n + a.n

a.vref = np.zeros((a.n,1))
a.vref(a.exc) = Exc.vref(a.con(a.exc,2))
a.vref(a.svc) = Svc.vref(a.con(a.svc,2))

a.cac = Cac.q(a.con(:,1))

a.q = np.zeros((a.n,1))
a.q(a.exc) = Syn.q(a.syn)
a.q(a.svc) = Svc.q(a.con(a.svc,2))
