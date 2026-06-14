# Module: psat.packages.spvclassclass.setx0
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global Bus DAE Settings 

if not a.n, return, end

check = 1

bt_Pref = a.con(:,2)./Settings.mva
# bt_Qref = a.con(:,3)./Settings.mva;

V = DAE.y(a.vbus)
t = DAE.y(a.bus)
st = sin(t)
ct = cos(t)

Vd = -V.*st
Vq =  V.*ct


# % Vref
a.dat(:,1) = V

# % Initialization of state variables

for i in range(1, a.n+1):
 
# find & delete static generators
  if not fm_rmgen(a.u(i)*a.bus(i)), check = 0; end

# state variables initialization

# id = bt_Pref;
# iq = zeros(a.n,1);
# DAE.x(a.btx1) = zeros(a.n,1);
# DAE.x(a.id) = a.u.*id;
# DAE.x(a.iq) = a.u.*iq;

idiq = [Vd Vq; Vq -Vd]\[Bus.Pg(a.bus);Bus.Qg(a.bus)]
id = idiq(1)
iq = idiq(2)

DAE.x(a.btx1) = a.u.*Bus.Qg(a.bus)
DAE.x(a.id) = a.u.*id
DAE.x(a.iq) = a.u.*iq
DAE.y(a.vref) = a.u.*a.dat(:,1)

if not check
  fm_print('Solar photo-voltaic generators (PV model) cannot be properly initialized.')
else
  fm_print('Initialization of Solar Photo-Voltaic Generators (PV model) completed.')
