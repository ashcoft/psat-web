# Module: psat.packages.dmclassclass.gams
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
function [n,idx,data] = gams(a)

global Bus GAMS

n = int2str(a.n)
idx = sparse(a.bus,[1:a.n],1,Bus.n,a.n)

data = []

if not a.n, return, end

tgphi = tanphi(a)
[Cda,Cdb,Cdc,Dda,Ddb,Ddc] = costs(a)

if GAMS.method == 7
  if len(a.con(1,:)) < 16
    Rdup = a.u.*a.con(:,9)
    Rddw = a.u.*a.con(:,9)
  else
    Rdup = a.u.*a.con(:,16)
    Rddw = a.u.*a.con(:,17)

if GAMS.loaddir
  Pd0 = a.u.*a.con(:,3)
else
  Pd0 = a.u.*a.con(:,7)

[Pdmax,Pdmin] = plim(a)

if GAMS.method < 7
  data.val = [Pd0,Pdmax,Pdmin,tgphi,Cda,Cdb,Cdc,Dda,Ddb,Ddc]
else
  data.val = [Pd0,Pdmax,Pdmin,tgphi,Cda,Cdb,Cdc,Dda,Ddb,Ddc,Rdup,Rddw]

if GAMS.method < 7
  data.labels = {cellstr(num2str([1:a.n]')), ...
              {'Pd0','Pdmax','Pdmin','tgphi','Cda', ...
               'Cdb','Cdc','Dda','Ddb','Ddc'}}
else
  data.labels = {cellstr(num2str([1:a.n]')), ...
              {'Pd0','Pdmax','Pdmin','tgphi','Cda', ...
               'Cdb','Cdc','Dda','Ddb','Ddc','RDup','RDdw'}}

data.name = 'D'