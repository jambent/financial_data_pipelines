##############################################################################
# s3 buckets                                                                 #
##############################################################################

resource "aws_s3_bucket" "code_bucket" {
  bucket_prefix = "yfinance-ingestion-code-"
  force_destroy = true
}

resource "aws_s3_bucket" "landing_bucket" {
  bucket_prefix = "landing-bucket-"
  force_destroy = true
}

##############################################################################
# Lambda code                                                             #
##############################################################################
resource "aws_s3_object" "yfinance_fx_ingestion_code" {
  key    = "yfinance_fx_ingestion_function.zip"
  source = "${path.module}/../lambda_code_zip_files/yfinance_fx_ingestion_function.zip"
  bucket = aws_s3_bucket.code_bucket.id
}



##############################################################################
# Lambda layers                                                              #
##############################################################################

resource "aws_lambda_layer_version" "yfinance_layer" {
  filename   = "${path.module}/../aws_lambda_layers/yfinance_layer.zip"
  layer_name = "yfinance_layer"

  compatible_runtimes = ["python3.11"]
}
