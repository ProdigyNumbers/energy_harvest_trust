#import required libraries
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import wget
from datetime import date
from datetime import timedelta
import os  
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
import numpy as np
import warnings
warnings.filterwarnings('ignore')
#download file
wget.download('https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/csv/SUOMI_VIIRS_C2_South_Asia_24h.csv', out='/home/ec2-user/s3vol/FireData/rawfiles')
#generate date str
today = date.today()
date_str = today.strftime("%m-%d-%Y")
print(f'************ {date_str} *************')
yesterday = date.today() - timedelta(1)
date_dir = yesterday.strftime("%m%d%Y")
yesterday = yesterday.strftime("%m-%d-%Y")
print(f'yesterday is {yesterday}')

filename = 'SUOMI_VIIRS_C2_South_Asia_24h_'+date_str+'.csv'
os.rename('/home/ec2-user/s3vol/FireData/rawfiles/SUOMI_VIIRS_C2_South_Asia_24h.csv', '/home/ec2-user/s3vol/FireData/rawfiles/' + filename)

data = pd.read_csv('/home/ec2-user/s3vol/FireData/rawfiles/'+filename, sep=',')
data = data.rename(index= str, columns={"acq_date": "ACQ_DATE", "acq_time": "ACQ_TIME", "satellite": "SATELLITE", "latitude": "LATTITUDE","longitude": "LONGITUDE", "bright_ti4": "Bright_Ti4", "bright_ti5":"Bright_Ti5", "confidence": "CONFIDENCE", "daynight":"Day_Night", "scan": "SCAN","frp":"FRP","track":"TRACK","version":"VERSION"})
data["INSTRUMENT"] = 'VIIRS'
#reorder columns
data= data[["LATTITUDE", "LONGITUDE", "Bright_Ti4", "SCAN", "TRACK", "ACQ_DATE", "ACQ_TIME", "SATELLITE", "INSTRUMENT", "CONFIDENCE", "VERSION", "Bright_Ti5", "FRP","Day_Night"]]
data["SATELLITE"].replace("N","S-NPP", inplace=True)
data["geometry"] = data.apply(lambda x: Point((float(x.LONGITUDE), float(x.LATTITUDE))), axis=1)
data = gpd.GeoDataFrame(data, geometry="geometry")

data.crs= "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs"
data.to_file('/home/ec2-user/s3vol/FireData/outputfiles/'+filename[:len(filename)-4] + '.shp', driver="ESRI Shapefile")

dat = "/home/ec2-user/s3vol/FireData/shapefiles/gadm36_IND_3.shp"
dat1= '/home/ec2-user/s3vol/FireData/outputfiles/'+filename[:len(filename)-4] + '.shp'

India= gpd.read_file(dat)
points= gpd.read_file(dat1)

India.crs == points.crs

#execute spatial join
join = gpd.sjoin(points, India, how="inner", op="within")

#save the output
outfp = '/home/ec2-user/s3vol/FireData/outputfiles/'+filename[:len(filename)-4] + '_join.shp'
join.to_file(outfp)

shapefile = gpd.read_file('/home/ec2-user/s3vol/FireData/outputfiles/'+filename[:len(filename)-4] + '_join.shp')
data1 = shapefile[["LATTITUDE", "LONGITUDE", "Bright_Ti4", "SCAN", "TRACK", "ACQ_DATE", "ACQ_TIME", "SATELLITE","INSTRUMENT", "CONFIDENCE", "VERSION", "Bright_Ti5", "FRP",  "NAME_0", "NAME_1", "NAME_2",  "NAME_3"]].copy()
data1["ACQ_DATE"] = pd.to_datetime(data1["ACQ_DATE"])
data1["ACQ_DATE"] = data1["ACQ_DATE"].dt.strftime('%m-%d-%Y')
data1.index.name= "FID"
data1['Total_Area'] = data1['SCAN']*data1['TRACK']
#save data as csv file
data2 = data1[data1.ACQ_DATE == yesterday]
data2.to_csv('/home/ec2-user/s3vol/FireData/outputfiles/SUOMI_VIIRS_C2_South_Asia_24h_' +yesterday + '_output.csv', sep=',', date_format="%m-%d-%Y")
data2 = data1[data1.ACQ_DATE == date_str]
data2.to_csv('/home/ec2-user/s3vol/FireData/outputfiles/SUOMI_VIIRS_C2_South_Asia_24h_' +date_str + '_output.csv', sep=',', date_format="%m-%d-%Y")

# calucalte firecount and generate fire_mapping_on_ file
dat = pd.read_csv('/home/ec2-user/s3vol/FireData/outputfiles/SUOMI_VIIRS_C2_South_Asia_24h_' + yesterday + '_output.csv')
grouped_frp = dat.groupby(["NAME_1", "NAME_2", "NAME_3"])['FRP'].agg('sum')
grouped_frp = grouped_frp.to_frame().reset_index()
Taluk_frp = grouped_frp['FRP']
grouped_frp = dat.groupby(["NAME_1", "NAME_2", "NAME_3"])['Total_Area'].agg('sum')
grouped_frp = grouped_frp.to_frame().reset_index()
Taluk_Total = grouped_frp['Total_Area']
Taluk_with_frp = dat.groupby(["NAME_1", "NAME_2", "NAME_3"]).size()
Taluk_with_frp = Taluk_with_frp.to_frame().reset_index()
Taluk_with_frp.columns = ["State", "District", "Taluk", "Taluk_Count"]
Taluk_with_frp['Taluk_Frp'] = Taluk_frp
Taluk_with_frp['Taluk_Total'] = Taluk_Total


grouped_frp = dat.groupby(["NAME_1", "NAME_2"])['FRP'].agg('sum')
grouped_frp = grouped_frp.to_frame().reset_index()
dist_frp = grouped_frp['FRP']
grouped_frp = dat.groupby(["NAME_1", "NAME_2"])['Total_Area'].agg('sum')
grouped_frp = grouped_frp.to_frame().reset_index()
dist_Total = grouped_frp['Total_Area']
District_with_frp = dat.groupby(["NAME_1", "NAME_2"]).size()
District_with_frp = District_with_frp.to_frame().reset_index()
District_with_frp.columns = ["State", "District", "District_Count"]
District_with_frp['District_Frp'] = dist_frp
District_with_frp['District_Total'] = dist_Total

grouped_frp = dat.groupby(["NAME_1"])['FRP'].agg('sum')
grouped_frp = grouped_frp.to_frame().reset_index()
state_frp = grouped_frp['FRP']
grouped_frp = dat.groupby(["NAME_1"])['Total_Area'].agg('sum')
grouped_frp = grouped_frp.to_frame().reset_index()
state_Total = grouped_frp['Total_Area']
State_with_frp = dat.groupby(["NAME_1"]).size()
State_with_frp = State_with_frp.to_frame().reset_index()
State_with_frp.columns = ["State", "State_Count"]
State_with_frp['State_Frp'] = state_frp
State_with_frp['State_Total'] = state_Total

val_frp = State_with_frp.merge(District_with_frp, left_on='State', right_on='State')
res_frp = val_frp.merge(Taluk_with_frp,on='District')
res_frp = res_frp[res_frp.State_x == res_frp.State_y]
res_frp = res_frp.drop(['State_y'],axis=1)
res_frp = res_frp.rename(columns={"State_x": "State"})

grouped = India.groupby(["NAME_1", "NAME_2", "NAME_3"]).size()
Ind_frp = grouped.to_frame().reset_index()
Ind_frp.columns = ["State", "District", "Taluk", "Count"]
Ind_frp['State_count'] = 0
Ind_frp['District_count'] = 0
Ind_frp['Taluk_Count'] = 0
Ind_frp['State_Frp'] = 0
Ind_frp['District_Frp'] = 0
Ind_frp['Taluk_Frp'] = 0
Ind_frp['State_Total'] = 0
Ind_frp['District_Total'] = 0
Ind_frp['Taluk_Total'] = 0



for states in res_frp.State.unique():
    indx = res_frp[res_frp.State == states].index[0]  # getting first element
    #print(indx)
    Indexes = Ind_frp[Ind_frp.State == states].index
    districts = res_frp[res_frp.State == states].District.unique()
    #print(districts)
    taluks = res_frp[res_frp.State == states].Taluk.unique()
    #print(taluks)
    for i in Indexes:
        # getting state count value by using index and assign to state count in another df
        Ind_frp.loc[i, 'State_count'] = res_frp.at[indx, 'State_Count']
        Ind_frp.loc[i, 'State_Frp'] = res_frp.at[indx, 'State_Frp']
        Ind_frp.loc[i, 'State_Total'] = res_frp.at[indx, 'State_Total']
    for distri in districts:
        temp_df = Ind_frp[Ind_frp.State == states]
        Indexes = temp_df[temp_df.District == distri].index
        #print(Indexes)
        temp_df1 = res_frp[res_frp.State == states]
        temp_df1 = temp_df1[temp_df1.District == distri]
        val = temp_df1['District_Count'].unique()
        val_frp = temp_df1['District_Frp'].unique()
        val_total = temp_df1['District_Total'].unique()
        #print(val)
        for i in Indexes:
            Ind_frp.loc[i, 'District_count'] = val
            Ind_frp.loc[i, 'District_Frp'] = val_frp
            Ind_frp.loc[i, 'District_Total'] = val_total
    for distri in districts:
        for talu in taluks:
            temp_df = Ind_frp[Ind_frp.State == states]
            temp_df = temp_df[temp_df.District == distri]
            Indexes = temp_df[temp_df.Taluk == talu].index
            #print(Indexes)
            temp_df1 = res_frp[res_frp.State == states]
            temp_df2 = temp_df1[temp_df1.District == distri]
            temp_df3 = temp_df2[temp_df2.Taluk == talu]
            val = temp_df3['Taluk_Count'].unique()
            val_frp = temp_df3['Taluk_Frp'].unique()
            val_total = temp_df3['Taluk_Total'].unique()
            #print(val)
            if len(val) and len(val_frp) != 0:
                for i in Indexes:
                    Ind_frp.loc[i, 'Taluk_Count'] = val
                    Ind_frp.loc[i, 'Taluk_Frp'] = val_frp
                    Ind_frp.loc[i, 'Taluk_Total'] = val_total

Ind_frp = Ind_frp[['State', 'State_count', 'State_Frp', 'State_Total', 'District', 'District_count','District_Frp', 'District_Total', 'Taluk', 'Taluk_Count', 'Taluk_Frp', 'Taluk_Total']]
Ind_frp = Ind_frp.rename(columns={"State_Total": "State_Pixarea","District_Total": "District_Pixarea", "Taluk_Total": "Taluk_Pixarea"})


print('saving data to file')
Ind_frp.to_csv('/home/ec2-user/s3vol/FireData/outputfiles/'+'Fires_Mapping_on_' +yesterday+'.csv', index=False)

df = pd.read_csv('/home/ec2-user/s3vol/FireData/outputfiles/'+'Fires_Mapping_on_'+yesterday+'.csv', sep=',')
#mapping
print('Read file and started mapping')
print('Now,Mapping India wide Taluk Level Fires')
# df1 = df[['Taluk', 'Taluk_Count']]
# merged1 = India.set_index('NAME_3').join(df1.set_index('Taluk'))
df1 = df[['State', 'District', 'Taluk', 'Taluk_Count']]
talu_df = India[['NAME_1', 'NAME_2', 'NAME_3', 'geometry']]
talu_df = talu_df.rename(columns={"NAME_1": "State", "NAME_2": "District", "NAME_3": "Taluk"}, errors="raise")
merged1 = talu_df.merge(df1, on=['State', 'District', 'Taluk'])
variable = 'Taluk_Count'
vmin, vmax = 1, df1.Taluk_Count.max()
fig, ax = plt.subplots(1, figsize=(12, 10))
xmax = round(0.8*vmax)
if xmax % 10 != 0 or xmax == 0:
    xmax = xmax + (10 - (xmax % 10))
if vmax < 10:
    vmax = 10
vals = list(np.arange(1, xmax+1, int(0.1*(xmax))))
bounds = [0]
bounds.extend(vals)
bounds.append(vmax+xmax)# adding a larger number as boundary at end
cmap = mpl.colors.ListedColormap(["#03a9fc", "#00ffff", "#00ff40", "#bfff00", "#ffff00", "#ffbf00", "#ff8000", "#ff4000", "#800000"])
cmap.set_under("#FFFFFF")
cmap.set_over("#FF00FF")
norm = mpl.colors.BoundaryNorm(vals, cmap.N)
im = merged1.plot(column=variable, linewidth=0.2, ax=ax,edgecolor='0.8', cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
ax.axis('off')
ax.set_title(f'VIIRS-SNPP Day-Night Fire Detection\nIndia - Taluk Level,{yesterday} UTC', fontdict={'fontsize': '25', 'fontweight': '3'})
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
a = fig.colorbar(sm, orientation='horizontal', extend='both', boundaries=bounds, ticks=vals, pad=0.05)
a.ax.set_title('Number Of Fires', fontsize=16, weight='bold')
fig.text(0.85, 0.3, '@USRA/MSFC', fontsize=20,color='black', ha='right', va='bottom', alpha=0.5)
fig.savefig('/home/ec2-user/s3vol/home/' + date_dir + '/indiataluk/' + 'INDIA_TALUK_SNP_VIIRS_FC_' + date_dir + '.png', dpi=150)
fig.clf()
ax.clear()

print('Mapping India wide District Level Fires')
# df1 = df[['District', 'District_count']]
# merged1 = India.set_index('NAME_2').join(df1.set_index('District'))
# df1 = df[['State', 'District', 'District_count']]
df1 = df.groupby(['State', 'District', 'District_count']).size()
df1 = df1.to_frame().reset_index()
distro = India[['NAME_1', 'NAME_2', 'geometry']]
distro = distro.rename(columns={"NAME_1": "State", "NAME_2": "District"}, errors="raise")
merged1 = distro.merge(df1, on=['State', 'District'])
variable = 'District_count'
vmin, vmax = 1, df1.District_count.max()
fig, ax = plt.subplots(1, figsize=(12, 10))
xmax = round(0.8*vmax)
if xmax % 10 != 0 or xmax == 0:
    xmax = xmax + (10 - (xmax % 10))
if vmax < 10:
    vmax = 10
vals = list(np.arange(1, xmax+1, int(0.1*(xmax))))
bounds = [0]
bounds.extend(vals)
bounds.append(vmax+xmax)
cmap = mpl.colors.ListedColormap(["#03a9fc", "#00ffff", "#00ff40", "#bfff00", "#ffff00", "#ffbf00", "#ff8000", "#ff4000", "#800000"])
cmap.set_under("#FFFFFF")
cmap.set_over("#FF00FF")
norm = mpl.colors.BoundaryNorm(vals, cmap.N)
im = merged1.plot(column=variable, linewidth=0.2, ax=ax,edgecolor='0.8', cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
ax.axis('off')
ax.set_title(f'VIIRS-SNPP Day-Night Fire Detection\nIndia - District Level,{yesterday} UTC', fontdict={'fontsize': '25', 'fontweight': '3'})
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
# empty array for the data range
sm.set_array([])
# add the colorbar to the figure
a = fig.colorbar(sm, orientation='horizontal', extend='both', boundaries=bounds, ticks=vals, pad=0.05)
a.ax.set_title('Number Of Fires', fontsize=16, weight='bold')
fig.text(0.85, 0.3, '@USRA/MSFC', fontsize=20,color='black', ha='right', va='bottom', alpha=0.5)
fig.savefig('/home/ec2-user/s3vol/home/' + date_dir + '/indiadist/' + 'INDIA_DISTI_SNP_VIIRS_FC_' + date_dir + '.png', dpi=150)
fig.clf()
ax.clear()

print('Mapping India wide State Level Fires')
India = India[['NAME_1', 'geometry']]
state_shape = India.dissolve('NAME_1')
# df1 = df[['State', 'State_count']]
df1 = df.groupby(['State', 'State_count']).size()
df1 = df1.to_frame().reset_index()
merged1 = state_shape.join(df1.set_index('State'))
variable = 'State_count'
vmin, vmax = 1, df1.State_count.max()
fig, ax = plt.subplots(1, figsize=(12, 10))
xmax = round(0.8*vmax)
if xmax % 10 != 0 or xmax == 0:
    xmax = xmax + (10 - (xmax % 10))
if vmax < 10:
    vmax = 10
vals = list(np.arange(1, xmax+1, int(0.1*(xmax))))
bounds = [0]
bounds.extend(vals)
bounds.append(vmax+xmax)
cmap = mpl.colors.ListedColormap(["#03a9fc", "#00ffff", "#00ff40", "#bfff00", "#ffff00", "#ffbf00", "#ff8000", "#ff4000", "#800000"])
cmap.set_under("#FFFFFF")
cmap.set_over("#FF00FF")
norm = mpl.colors.BoundaryNorm(vals, cmap.N)
im = merged1.plot(column=variable, linewidth=0.8, ax=ax, edgecolor='0.8', cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
ax.axis('off')
ax.set_title(f'VIIRS-SNPP Day-Night Fire Detection\nIndia - State Level,{yesterday} UTC', fontdict={'fontsize': '25', 'fontweight': '3'})
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
a = fig.colorbar(sm, orientation='horizontal', extend='both',boundaries=bounds, ticks=vals, pad=0.05)
a.ax.set_title('Number Of Fires', fontsize=16, weight='bold')
fig.text(0.85, 0.3, '@USRA/MSFC', fontsize=20,color='black', ha='right', va='bottom', alpha=0.5)
fig.savefig('/home/ec2-user/s3vol/home/' + date_dir + '/indiastate/' +'INDIA_STATE_SNP_VIIRS_FC_' + date_dir + '.png', dpi=150)
fig.clf()
ax.clear()
