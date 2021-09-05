# LIF-Beam-Optimization
This was used to optimize a laser beam and measure the beam waist and convert it into a beam radius as a function of length.

Note: Energies from a laser beam being cut by a razor blade over different increments in the z-direction (Up and downwards of the laser). 
.xlsx file is required for this code to run. Furthermore columns should be in the order of z-position, beam energy in microwatts, and standard deviation.

Version Used: Python 3.7.6

Installation
1. Download and Run python file
2. Change 0.00028 to desired wavelength in mm from nm, (i.e. UV Light at 300 nm -> 0.0003 mm) on line 16
3. Change pd.read_excel('...', i) to pd.read_excel('[Insert Excel File]', i) on Line 27
4. Change Position list to order of sheetlist you want, make sure it is in the [] on Line 93
5. Change the np.array to the inches spaced for the laser beam (x-position) inside np.array([]) on Line 94
6. Run all cells and graphs for figure 0, 1, 2 should show last regressions and data points, and figure 3 is regression
7. [Optional] run code " wzr_fit " to return: Beam Waist Position, Position of Beam Waist, and M^2 value of laser output.

Debug
If .xlsx file is not being shown/running then make sure either .xlsx file is in same directory as this .py file or the directory is pathed towards there.
