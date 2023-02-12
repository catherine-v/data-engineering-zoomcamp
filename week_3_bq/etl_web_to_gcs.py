import os
from pathlib import Path
from typing import List
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def fetch(year: int, month: int) -> Path:
    """Save a removev file locally"""
    dataset_file = f"fhv_tripdata_{year}-{month:02}.csv.gz"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/{dataset_file}"
    dataset_download_path = Path(f"data/fhv/{dataset_file}")
    dataset_download_path.parent.mkdir(parents=True, exist_ok=True)
    os.system(f"wget {dataset_url} -O {dataset_download_path}")
    return dataset_download_path


@task()
def write_gcs(path: Path) -> None:
    """Upload local file to GCS"""
    gcs_block = GcsBucket.load("gcs-bucket")
    gcs_block.upload_from_path(from_path=path, to_path=path, timeout=30 * 60)
    return


@flow()
def etl_web_to_gcs(year: int, month: int) -> None:
    """The main ETL function"""
    path = fetch(year, month)
    write_gcs(path)


@flow()
def etl_parent_flow(year: int, months: List[int]) -> None:
    for month in months:
        etl_web_to_gcs(year, month)


if __name__ == "__main__":
    year = 2019
    months = [i for i in range(1, 13)]
    etl_parent_flow(year, months)
