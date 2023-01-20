#!/usr/bin/env python
# coding: utf-8
import argparse
import os
from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    print("Downloading the file...")
    if url.endswith(".csv.gz"):
        csv_name = "output.csv.gz"
    else:
        csv_name = "output.csv"

    os.system(f"wget {url} -O {csv_name}")

    print("Connecting to the DB...")
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    engine.connect()

    print("Creating the table...")
    df = pd.read_csv(
        csv_name,
        parse_dates=params.date_columns,
        nrows=100,
    )
    df.head(n=0).to_sql(table_name, con=engine, if_exists="replace")

    print("Uploading data...")
    df_iter = pd.read_csv(
        csv_name,
        parse_dates=params.date_columns,
        iterator=True,
        chunksize=100_000,
    )
    for i, df in enumerate(df_iter, start=1):
        start = time()
        df.to_sql(table_name, con=engine, if_exists="append")
        end = time()
        print(
            "...uploaded chunk %d of %d records. It took %.3f seconds"
            % (i, len(df), end - start)
        )
    print("Finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="database name for postgres")
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    parser.add_argument("--url", required=True, help="url of the csv file")
    parser.add_argument("--date-column", nargs="+", default=[], dest="date_columns")

    args = parser.parse_args()

    main(args)
