import numpy as np
import sys, os
from math import erfc
try: import xraylib as xlib
except: 
    print("Failed to import xraylib. Aborting...")
    sys.exit(1)

class rivelatore:
    def __init__(__self__):
        __self__.Detect_Z = int
        __self__.Detect_thickness = float
        __self__.Detect_window_Z = int
        __self__.Detect_window_thickness = float
        __self__.FWHM_start = float
        __self__.FWHM_stop = float
        __self__.AirThick = float
        __self__.MCA_chns = int
        __self__.noise = float
        __self__.Fano = float
        __self__.EscapePeakPercentage = float
        __self__.energy_max = float
        __self__.scatt_orders =  int
        __self__.tail_model = bool
        __self__.EscapePeak = bool

    def setup(__self__, w):
        __self__.Detect_Z = int(w.Z.get())
        __self__.Detect_thickness = float(w.thickness.get())
        __self__.Detect_window_Z = int(w.win_z.get())
        __self__.Detect_window_thickness = float(w.win_thickness.get())
        __self__.FWHM_start = float(w.fstart.get())
        __self__.FWHM_stop = float(w.fstop.get())
        __self__.AirThick = float(w.air_thickness.get())
        __self__.noise = float(w.noise.get())
        __self__.Fano = float(w.fano.get())
        __self__.EscapePeakPercentage = float(w.escape_perc.get())
        __self__.tail_model = bool(w.tail.get())
        __self__.EscapePeak = bool(w.escape.get())

def detector_efficiency_convolution(
        data,
        spectrum_size,
        scatt_orders,
        rivelatore):
    
    Z = rivelatore.Detect_Z
    thickness = rivelatore.Detect_thickness
    Z_window = rivelatore.Detect_window_Z
    window_thick = rivelatore.Detect_window_thickness
    energy_max = rivelatore.energy_max

    #FILE *file_in,*file_out;
    i,j,k = 0,0,0
    sigma_var = 0
    density, density1 = 0, 0 
    density_air = 0.0012
    attenuation = 0
    attenuation_window = 0 
    attenuation_air = 0
    energy = 0
    air_thickness = rivelatore.AirThick

    #xrl_error **error;

    spectrum_temp = np.zeros(spectrum_size, dtype=np.double)
    spectrum_conv = np.zeros([scatt_orders,spectrum_size], dtype=np.double)

    k=0
    print("Efficiency correction")
    #########################################################################
    #NOTE: No longer performs the convolution PER ORDER. Instead, we sum
    #all orders and apply it only once
    #########################################################################
    for k in range(scatt_orders):
        spectrum_temp += data[k,:] 
    #########################################################################

        density = xlib.ElementDensity(Z)
        density1 = xlib.ElementDensity(Z_window)
        i=0
        for i in range(spectrum_size): 
            energy = i*rivelatore.energy_max/rivelatore.MCA_chns
            print(f"{energy} - Progress {k}: {i}/{spectrum_size}", end="\r")
            if energy > 0:
                attenuation = xlib.CS_Total(Z, energy)
                attenuation_window = xlib.CS_Total(Z_window, energy)
                attenuation_air = 0.7804 * xlib.CS_Total(7, energy) + 0.20946 * xlib.CS_Total(8, energy) + 0.00934 * xlib.CS_Total(18, energy)
                spectrum_conv[k][i] = spectrum_temp[i] * (1.0-np.exp(-attenuation*thickness*density)) * np.exp(-attenuation_window * window_thick * density1-attenuation_air * air_thickness*density_air)
            else:
                spectrum_conv[k][i] = 0.0
    return spectrum_conv

def SDD_convolution_with_tail(
        data,
        num_chns, 
        scatt_orders,
        rivelatore):

    i,j,k,m = 0,0,0,0
    sigma_var, my_sum = 0, 0
    factor = 0
    spectrum_temp = np.zeros(num_chns, dtype=np.double)
    spectrum_conv = np.zeros([scatt_orders,num_chns], dtype=np.double)
    R = np.zeros(num_chns, dtype=np.double)
    step = rivelatore.energy_max/rivelatore.MCA_chns

    A0,A3,A4,A5,B0,X,FWHM = 0,0,0,0,0,0,0
    alpha,a,b,E0,G,G1,F,E_curr = 0,0,0,0,0,0,0,0
    chan_ref = 0
    print("SDD convolution")

    #########################################################################
    #NOTE: No longer performs the convolution PER ORDER. Instead, we sum 
    #all orders and apply it only once
    #########################################################################
    for m in range(scatt_orders):
        spectrum_temp += data[m,:,0,0] 
    #########################################################################

    a=rivelatore.noise*rivelatore.noise;
    b=2.3548*2.3548*3.85*rivelatore.Fano/1000.0;

    for i in range(1,num_chns):
        print(f"Progress {m}: {i}/{num_chns}", end="\r")
        my_sum=0.0;
        E0=i*step;
        FWHM=np.sqrt(a+b*E0);
        B0=np.sqrt(2.0)/(2.0*np.sqrt(2.0*np.log(2.0)))*FWHM;
        #A0=1.0/(FWHM*np.sqrt(np.pi));
        #B0 = 0.6005612*FWHM
        A0=1.0/(FWHM*1.77245385);
        A3=2.73E-3*np.exp(-0.21*E0)+1.0E-4;
        A4=0.000188*np.exp(-0.00296*(pow(E0,0.763)))+1.355E-5*np.exp(0.968*(pow(E0,0.498)));
        alpha=1.179*np.exp(8.6E-4*(pow(E0,1.877)))- 7.793*np.exp(-3.81/(pow(E0,0.0716)));
        for j in range(1,i+100):
            if j < rivelatore.MCA_chns:
                E_curr=step*j;
                X=(E_curr-E0)/B0;
                G=np.exp(-X*X);
                #G1=exp(-(E_curr-(E0-1.74))*(E_curr-(E0-1.74))/(2*FWHM*FWHM));
                F=erfc(X);
                R[j]=A0*G+0.63*A3+15.0*A4*np.exp(alpha*(E_curr-E0))*F;
                my_sum+=R[j];
            else: break
        for k in range(1,i+100):
            if k < rivelatore.MCA_chns:
                spectrum_conv[m][k]+=R[k]*spectrum_temp[i]/my_sum;
            else: break
    return spectrum_conv

