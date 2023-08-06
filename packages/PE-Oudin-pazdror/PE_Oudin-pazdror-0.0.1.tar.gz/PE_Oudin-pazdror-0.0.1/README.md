# potEvap

Compute PE (Potential Evapotranspiration) using the formula from Oudin et al. (2005). 

This is a pure python implementation of the R - AirGR PEdaily_Oudin function.

Original source found at https://github.com/cran/airGR/blob/master/R/PEdaily_Oudin.R

AirGR package can be found at https://cran.r-project.org/package=airGR 


Changes from the original (R package) include:
 - Support single day as well as multiple days (list, numpy array, pandas etc.). 
 - Get latitude in degrees or radians (default degrees).
 - Can choose output units (useful for GR2M and GR2A)

## Usage:

`from potEvap import potEvap`

For single value:
```
temp = 20  # Degrees celcius
date = datetime(2018,1,1)
lat = 32  # Degrees (but can be set to radians)
latUnit = 'deg'  # Optional, and default. Can also be 'rad'
out_units = 'mm/day'  # Optional, and default. Can also be 'mm/month' or 'mm/year'

potEvap(temp, date, lat, latUnit, out_units)
```

For multiple values (list, pandas series etc.):
```
temp = [20, 25] # Degrees celcius
date = [datetime(2018,1,1), datetime(2018,1,1)]
lat = 32 # Degrees (but can be set to radians)
latUnit = 'deg'  # Optional, and default. Can also be 'rad'
out_units = 'mm/day'  # Optional, and default. Can also be 'mm/month' or 'mm/year'

potEvap(temp, date, lat, latUnit, out_units)
```
