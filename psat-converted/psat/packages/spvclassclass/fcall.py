# Module: psat.packages.spvclassclass.fcall
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
def fcall(a):

global DAE  Settings

if not a.n, return, end

btx1 = DAE.x(a.btx1)
id = DAE.x(a.id)
iq = DAE.x(a.iq)

V = DAE.y(a.vbus)
t = DAE.y(a.bus)
st = sin(t)
ct = cos(t)

bt_Pref = a.con(:,2)./Settings.mva
# bt_vref = a.con(:,3);

Tp = a.con(:,4)
Tq = a.con(:,5)

bt_kv = a.con(:,6)
bt_ki = a.con(:,7)




bt_Qref = btx1 + ( bt_kv .* (DAE.y(a.vref) - V) )

DAE.f(a.btx1) = a.u.* ( bt_ki .* (DAE.y(a.vref) - V) )

DAE.f(a.id) = a.u.*((bt_Qref.*ct - bt_Pref.*st)./V - id)./Tp

DAE.f(a.iq) = a.u.*((bt_Pref.*ct + bt_Qref.*st)./V - iq)./Tq

