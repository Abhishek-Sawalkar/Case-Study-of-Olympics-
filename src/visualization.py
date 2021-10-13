
#%%
import folium
import geopandas as gpd
import pandas as pd
import branca

import dataset

def visualize(year="whole"):

    # Fetching data
    df, global_polygon = dataset.df_for_visualization()
    df = pd.DataFrame(df)
    global_polygon = pd.DataFrame(global_polygon)
    
    if year=="whole":
        temp = df[['gold_medal', 'silver_medal', 'bronze_medal', 'total', 'country_code']].groupby('country_code').agg(sum)
        temp = temp.reset_index(drop=False)
        temp['id'] = temp['country_code']
        temp = temp.merge(global_polygon, on='id', how='inner')
        Temp = gpd.GeoDataFrame(temp)

    elif(len(df[df.year==int(year)])==0):
        return "Olympics was not held at this year"
    
    else:
        Temp = gpd.GeoDataFrame(df[df.year==int(year)])

    def rd2(x):
        return round(x, 2)

    minimum, maximum = Temp["total"].quantile([0.05, 0.95])
    mean = round(Temp["total"].mean(), 2)


    colormap = branca.colormap.LinearColormap(
        # colors=["#f2f0f7", "#cbc9e2", "#9e9ac8", "#756bb1", "#54278f"],
        colors=["#b4ffe6", "#3fffbf", "#04ffab", "#00dc92", "#007a51"],
        index=Temp["total"].quantile([0.25, 0.5, 0.85, 0.95]),
        vmin=minimum,
        vmax=maximum,
    )
    colormap.caption = "Total medals"


    def style_function(x):
        return {
            "fillColor": colormap(x["properties"]["total"]),
            "color": "black",
            "weight": 2,
            "fillOpacity": 0.8,
        }

    m = folium.Map(location=[26.8206, 30.8025], zoom_start=2.2)

    Map_Layer = folium.GeoJson(
        Temp,
        name="Hosted",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["name","total","gold_medal","silver_medal","bronze_medal"], aliases=["name","Total","Gold","Silver", "Bronze"], localize=True
        ),
    ).add_to(m)

    return m

if __name__ == "__main__":
    visualize()
# %%
# To see the real output run this cell
# visualize()
# %%
import folium
import pandas as pd


def bubble_visualization(year="whole"):
    
    # Reading the data
    df, global_polygon = dataset.df_for_visualization()
    df = pd.DataFrame(df)
    global_polygon = pd.DataFrame(global_polygon)

    if year=="whole":
        temp = df[['gold_medal', 'silver_medal', 'bronze_medal', 'total', 'country_code']].groupby('country_code').agg(sum)
        temp = temp.reset_index(drop=False)
        temp['id'] = temp['country_code']
        temp = temp.merge(global_polygon, on='id', how='inner')
        df = gpd.GeoDataFrame(temp)

    elif(len(df[df.year==int(year)])==0):
        return "Olympics was not held at this year"
    
    else:
        df = gpd.GeoDataFrame(df[df.year==int(year)])

    # To get the center(approx) of each country
    ns = []
    ew = []
    for geo in global_polygon['geometry']:
        try:
            # For Polygon
            shellp = np.array(geo.exterior)
            ns.append((shellp[:,1:2].min()+shellp[:,1:2].max())/2)
            ew.append((shellp[:,:1].min()+shellp[:,:1].max())/2)
        except:
            # For MultiPolygon
            maxx=0
            ind = 0
            for i in geo:
                if maxx < len(np.array(i.exterior)):
                    maxx = len(np.array(i.exterior))
                    shellp = np.array(i.exterior)
            ns.append((shellp[:,1:2].min()+shellp[:,1:2].max())/2)
            ew.append((shellp[:,:1].min()+shellp[:,:1].max())/2)
            
    global_polygon['NS'] = ns
    global_polygon['EW'] = ew
    global_polygon = global_polygon[['id', 'NS', 'EW']]
    global_polygon

    # Merging main dataframe and global_polygon
    dtemp = df.merge(global_polygon, on='id', how='inner')

    # Normalizing the 'total' column
    dtemp['nor_total']=(dtemp['total']-dtemp['total'].mean())/dtemp['total'].std() +1
    dtemp.head()

    # Style function for the borders
    def style_function(x):
        return {
            "color": "black",
            "weight": 1,
            "opacity": 0.8
        }

    # Folium map instance
    m = folium.Map(location= [26.8206, 30.8025], zoom_start=2.2)
    Temp = gpd.GeoDataFrame(dtemp)

    # Creating Borders
    Map_Layer = folium.GeoJson(
        Temp,
        name="overall",
        style_function=style_function,

    ).add_to(m)

    # Creating bubbles for each country
    for index, row in dtemp.iterrows():
        folium.Circle(
            location=[row['NS'], row['EW']],
            fill=True,
            radius=row['nor_total']*170000,
            color='red',
            fill_color= 'Indigo',
            tooltip = "<div style='margin: 0; background-color: white; color: black;'>"+
                        "<h4 style='text-align:center;font-weight: bold'>"+row['name'] + "</h4>"
                        "<hr style='margin:10px;color: white;'>"+
                        "<ul style='color: black;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                            "<li>Total: "+str(row['total'])+"</li>"+
                            "<li>Gold:   "+str(row['gold_medal'])+"</li>"+
                            "<li>Silver: "+ str(row['silver_medal'])+ "</li>"+
                            "<li>Bronze: "+ str(row['bronze_medal'])+ "</li>"+
                        "</ul></div>",
            ).add_to(m)

    return m

bubble_visualization("2020")
# %%
