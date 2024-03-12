from dagster import asset
from dagster_duckdb import DuckDBResource
from ..partitions import weekly_partition
import plotly.express as px
import plotly.io as pio
import geopandas as gpd
import os
from . import constants
from datetime import datetime, timedelta
import pandas as pd


@asset(
    deps=["taxi_trips", "taxi_zones"]
)
def manhattan_stats(database: DuckDBResource):
    """
    selects trips in manhattan and creates a json file with geo data
    """
    query = """
        select
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips,
        from trips
        left join zones on trips.pickup_zone_id = zones.zone_id
        where borough = 'Manhattan' and geometry is not null
        group by zone, borough, geometry
    """
    with database.get_connection() as conn:
      trips_by_zone = conn.execute(query).fetch_df()

    trips_by_zone["geometry"] = gpd.GeoSeries.from_wkt(trips_by_zone["geometry"])
    trips_by_zone = gpd.GeoDataFrame(trips_by_zone)

    with open(constants.MANHATTAN_STATS_FILE_PATH, 'w') as output_file:
        output_file.write(trips_by_zone.to_json())

@asset(
    deps=["manhattan_stats"]
)
def manhattan_map():
    """
    creates a map of trips in Manhattan using upstream manhattan_stats
    """
    trips_by_zone = gpd.read_file(constants.MANHATTAN_STATS_FILE_PATH)

    fig = px.choropleth_mapbox(trips_by_zone,
        geojson=trips_by_zone.geometry.__geo_interface__,
        locations=trips_by_zone.index,
        color='num_trips',
        color_continuous_scale='Plasma',
        mapbox_style='carto-positron',
        center={'lat': 40.758, 'lon': -73.985},
        zoom=11,
        opacity=0.7,
        labels={'num_trips': 'Number of Trips'}
    )

    pio.write_image(fig, constants.MANHATTAN_MAP_FILE_PATH)

    # @asset(
    #     deps=["taxi_trips"]
    # )
    # def trips_by_week():
        
    #     query = """
    #         select
    #             (date_trunc('week', pickup_datetime) - INTERVAL '1 day') AS period,
    #             count(1) as num_trips,
    #             ROUND(SUM(passenger_count),2) as passenger_count,
    #             ROUND(SUM(total_amount),2) as total_amount,
    #             ROUND(SUM(trip_distance),2) as trip_distance,
    #         from trips 
    #         where period > '2023-01-01'
    #         group by period
    #         order by period;
    #     """

    #     conn = duckdb.connect(os.getenv("DUCKDB_DATABASE"))
    #     trips_by_week = conn.execute(query).fetch_df()

    #     with open(constants.TRIPS_BY_WEEK_FILE_PATH, 'w') as output_file:
    #         output_file.write(trips_by_week.to_csv())

@asset(
    deps=["taxi_trips"],
    partitions_def=weekly_partition,
)
def trips_by_week(context, database: DuckDBResource):
    """
      The number of trips per week, aggregated by week.
    """

    period_to_fetch = context.asset_partition_key_for_output()

    # get all trips for the week
    query = f"""
        select vendor_id, total_amount, trip_distance, passenger_count
        from trips
        where pickup_datetime >= '{period_to_fetch}'
            and pickup_datetime < '{period_to_fetch}'::date + interval '1 week'
    """

    with database.get_connection() as conn:
        data_for_month = conn.execute(query).fetch_df()

    aggregate = data_for_month.agg({
        "vendor_id": "count",
        "total_amount": "sum",
        "trip_distance": "sum",
        "passenger_count": "sum"
    }).rename({"vendor_id": "num_trips"}).to_frame().T # type: ignore

    # clean up the formatting of the dataframe
    aggregate["period"] = period_to_fetch
    aggregate['num_trips'] = aggregate['num_trips'].astype(int)
    aggregate['passenger_count'] = aggregate['passenger_count'].astype(int)
    aggregate['total_amount'] = aggregate['total_amount'].round(2).astype(float)
    aggregate['trip_distance'] = aggregate['trip_distance'].round(2).astype(float)
    aggregate = aggregate[["period", "num_trips", "total_amount", "trip_distance", "passenger_count"]]

    try:
        # If the file already exists, append to it, but replace the existing month's data
        existing = pd.read_csv(constants.TRIPS_BY_WEEK_FILE_PATH)
        existing = existing[existing["period"] != period_to_fetch]
        existing = pd.concat([existing, aggregate]).sort_values(by="period")
        existing.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)
    except FileNotFoundError:
        aggregate.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)

