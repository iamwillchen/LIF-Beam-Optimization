#%%%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as so

def find_nearest(array, value):
    idx = (np.abs(array - value)).argmin()
    return idx

def gauss(x, a, b, c): #normal distribution function
    y = a * np.exp(- (x - b) ** 2 / (2 * c ** 2))
    return y

def RealBeam(z, w0, z0, M):
    top = (z - z0) * 0.00028 * M #0.0028 mm -> 280 nm wavelength of light
    bottom = np.pi * w0 ** 2
    frac = (top / bottom) ** 2
    wr = w0 * np.sqrt((1 + frac))
    return wr
 
def waistCalc(sheetList):
    
    radiusList = []
    
    for i in sheetList:
        raw_data = pd.read_excel('UV 280nm Power to Position Measurements.xlsx',i) #Change this .xlsx file to what you want
        ana_data = np.array(raw_data)
        height_dat = ana_data[:, 0]
        
        up_lim = 0
        low_lim = len(ana_data)

        watt_trials = ana_data[:, 1] #normalizing by subtracitng lowest values
        watt_trials = watt_trials[up_lim:low_lim] - np.min(watt_trials)
        
        height_dat = height_dat[up_lim:low_lim]
        
        STD = ana_data[:, 2] #normalizing STD
        STD = STD[up_lim:low_lim]
        
        watt_trials = watt_trials.astype('float')
        height_dat = height_dat.astype('float')
        
        dydx = np.diff(watt_trials) / np.diff(height_dat)
        dx = height_dat[:-1:]
        
        err_dydx = np.zeros(len(dydx))
        
        for j in range(1, len(dydx) - 1):
            del_x1 = (1 / (height_dat[1] - height_dat[0])) ** 2 * (STD[j + 2]) ** 2
            del_x2 = ((-1) / (height_dat[1] - height_dat[0])) ** 2 * (STD[j + 1]) ** 2
            err_dydx[j - 1] = np.sqrt(del_x1 + del_x2)
        
        gaussfit = so.curve_fit(gauss, dx, dydx)
        numdx = np.linspace(dx[0], dx[-1], 1000)
        
        
        plt.close(0)
        plt.figure(0)
        plt.plot(height_dat, watt_trials, 'k.')
        plt.errorbar(height_dat, watt_trials, yerr = STD, fmt = 'none')
        plt.xlabel('Razor Blade Height (mm)')
        plt.ylabel(r'Power ($\mu$W)')
        plt.title('Power vs. Razor Blade height @ {}'.format(i))
        
        plt.close(1)
        plt.figure(1)
        plt.plot(dx, dydx, 'r.', label = 'Experimental Fitting')
        plt.plot(numdx, gauss(numdx, *gaussfit[0]), 'k-', label = 'Analytical Fitting')
        plt.errorbar(dx, dydx, yerr = err_dydx, fmt = 'none')
        plt.xlabel('Razor Blade Height(mm)')
        plt.ylabel(r'Power per Length ($\mu$W/mm) @')
        plt.legend()
        plt.title('Power per mm vs. Razor Blade Height @ {}'.format(i))
        
        numdydx = gauss(numdx, *gaussfit[0]) #y vals
        max_numdydx = np.max(numdydx) #max y value
        max_idx = find_nearest(numdydx, max_numdydx) #y idx
        radius_norm = numdx - numdx[max_idx] 
        g_intensity = max_numdydx / np.exp(2)
        radius_idx = find_nearest(numdydx, g_intensity)
        radius = np.abs(radius_norm[radius_idx])
        
        radiusList.append(radius)
        
        plt.close(2)
        plt.figure(2)
        plt.plot(radius_norm, numdydx)
    
    return radiusList
#%%
Position_list = ["x = 2","x = 3","x = 4","x = 4.5","x = 5","x = 5.5","x = 6","x = 7","x = 8","x = 9","x = 10"]
mm = 25.4 * np.array([2, 3, 4, 4.5, 5, 5.5, 6, 7, 8, 9, 10])

wz = waistCalc(Position_list)
zdat = np.array(wz)
wzr_fit = so.curve_fit(RealBeam, mm, zdat)
wzr_z = np.linspace(mm[0], mm[-1], 1000)
wzr = RealBeam(wzr_z, *wzr_fit[0])

plt.close(3)
plt.figure(3)
plt.plot(mm[2:6], zdat, 'k.', label = 'Experimental Data')
plt.plot(wzr_z, wzr, 'b', label = 'Analytical Solution')
plt.xlabel('Z Position (mm)')
plt.ylabel('Beam Waist Radius (mm)')
plt.legend()