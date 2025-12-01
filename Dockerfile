# 1. Use the AWS Lambda Python 3.12 image (ARM64 for Mac speed)
FROM public.ecr.aws/lambda/python:3.12-arm64

# 2. Install the libraries
# We run this directly in the container so it's perfectly compatible
RUN pip install langchain-aws langchain-core pydantic boto3

# 3. Copy specific code folders
COPY lambda/llm_handler.py ${LAMBDA_TASK_ROOT}/
COPY lambda/utils/ ${LAMBDA_TASK_ROOT}/utils/

# 4. Tell the container what function to run
# filename.function_name
CMD [ "llm_handler.lambda_handler" ]
