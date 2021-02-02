import os
import xraylib

class Parser:

    def __init__(__self__):
        __self__.temporary_files = []
        __self__.quadrics = []

    def write_inputs(__self__,compounds):
        # write input file

        f = open(os.path.join(os.getcwd(),'input.dat'), 'w+')
        __self__.temporary_files.append(os.path.join(os.getcwd(),"input.dat"))
        f.write('Load source.dat;\n')
        f.write('Load detector.dat;\n')
        f.write('Load tube.dat;\n')
        f.write('Load sample.dat;\n')
        f.write('Load quadrics.dat;\n')
        f.write('Load geometry.dat;\n')
        f.write('Load composition.dat;\n')
        f.write('Run DetectorArray;\n')
        f.write('Save DetectorArray Image output.dat;\n')
        f.close()

        #write composition file

        f = open(os.path.join(os.getcwd(),'composition.dat'), 'w+')
        __self__.temporary_files.append(os.path.join(os.getcwd(),"composition.dat"))
        f.write('Newdevice composition\n')
        f.write('Composition\n\n')
        for compound in compounds:
            f.write('Phase {}\n'.format(compound.name))
            f.write('NElem {}\n'.format(len(compound.weight)))
            for element, weight in compound.weight.items():
                f.write('{0}\t{1:.4f}\n'.format(xraylib.SymbolToAtomicNumber(element), 
                    weight * 100))

            f.write('Rho\t{0:.4f}\n\n'.format(compound.density))

        f.write(';\nEnd\n')
        f.close()

        #wrote quadrics file

        f = open(os.path.join(os.getcwd(),'quadrics.dat'), 'w+')
        __self__.temporary_files.append(os.path.join(os.getcwd(),"quadrics.dat"))
        f.write('Newdevice quadricarray\n')
        f.write('QuadricArray;\n;\n')
        aux = 0
        for plane in __self__.quadrics:
            x, y, z, i, j, k = plane
            aux += 1
            f.write('Plane P{}\n'.format(aux))
            f.write(f"{x:.7f}\t{y:.7f}\t{z:.7f}\t{i:.7f}\t{j:.7f}\t{k:.7f}\n\n")

        aux = 0
        f.write(';\nEnd\n')
        f.close()

        #write geometry file

        f = open(os.path.join(os.getcwd(),'geometry.dat'), 'w+')
        __self__.temporary_files.append(os.path.join(os.getcwd(),"geometry.dat"))
        f.write('Newdevice geom3d\n')
        f.write('Geom3D\n')
        f.write('QArrName QuadricArray\n')
        f.write('CompName Composition\n')
        p = 0
        for compound in compounds:
            aux += 1
            lp = len(__self__.quadrics)
            f.write('Object Par{}\n'.format(aux))
            f.write('{} Vacuum\n6\n'.format(compound.name))
            f.write(f"P{p + 1} P{p + 2} P{lp - 3} P{lp - 2} P{lp - 1} P{lp}\n")
            p += 2

        f.write(';\nEnd\n')
        return (
         os.path.join(os.getcwd(),'input.dat'), os.path.join(os.getcwd(),'output.dat'))

    def get_planes(__self__, planes):
        start, end = 0, 0
        from itertools import chain
        for plane in planes:
            i, j, k = 1, 0, 0
            end = start -plane/10000
            pl1, pl2 = (start, 0, 0, i, j, k), (end, 0, 0, -i, -j, -k)
            start = end - 0.000001
            __self__.quadrics.append(pl1)
            __self__.quadrics.append(pl2)
        for plane in Planes().infinite_planes:
            __self__.quadrics.append(plane)
        return __self__.quadrics

class Planes:
    def __init__(__self__):
        __self__.infinite_planes = (0,0,1,0,0,1),(0,0,-1,0,0,-1),(0,-1,0,0,-1,0),(0,1,0,0,1,0)

