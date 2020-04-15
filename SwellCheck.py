# SwellCheck.py
# Date created: 14 April 2020
# Author: Maurizio von Flotow
# Scrape water depth level from USGS sites, then try to use it to predict
# river swell height for getting tchubed.

import requests
import csv
import datetime
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import dates
import pandas as pd
from moving_average import sma

# define date strings to use in the USGS URL
dayLength = 100
endDateStr = (datetime.date.today() - datetime.timedelta(days=0)).strftime("%Y-%m-%d")
startDateStr = (datetime.date.today() - datetime.timedelta(days=dayLength)).strftime("%Y-%m-%d")
# get the last dayLength days of tsv data from the web
# =============================================================================
# URL = 'https://nwis.waterdata.usgs.gov/nwis/uv?cb_00065=on&format=rdb&site_no=14128870&period=&begin_date='+startDateStr+'&end_date='+endDateStr
# page = requests.get(URL)
# =============================================================================

# save page text as .txt file, so we can re-import as .tsv
# there's probably a better way to do this but I can't be bothered now that it works
filename = "Output.txt"
# =============================================================================
# with open(filename, "w") as text_file:
#     print(page.text, file=text_file)
# =============================================================================
# open as .tsv
with open(filename) as fd:
    rd = list(csv.reader(fd, delimiter='\t'))
# remove empty lines and header comments
parsed = rd[:]
for line in rd:

    if len(line) > 0:
        if line[0] != "USGS":
            parsed.remove(line)
    else:
        parsed.remove(line)
# convert this list of lists to a pandas dataframe, then extract time and depth from data frame
# this works, but the dataframe object could be utilized better
# However this is a more "matlaby" way of doing it imo and thus more comfortable for me
df = pd.DataFrame.from_records(parsed)
time = pd.to_datetime((df[2][:]))
depth = df[4][:].astype(float)
#simple moving average
vals = 100
sma_depth = sma(depth,vals)
time2 = pd.to_datetime((df[2][vals-1:df.size]))
# calculate derivative
depthDeriv = sma_depth.diff()/(time2.diff().dt.total_seconds())

# plot data
fig = plt.figure()
fig.set_size_inches(50 ,40)
ax1 = fig.add_subplot(2,1,1)
ax1.plot(time, depth)
ax1.plot(time2,sma_depth)
plt.title('Bonneville Gage Height (ft), last '+ str(dayLength) +' days')
plt.grid()

ax1 = fig.add_subplot(2,1,2)
ax1.plot(time, depthDeriv)
plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
plt.title('Gage Height Derivative (ft/s)')
fig.autofmt_xdate()
plt.grid()
plt.show()