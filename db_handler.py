import configparser
import geopandas as gpd
import psycopg2
from sqlalchemy import create_engine

def get_db_connection():
    config = configparser.ConfigParser()
    config.read("configfile.ini")
    db = config["postgresql"]
    engine = create_engine(
        f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"
    )
    return engine

def get_region_list():
    engine = get_db_connection()
    query = "SELECT DISTINCT region_name FROM your_table ORDER BY region_name;"
    df = gpd.read_postgis(query, engine)
    return df["region_name"].tolist()

def get_geodata_for_regions(regions):
    engine = get_db_connection()
    region_list = "', '".join(regions)
    query = f"""
        SELECT * FROM your_table
        WHERE region_name IN ('{region_list}');
    """
    gdf = gpd.read_postgis(query, engine, geom_col='geom')  # replace 'geom' if your column is named differently
    return gdf

def get_geodata_group(region_code):
    engine = get_db_connection()
    tables = ['d', 'c', 'e']
    gdfs = {}
    for t in tables:
        query = f"SELECT * FROM {t} WHERE cc = %s;"
        gdf = gpd.read_postgis(query, engine, geom_col='geom', params=(region_code,))
        gdfs[t] = gdf
    return gdfs  # dictionary of 3 GeoDataFrames

def get_basemap_for_region(region_code):
    engine = get_db_connection()
    query = "SELECT * FROM country_polygons WHERE cc = %s"
    gdf = gpd.read_postgis(query, engine, geom_col='geom', params=(region_code,))
    return gdf