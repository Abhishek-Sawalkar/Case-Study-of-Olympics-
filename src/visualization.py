
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
