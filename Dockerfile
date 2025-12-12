FROM public.ecr.aws/lambda/python:3.12-arm64

RUN pip install langchain-aws langchain-core pydantic boto3

COPY app/llm_handler.py ${LAMBDA_TASK_ROOT}/
COPY app/utils/ ${LAMBDA_TASK_ROOT}/utils/

# filename.function_name
CMD [ "llm_handler.lambda_handler" ]
