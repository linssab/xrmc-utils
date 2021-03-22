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
        f.write('Load __sample__.dat;\n')
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

        #write quadrics file

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

def load_input(file_name):
    path = os.path.dirname(file_name)
    output_file = None
    f = open(file_name, "r")
    lines = f.readlines()
    line_no = 1
    for line in lines:
        if line.replace("\n","") == "": continue
        else: pass
        if "Load" in line:
            if line_no == 1:
                source_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            elif line_no == 2:
                 screen_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            elif line_no == 3:
                 spectrum_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            elif line_no == 4:
                 sample_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            elif line_no == 5:
                 quadrics_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            elif line_no == 6:
                 geom_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            elif line_no == 7:
                 composition_file = line.replace(";","").replace("\n","").split("Load")[-1].split(".dat")[0].replace(" ","") + ".dat"
            line_no += 1

        elif "Save" in line:
            output_file = line.replace(";","").replace("\n","").split("Image ")[-1].split(".dat")[0].replace(" ","") + ".dat"
    f.close()
    
    continuous_spectrum_file = get_tube_dat(os.path.join(path,spectrum_file))
    
    files = []
    files.append((os.path.join(path,source_file),source_file))
    files.append((os.path.join(path,screen_file),screen_file))
    files.append((os.path.join(path,continuous_spectrum_file),continuous_spectrum_file))
    files.append((os.path.join(path,spectrum_file),spectrum_file))
    files.append((os.path.join(path,sample_file),sample_file))
    files.append((os.path.join(path,quadrics_file),quadrics_file))
    files.append((os.path.join(path,geom_file),geom_file))
    files.append((os.path.join(path,composition_file),composition_file))
    return files, output_file

def get_tube_dat(file_): 
    f = open(file_, "r")
    lines = f.readlines()
    for line in lines:
        if ".dat" in line:
            return line.split(".dat")[0]+".dat"
    return 0
