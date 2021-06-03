import pandapower
import pandapower.networks
import pandapower.topology
import pandapower.plotting
import pandapower.converter
import pandapower.estimation
import pandapower.test
import pandapower.networks as pn
#pandapower.test.run_all_tests()
#Cases are at https://pandapower.readthedocs.io/en/v2.6.0/networks/power_system_test_cases.html?highlight=118#case-118
#Network loaded from pandapower built-in networks
net = pn.case118()
#Printing test
print(net)
print(net.line)
print(net.trafo)
print(net.bus)
print(net.load)
print(net.gen)
#Plotting test
pandapower.plotting.simple_plot(net, respect_switches=False, line_width=1.0, bus_size=1.0, ext_grid_size=1.0, trafo_size=1.0, plot_loads=False, plot_sgens=False, load_size=1.0, sgen_size=1.0, switch_size=2.0, switch_distance=1.0, plot_line_switches=False, scale_size=True, bus_color='b', line_color='grey', trafo_color='k', ext_grid_color='y', switch_color='k', library='igraph', show_plot=True, ax=None)
