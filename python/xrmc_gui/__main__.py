from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import subprocess, sys, os
import xrmc
import Configure
import Elements
import matplotlib.pyplot as plt
from subprocess import Popen, PIPE

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


class Root:
    def __init__(__self__):
        __self__.master = Tk()
        __self__.master.resizable(False, False)
        __self__.layer_count = int(0)
        __self__.info = StringVar()
        __self__.layers = []
        __self__.thicknesses = []
        __self__.comboboxes = []
        __self__.build_widgets()

    def build_widgets(__self__):
        __self__.frame = LabelFrame(__self__.master, text="Main Panel",padx=6,pady=6)
        __self__.frame2 = LabelFrame(__self__.master, text="Layer Info",padx=6,pady=6)
        __self__.buttons = Frame(__self__.master)
        __self__.statusbox = Label(__self__.master, 
                textvariable=__self__.info,
                anchor=W,
                relief=SUNKEN)

        __self__.frame.grid(row=0, column=0, padx=3, pady=3,sticky=N+S)
        __self__.frame2.grid(row=0, column=1, padx=3, pady=3,sticky=N+S)
        __self__.buttons.grid(row=1, padx=3, pady=3)
        __self__.statusbox.grid(row=2, columnspan=2, sticky=W+E)

        Label(__self__.frame, text="Layer Material").grid(row=0,column=0,columnspan=2)
        Label(__self__.frame, text="Layer\nThickness (um)").grid(row=0,column=2)
        __self__.add = ttk.Button(__self__.frame, text="Add Layer",
                command=__self__.insert_layer)

        w = 7
        __self__.species = Listbox(__self__.frame2, width=w)
        __self__.quantity = Listbox(__self__.frame2, width=w+3)
        __self__.species.grid(row=0, column=0, sticky=N+S)
        __self__.quantity.grid(row=0, column=1, sticky=N+S)

        __self__.insert_layer()

        __self__.accept = ttk.Button(__self__.buttons, text="Go!",
                command=__self__.launch)
        __self__.cancel = ttk.Button(__self__.buttons, text="Cancel",
                command=__self__.master.destroy)

        __self__.accept.grid(row=0, column=0)
        __self__.cancel.grid(row=0, column=1)

        return

    def insert_layer(__self__, e=""):
        values = sorted([i for i in Elements.ListDatabase().keys()])
        values.insert(0,"Custom")

        __self__.layer_count += 1

        label = f"Layer {__self__.layer_count}"
        Label(__self__.frame, text=label).grid(row=__self__.layer_count,column=0)

        # Comboboxes in the middle
        __self__.layers.append(StringVar())
        __self__.thicknesses.append(IntVar())

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

    def launch(__self__,e=""):
        compounds, materials, thicknesses = [], [], []
        for i in range(len(__self__.layers)):
            if __self__.layers[i].get() \
                    and __self__.layers[i].get() != "Custom"\
                    and __self__.thicknesses[i].get() > 0:
                materials.append(__self__.layers[i].get())
                thicknesses.append(__self__.thicknesses[i].get())
        for material in materials:
            a = Elements.compound()
            a.set_compound(material)
            compounds.append(a)

        pars = Configure.Parser()
        pars.get_planes(thicknesses)
        input_file, output_file = pars.write_inputs(compounds)

        exe_str = r"xrmc {}".format(input_file)
        p1 = subprocess.Popen(exe_str,  stderr=subprocess.PIPE)#, stdout=subprocess.PIPE)
        #while True:
        #    p1.stdout.flush()
        #    output = p1.stdout.readline()
        #    if not output: break

        p1.wait()
        print("SIMULATION DONE")
        for f in pars.temporary_files:
            #os.remove(f)
            print(f"Got rid of {f}")

        print("Output file: ", output_file)
        data = xrmc.Output(output_file) 
        a = data[:,:,0,0].sum(0)
        plt.semilogy(a)
        plt.show()
        return

if __name__.endswith("__main__"):
    root = Root()
    root.master.mainloop()
