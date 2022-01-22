function [TorF, vstr, rdate] = have_feature_pdipmopf()
%HAVE_FEATURE_PDIPMOPF  Detect availability/version info for PDIPMOPF
%
%   Feature detection function implementing 'pdipmopf' tag for HAVE_FEATURE
%   to detect availability/version of PDIPMOPF, a primal-dual interior point
%   method optimal power flow (OPF) solver included in TSPOPF.
%   (https://www.pserc.cornell.edu/tspopf)
%
%   See also HAVE_FEATURE, PDIPMOPF.

%   MATPOWER
%   Copyright (c) 2004-2020, Power Systems Engineering Research Center (PSERC)
%   by Ray Zimmerman, PSERC Cornell
%
%   This file is part of MATPOWER.
%   Covered by the 3-clause BSD License (see LICENSE file for details).
%   See https://matpower.org for more info.

if have_feature('matlab') && exist('pdipmopf', 'file') == 3;
    TorF = 1;
    v = pdipmopfver('all');
    vstr = v.Version;
    rdate = v.Date;
else
    TorF = 0;
    vstr = '';
    rdate = '';
end
