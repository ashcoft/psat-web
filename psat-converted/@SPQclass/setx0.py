# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@SPQclass\setx0.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function a = setx0(a)

global Bus DAE 

if not a.n, return, end

check = 1

# bt_Pref = a.con(:,2)./Settings.mva;
# bt_Qref = a.con(:,3)./Settings.mva;

# Pc = Bus.Pg(a.bus);
# Qc = Bus.Qg(a.bus);
Vc = DAE.y(a.vbus)
ac = DAE.y(a.bus)

Vd = -Vc.*sin(ac)
Vq =  Vc.*cos(ac)
# 
# % Initialization of state variables

for i in range(1, a.n+1):
  
# find & delete static generators
  if not fm_rmgen(a.u(i)*a.bus(i)), check = 0; end

# state variables initialization
# id = bt_Qref;
# iq = bt_Pref;
# DAE.x(a.id) = a.u.*id;
# DAE.x(a.iq) = a.u.*iq;
idiq = [Vd Vq; Vq -Vd]\[Bus.Pg(a.bus);Bus.Qg(a.bus)]
id = idiq(1)
iq = idiq(2)

DAE.x(a.id) = a.u.*id
DAE.x(a.iq) = a.u.*iq


if not check
  fm_print('Solar photo-voltaic generators (PQ model) cannot be properly initialized.')
else
  fm_print('Initialization of Solar Photo-Voltaic Generators (PQ model) completed.')

