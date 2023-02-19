from pathlib import Path
from typing import List
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(retries=3)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def load(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame, color: str) -> None:
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("gcp-cred")

    df.to_gbq(
        destination_table=f"trips_data_all.trips_{color}",
        project_id="smiling-breaker-376117",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def el_gcs_to_bq(color: str, year: int, month: int) -> int:
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    df = load(path)
    write_bq(df, color)
    return len(df)


@flow(log_prints=True)
def el_parent_flow(color: str, year: int, months: List[int]) -> None:
    total_processed = 0
    for month in months:
        rows_processed = el_gcs_to_bq(color, year, month)
        print(f"Processed {rows_processed} rows for {color}/{year}/{month}")
        total_processed += rows_processed
    print(f"Total rows processed: {total_processed}")


if __name__ == "__main__":
    color = "yellow"
    year = 2020
    months = list(range(1, 13))
    el_parent_flow(color, year, months)
