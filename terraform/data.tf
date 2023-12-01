data "archive_file" "df_to_parquet_lambda" {
  type        = "zip"
  source_dir = "${path.module}/../src"
  output_path = "${path.module}/../yfinance_ingestion_function.zip"
}