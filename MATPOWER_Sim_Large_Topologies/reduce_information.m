%%reduces case information
function mpc=reduce_information(mpc1)
case_to_base_off_of = loadcase('caseBase');
branch_len = length(case_to_base_off_of.branch);
bus_len = length(case_to_base_off_of.bus);
gen_len = length(case_to_base_off_of.gen);
gencost_len = length(case_to_base_off_of.gencost);
mpc = mpc1;
%crop
if branch_len < length(mpc.branch(1,:))
    mpc.branch=mpc.branch(:, 1:branch_len);
end
if bus_len < length(mpc.bus(1,:))
    mpc.bus=mpc.bus(:, 1:bus_len);
end
if gen_len < length(mpc.gen(1,:))
    mpc.gen=mpc.gen(:, 1:gen_len);
end
if gencost_len < length(mpc.gencost(1,:))
    mpc.gencost=mpc.gencost(:, 1:gencost_len);
end
end