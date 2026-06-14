# Module: psat.packages.plclassclass.base
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = base(a)

if not a.n, return, end

global Settings

if not isempty(a.init)
  k = a.init
  a.con(k,5) = a.con(k,5).*a.con(k,2)/Settings.mva
  a.con(k,6) = a.con(k,6).*a.con(k,2)/Settings.mva
  a.con(k,7) = a.con(k,7).*a.con(k,2)/Settings.mva
  a.con(k,8) = a.con(k,8).*a.con(k,2)/Settings.mva
  a.con(k,9) = a.con(k,9).*a.con(k,2)/Settings.mva
  a.con(k,10) = a.con(k,10).*a.con(k,2)/Settings.mva