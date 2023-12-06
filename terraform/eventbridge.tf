resource "aws_cloudwatch_event_rule" "yfinance_fx_ingestion_lambda_invocation_rule" {
  name                = "yfinance-fx-ingestion-lambda-invocation-event-rule"
  description         = "triggers yfinance fx ingestion lambda according to specified schedule"
  schedule_expression = "cron(50 16 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "yfinance_fx_ingestion_lambda_target" {
  arn  = aws_lambda_function.yfinance_fx_dataframe_to_parquet.arn
  rule = aws_cloudwatch_event_rule.yfinance_fx_ingestion_lambda_invocation_rule.name
}