# Module: psat.packages.pqclassclass.restore
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = restore(a,varargin)

global PQgen

if isempty(a.store)
  a = init(a)
  return

a.con = a.store
a = setup(a)

switch nargin
 case 2
  addpqgen = varargin{1}
 otherwise
  addpqgen = 1

if PQgen.n  and  addpqgen
  a = addgen(a,PQgen)