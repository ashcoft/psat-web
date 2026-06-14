# Module: psat.packages.swclassclass.odm
# Refactored from psat-converted
# ------------------------------------------------------------------
# WARNING: This is a mechanical, BEST-EFFORT textual conversion.
# It is NOT a runnable Python port. Manual review is REQUIRED.
# ------------------------------------------------------------------
import numpy as np

def odm(a, fid, tag, bus, space):

if not a.n, return, end

idx = findbus(a,bus)

if isempty(idx), return, end

count = fprintf(fid,'%s<%s:voltage>\n',space,tag)
count = fprintf(fid,'  %s<%s:voltage>%8.5f</%s:voltage>\n',space,tag,a.con(idx,4),tag)
count = fprintf(fid,'  %s<%s:unit>PU</%s:unit>\n',space,tag,tag)
count = fprintf(fid,'%s</%s:voltage>\n',space,tag)
count = fprintf(fid,'%s<%s:angle>\n',space,tag)
count = fprintf(fid,'  %s<%s:angle>%8.5f</%s:angle>\n',space,tag,180*a.con(idx,5)/np.pi,tag)
count = fprintf(fid,'  %s<%s:unit>DEG</%s:unit>\n',space,tag,tag)
count = fprintf(fid,'%s</%s:angle>\n',space,tag)
count = fprintf(fid,'%s<%s:genData>\n',space,tag)
if a.con(:,12)
  count = fprintf(fid,'  %s<%s:code>SWING</%s:code>\n',space,tag,tag)
else
  count = fprintf(fid,'  %s<%s:code>VTHETA</%s:code>\n',space,tag,tag)
count = fprintf(fid,'%s</%s:genData>\n',space,tag)