#TODO: convert loadcase.m to python
import pandapower.networks as pn
def loadcase(caseName="case118"):
    if (caseName == "case118"):
        net = pn.case118()
        return net
    else:
        print("loadcase: case does not exist, returning case 118 instead\r\n")
        net = pn.case118()
        return net