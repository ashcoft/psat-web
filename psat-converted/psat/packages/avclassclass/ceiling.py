# Module: psat.packages.avclassclass.ceiling
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function output = ceiling(p,vf,A,B,flag)

#Se = A.*(exp(B.*abs(vf))-1);
Se = A.*exp(B.*abs(vf))

switch flag
 
 case 1, output = Se.*vf
 case 2, output = Se + A.*B.*exp(B.*abs(vf)).*abs(vf)
