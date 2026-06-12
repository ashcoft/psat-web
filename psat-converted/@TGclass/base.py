# ------------------------------------------------------------------
# AUTO-CONVERTED FROM MATLAB BY tools/matlab_to_python.py
# Source: third-party/psat/@TGclass\base.m  (upstream PSAT, GPL-2.0+)
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function p = base(p)
#converts revice parameters to system power and voltage bases
global Syn Settings

if not p.n, return, end
for i in range(1, p.n+1):
    if (p.con(i,2) == 1)  or  (p.con(i,2) == 2),
         p.con(i,4) = Settings.mva.*p.con(i,4)./getvar(Syn,p.syn(i),'mva')
         p.con(i,5) = p.con(i,5).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,6) = p.con(i,6).*getvar(Syn,p.syn(i),'mva')/Settings.mva
    if (p.con(i,2) == 3),
         p.con(i,5) = p.con(i,5).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,6) = p.con(i,6).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,7) = p.con(i,7).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,8) = p.con(i,8).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,11) = p.con(i,11).*Settings.mva./getvar(Syn,p.syn(i),'mva')
    if (p.con(i,2) == 4),
         p.con(i,5) = p.con(i,5).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,6) = p.con(i,6).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,7) = p.con(i,7).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,8) = p.con(i,8).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,11) = p.con(i,11).*Settings.mva./getvar(Syn,p.syn(i),'mva')
    if (p.con(i,2) == 5),
         p.con(i,5) = p.con(i,5).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,6) = p.con(i,6).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,7) = p.con(i,7).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,8) = p.con(i,8).*getvar(Syn,p.syn(i),'mva')/Settings.mva
         p.con(i,11) = p.con(i,11).*Settings.mva./getvar(Syn,p.syn(i),'mva')
    if (p.con(i,2) == 6),
         p.con(i,16) = p.con(i,16).*Settings.mva./getvar(Syn,p.syn(i),'mva')



    



