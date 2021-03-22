from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import subprocess, sys, os
import shutil
import xrmc
from DetectorResponse import *
import Configure
import Elements
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE

global DETECTOR
DETECTOR = rivelatore()

class CustomCompound:
    def __init__(__self__, root=None):
        __self__.master = Toplevel(master=root.master)
        __self__.master.resizable(False,False)
        __self__.master.title("Custom coumpound maker")
        __self__.build_widgets

    def build_widgets(__self__):
        __self__.frame = Frame(__self__.master, padx=3, pady=3, sticky=N+S+W+E)
        __self__.frame.grid(row=0, column=0)
        label = Label(__self__.frame, text="UNDER CONSTRUCTION").grid(row=0,column=0)


class SDD_window:
    def __init__(__self__,parent):
        __self__.master = Toplevel(master=parent.master)
        __self__.parent = parent
        __self__.Frame = ttk.LabelFrame(__self__.master, text="Detector properties")
        __self__.Labels = Frame(__self__.Frame, padx=10, pady=10)
        __self__.Buttons = Frame(__self__.Frame, padx=15, pady=10)
        __self__.Frame.grid(padx=15, pady=15)
        __self__.Labels.grid(row=0,column=0)
        __self__.Buttons.grid(row=1,column=0,columnspan=2)
        __self__.init_variables()
        __self__.write_from_init()
        __self__.build_widgets()
    
    def init_variables(__self__):
        __self__.Z = IntVar()
        __self__.thickness = DoubleVar()
        __self__.win_z = IntVar()
        __self__.win_thickness = DoubleVar()
        __self__.fstart = DoubleVar()
        __self__.fstop = DoubleVar()
        __self__.air_thickness = DoubleVar()
        __self__.noise = DoubleVar()
        __self__.fano = DoubleVar()
        __self__.escape_perc = DoubleVar()
        __self__.tail = BooleanVar()
        __self__.escape = BooleanVar()

    def kill(__self__):
        __self__.master.grab_release()
        __self__.parent.master.focus_set()
        __self__.master.destroy()

    def save(__self__):
        print("saving...")
        global DETECTOR
        DETECTOR.setup(__self__)
        __self__.kill()

    def write_from_init(__self__):
        p = os.path.join(os.path.dirname(__file__),"detector.ini")
        if os.path.exists(p):
            pass
        else:
            return
        f = open(p,"r")
        lines = f.readlines()
        for line in lines:
            line = line.replace("\n","")
            if "DETECTOR_Z" in line: __self__.Z.set(int(line.split("=")[-1]))
            elif "MATERIAL_THICK" in line: __self__.thickness.set(float(line.split("=")[-1]))
            elif "WINDOW_Z" in line: __self__.win_z.set(int(line.split("=")[-1]))
            elif "WINDOW_THICK" in line: __self__.win_thickness.set(float(line.split("=")[-1]))
            elif "FWHM_START" in line: __self__.fstart.set(float(line.split("=")[-1]))
            elif "FWHM_STOP" in line: __self__.fstop.set(float(line.split("=")[-1]))
            elif "AIR_THICK" in line: __self__.air_thickness.set(float(line.split("=")[-1]))
            elif "NOISE" in line: __self__.noise.set(float(line.split("=")[-1]))
            elif "FANO" in line: __self__.fano.set(float(line.split("=")[-1]))
            elif "ESCAPE_PERC" in line: __self__.escape_perc.set(float(line.split("=")[-1]))
            elif "TAIL" in line: __self__.tail.set(bool(int(line.split("=")[-1])))
            elif "ESCAPE" in line: __self__.escape.set(bool(int(line.split("=")[-1])))
        return

    def build_widgets(__self__):
        Label(__self__.Labels, text="Detector Z").grid(row=0, column=0, sticky=W)
        Label(__self__.Labels, text="Material thickness").grid(row=1, column=0, sticky=W)
        Label(__self__.Labels, text="Window Z").grid(row=2, column=0, sticky=W)
        Label(__self__.Labels, text="Window thickness").grid(row=3, column=0, sticky=W)
        Label(__self__.Labels, text="FWHM start").grid(row=4, column=0, sticky=W)
        Label(__self__.Labels, text="FWHM stop").grid(row=5, column=0, sticky=W)
        Label(__self__.Labels, text="Air thickness").grid(row=6, column=0, sticky=W)
        Label(__self__.Labels, text="Detector noise").grid(row=7, column=0, sticky=W)
        Label(__self__.Labels, text="Fano factor").grid(row=8, column=0, sticky=W)
        Label(__self__.Labels, text="Escape peak (%) 0-1").grid(row=9,column=0, sticky=W)
        ttk.Entry(__self__.Labels, textvariable=__self__.Z).grid(row=0, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.thickness).grid(row=1, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.win_z).grid(row=2, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.win_thickness).grid(row=3, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.fstart).grid(row=4, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.fstop).grid(row=5, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.air_thickness).grid(row=6, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.noise).grid(row=7, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.fano).grid(row=8, column=1)
        ttk.Entry(__self__.Labels, textvariable=__self__.escape_perc).grid(row=9, column=1)
        ttk.Checkbutton(__self__.Buttons, text="Use tail model", variable=__self__.tail).grid(
                row=0, column=0, padx=(0,10))
        ttk.Checkbutton(__self__.Buttons, text="Escape peaks corr", 
                variable=__self__.escape).grid(row=0, column=1, padx=(10,0))
        ttk.Button(__self__.Buttons, text="Cancel", command=__self__.kill).grid(
                row=1, column=0, pady=(15,0))
        ttk.Button(__self__.Buttons, text="Save", command=__self__.save).grid(
                row=1, column=1, pady=(15,0))
        __self__.master.update_idletasks()
        __self__.master.focus_set()
        __self__.master.grab_set()


class Root:
    def __init__(__self__):
        __self__.master = Tk()
        __self__.master.resizable(False, False)
        __self__.menu = Menu(__self__.master, tearoff=0)
        __self__.dropdown = Menu(__self__.menu, tearoff=0)
        __self__.dropdown.add_command(label="Load input", 
                command=__self__.load_input)
        __self__.dropdown.add_command(label="Load DAT", 
                command=load_dat)
        __self__.dropdown.add_command(label="Configure detector", 
                command=__self__.configure_SDD)
        __self__.menu.add_cascade(label="Options", menu=__self__.dropdown)
        __self__.master.config(menu=__self__.menu)
        __self__.layer_count = int(0)
        __self__.info = StringVar()
        __self__.layers = []
        __self__.thicknesses = []
        __self__.comboboxes = []
        __self__.build_widgets()

    def load_input(__self__):
        f = filedialog.askopenfilename(title="Open input file",
                        filetypes=[("Input file","*.dat")])
        if f is not "":
            files, __self__.out = Configure.load_input(f)
            __self__.temp = []
            local_path = os.path.dirname(os.path.abspath(__file__))

            ##################################################
            # Copies all relevant files to working directory #
            ##################################################
            for fpath, fname in files:
                destination = os.path.join(local_path,fname)
                try: 
                    shutil.copy(fpath,destination)
                    __self__.temp.append(destination)
                    files_in_root = 0
                except: 
                    files_in_root = 1
                    pass
            #################################################################
            #NOTE: If the input file selected is in the working directory,  #
            # there it no need to create a temporary input file             #
            #################################################################
            if not files_in_root:
                shutil.copy(f,os.path.join(local_path,"temp_input.dat"))
                __self__.temp.append(os.path.join(local_path,"temp_input.dat"))
                __self__.launch(__input__="temp_input.dat")
            else: __self__.launch(__input__=f)
            #################################################################

    def configure_SDD(__self__):
        SDD_window(__self__)        
        return

    def build_widgets(__self__):
        __self__.frame = LabelFrame(__self__.master, text="Main Panel",padx=6,pady=6)
        __self__.frame2 = LabelFrame(__self__.master, text="Layer Info",padx=6,pady=6)
        __self__.buttons = Frame(__self__.master)
        __self__.statusbox = Label(__self__.master, 
                textvariable=__self__.info,
                anchor=W,
                relief=SUNKEN)

        Label(__self__.frame, text="Layer Material").grid(row=0,column=0,columnspan=2)
        Label(__self__.frame, text="Layer\nThickness (um)").grid(row=0,column=2)
        __self__.add = ttk.Button(__self__.frame, text="Add Layer",
                command=__self__.insert_layer)

        w = 7
        __self__.species = Listbox(__self__.frame2, width=w)
        __self__.quantity = Listbox(__self__.frame2, width=w+3)

        __self__.insert_layer()

        __self__.EraseVar = BooleanVar()
        __self__.EraseVar.set(1)
        __self__.erase = ttk.Checkbutton(__self__.buttons, text="Erase generated files", variable=__self__.EraseVar)
        __self__.accept = ttk.Button(__self__.buttons, text="Go!",
                command=__self__.launch)
        __self__.cancel = ttk.Button(__self__.buttons, text="Exit",
                command=__self__.master.destroy)

        __self__.frame.grid(row=0, column=0, padx=3, pady=3,sticky=N+S)
        __self__.frame2.grid(row=0, column=1, padx=3, pady=3,sticky=N+S)
        __self__.buttons.grid(row=1, padx=3, pady=3)
        __self__.statusbox.grid(row=2, columnspan=2, sticky=W+E)
        __self__.species.grid(row=0, column=0, sticky=N+S)
        __self__.quantity.grid(row=0, column=1, sticky=N+S)
        __self__.accept.grid(row=0, column=0)
        __self__.cancel.grid(row=0, column=1)
        __self__.erase.grid(row=0,column=2)
        return

    def insert_layer(__self__, e=""):
        values = sorted([i for i in Elements.ListDatabase().keys()])
        values.insert(0,"Custom")

        __self__.layer_count += 1

        label = f"Layer {__self__.layer_count}"
        Label(__self__.frame, text=label).grid(row=__self__.layer_count,column=0)

        # Comboboxes in the middle
        __self__.layers.append(StringVar())
        __self__.thicknesses.append(DoubleVar())

        cbb = ttk.Combobox(__self__.frame, values=values, 
                textvariable=__self__.layers[__self__.layer_count-1])
        cbb.grid(row=__self__.layer_count, column=1, padx=(6,3))
        cbb.bind("<<ComboboxSelected>>",__self__.write_layer_info)
        __self__.comboboxes.append(cbb)
        ttk.Entry(__self__.frame, textvariable=__self__.thicknesses[__self__.layer_count-1], 
                width=7).grid(row=__self__.layer_count, column=2, padx=(3,6))

        __self__.add.grid(row=__self__.layer_count+1, column=0, columnspan=3,pady=(8,8))
        return
        
    def write_layer_info(__self__, e=""):
        value = e.widget.get()
        if value == "Custom": 
            CustomCompound(root=__self__)
        else:
            __self__.species.delete(0,END)
            __self__.quantity.delete(0,END)
            c = Elements.compound()
            c.set_compound(value)
            for el,w in c.weight.items():
                __self__.species.insert(END,el)
                __self__.quantity.insert(END,f"{w*100:.2f}%")
        return

    def launch(__self__,__input__=None):
        global DETECTOR
        if not DETECTOR.Configured:
            messagebox.showerror("Detector not configured!",
                    "SDD Detector parameters are not configured!")
            return

        if __input__ is not None:
            input_file, output_file = __input__,__self__.out
            exe_str = r"xrmc {}".format(input_file)
            print("SIMULATION START!")
            p1 = subprocess.Popen(exe_str,  stderr=subprocess.PIPE)#, stdout=subprocess.PIPE)
            p1.wait()
            print("SIMULATION DONE")
            for file_ in __self__.temp:
                os.remove(file_)
                print(f"Removed {file_}")

        else:
            compounds, materials, thicknesses = [], [], []
            skipped_materials, skipped_thick = [], []
            for i in range(len(__self__.layers)):
                if __self__.layers[i].get() \
                        and __self__.layers[i].get() != "Custom"\
                        and __self__.thicknesses[i].get() > 0.0:
                    materials.append(__self__.layers[i].get())
                    thicknesses.append(__self__.thicknesses[i].get())
                else: 
                    skipped_materials.append(__self__.layers[i].get())
                    skipped_thick.append(i)
            if skipped_materials != []:
                text1 = ""
                for mat, l in zip(skipped_materials,skipped_thick):
                    if mat == "": mat = "Empty"
                    text1 = str(mat) + f" - Layer {l}"
                messagebox.showinfo("Invalid layers!",f"Ignoring layers: {text1}")
            for material in materials:
                a = Elements.compound()
                a.set_compound(material)
                compounds.append(a)

            pars = Configure.Parser()
            pars.get_planes(thicknesses)
            input_file, output_file = pars.write_inputs(compounds)

            exe_str = r"xrmc {}".format(input_file)
            print("SIMULATION START!")
            p1 = subprocess.Popen(exe_str,  stderr=subprocess.PIPE)#, stdout=subprocess.PIPE)
            p1.wait()
            print("SIMULATION DONE")
            if __self__.EraseVar.get():
                for f in pars.temporary_files:
                    try: 
                        os.remove(f)
                        print(f"Got rid of {f}")
                    except:
                        print(f"Could not remove {f}!")

        print("Output file: ", output_file)
        load_dat(output_file=output_file)
        return

def save_to_file(data, path):
    if not isinstance(data,np.ndarray):
        print("Invalid data format")
        return
    f = open(path,"w+")
    for i in range(data.shape[0]):
        f.write(f"{data[i]}\n")
    f.close()

def load_dat(output_file=None):
    global DETECTOR
    if not DETECTOR.Configured:
        messagebox.showerror("Detector not configured!",
                "SDD Detector parameters are not configured!")
        return
    if output_file is None:
        f = filedialog.askopenfilename(title="Open DAT file",
                        filetypes=[("DAT output file","*.dat")])
        if f is not "":
            output_file = f
        else: return

    data = xrmc.Output(output_file)
    nchan = data[:,:,0,0].sum(0).shape[0]

    DETECTOR.MCA_chns = nchan
    DETECTOR.energy_max = data.Emax

    data = SDD_convolution_with_tail(
            data,
            nchan,
            3,              #scatt_order
            DETECTOR)

    data = detector_efficiency_convolution(
            data,
            nchan,
            3,
            DETECTOR)

    spec = np.zeros(nchan, dtype=np.float32)
    for k in range(3):
        spec += data[k,:]
    save = messagebox.askyesno("Save","Save output to txt?")
    if save:
        f = filedialog.asksaveasfile(mode="w",
                defaultextension=".txt",
                filetypes=[("Text file","*.txt")],
                title="Save output:")
        if f is not None:
            save_to_file(spec,f.name)
    plt.semilogy(spec)
    plt.show()
    return

if __name__.endswith("__main__"):
    root = Root()
    root.master.mainloop()
