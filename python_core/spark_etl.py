"""Batch cleaning and Parquet preparation.

Uses explicit Spark schemas when PySpark is installed. A small stdlib CSV fallback
is provided so the demo can still validate its cleaning rules without Spark.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "python_core" / "parquet"


def clean_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = csv.DictReader(handle)
        cleaned: list[dict[str, Any]] = []
        for row in rows:
            item = {key.strip(): value.strip() if isinstance(value, str) else value for key, value in row.items() if key and not key.startswith("Unnamed")}
            if "crop" in item:
                item["crop"] = item["crop"].lower()
            cleaned.append(item)
        return cleaned


def run_fallback() -> dict[str, int]:
    OUT.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for source, target in [("Dataset_sensors.csv", "sensors.json"), ("crop_yield.csv", "yield.json"), ("agriculture_dataset.csv", "farms.json")]:
        rows = clean_csv(DATA / source)
        (OUT / target).write_text(json.dumps(rows), encoding="utf-8")
        counts[source] = len(rows)
    return counts


def run_spark() -> None:
    from pyspark.sql import SparkSession, functions as F, types as T
    spark = SparkSession.builder.appName("crop-bodyguard-etl").getOrCreate()
    sensor_schema = T.StructType([T.StructField("weather_temperature", T.DoubleType()), T.StructField("weather_humidity", T.DoubleType()), T.StructField("solar_radiation", T.DoubleType()), T.StructField("soil_moisture", T.DoubleType()), T.StructField("soil_temperature", T.DoubleType()), T.StructField("Unnamed_5", T.StringType())])
    sensors = spark.read.schema(sensor_schema).option("header", True).csv(str(DATA / "Dataset_sensors.csv")).drop("Unnamed_5").dropDuplicates()
    sensors.write.mode("overwrite").parquet(str(OUT / "sensors"))
    yield_df = spark.read.option("header", True).option("inferSchema", False).csv(str(DATA / "crop_yield.csv"))
    for column in yield_df.columns:
        yield_df = yield_df.withColumnRenamed(column, column.strip())
    yield_df = yield_df.withColumn("crop", F.lower(F.trim("crop"))).withColumn("state", F.trim("state"))
    yield_df.write.mode("overwrite").partitionBy("state").parquet(str(OUT / "yield"))
    spark.stop()


if __name__ == "__main__":
    try:
        import pyspark  # noqa: F401
    except ImportError:
        print(json.dumps(run_fallback(), indent=2))
    else:
        run_spark()
