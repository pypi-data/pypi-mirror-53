# Local Lambda Kinesis Runner [![Build Status](https://travis-ci.org/kobybum/local-lambda-kinesis.svg?branch=master)](https://travis-ci.org/kobybum/local-lambda-kinesis)

A python utility for testing lambda kinesis handlers locally using real data.

## Use Case

You want to test your lambda handler locally on real data before deploying it.
This utility reads from a kinesis stream, transforms the events and forwards them to your handler.

## Alternatives

At the time of writing, [AWS SAM](https://github.com/awslabs/serverless-application-model) supports running kinesis handlers locally on a custom event.

## Usage
`pip install local_lambda_kinesis`
`lambda_kinesis -s <stream_name> -p <handler path>`

### Optional arguments:
- `-i <iterator type>` - Set the [shard iterator type](https://stackoverflow.com/questions/49728807/trim-horizon-vs-latest), suppors `LATEST` and `TRIM_HORIZON`.
- `--shard-iterator` - By default the handler runs on the first available shard in the stream. you can use a specific one.

### Environment Variables:
The tool uses the default AWS CLI settings. To override them, set `AWS_PROFILE` and `AWS_DEFAULT_REGION`.
