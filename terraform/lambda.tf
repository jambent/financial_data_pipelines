resource "aws_lambda_function" "yfinance_dataframe_to_parquet" {
  function_name = var.lambda_df_to_parquet_name
  role          = aws_iam_role.lambda_df_to_parquet_role.arn
  s3_bucket     = aws_s3_bucket.code_bucket.id
  s3_key        = aws_s3_object.yfinance_ingestion_code.key
  handler       = "prototype_data_ingestion.lambda_handler"
  runtime       = "python3.11"
  timeout       = 600
  environment {
    variables = {
      "S3_LANDING_ID"          = aws_s3_bucket.landing_bucket.id,
      "S3_LANDING_ARN"         = aws_s3_bucket.landing_bucket.arn
    }
  }
  layers = [
            "arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python311:4",
            aws_lambda_layer_version.yfinance_layer.arn
        ]

}