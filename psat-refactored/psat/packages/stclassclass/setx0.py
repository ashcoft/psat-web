# Module: psat.packages.stclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global Syn Bus DAE PV

if not a.n, return, end

V = DAE.y(a.vbus)
Kr = a.con(:,5)
Tr = a.con(:,6)
ist_max = a.u.*a.con(:,7)
ist_min = a.u.*a.con(:,8)

# eliminate PV components used for initializing STATCOM's
for i in range(1, a.n+1):
  idxg = findbus(Syn,a.bus(i))
  if not isempty(idxg)
    warn(a,i,[' STATCOM cannot be connected at the same bus as ' ...
                     'synchronous machines.'])
    continue
  if a.u(i)
    idx = findbus(PV,a.bus(i))
    PV = remove(PV,idx)
    if isempty(idx)
      warn(a,i,' no PV generator found at the bus.')
DAE.x(a.ist) = a.u.*Bus.Qg(a.bus)./V
idx = find(DAE.x(a.ist) > ist_max)
if idx, warn(a,idx,' Ish is over its max limit.'), end
idx = find(DAE.x(a.ist) < ist_min)
if idx, warn(a,idx,' Ish is under its min limit.'), end
DAE.x(a.ist) = max(DAE.x(a.ist),ist_min)
DAE.x(a.ist) = min(DAE.x(a.ist),ist_max)

# reference voltages
a.Vref = DAE.x(a.ist)./Kr + V
DAE.y(a.vref) = a.Vref

fm_print('Initialization of STATCOMs completed.')