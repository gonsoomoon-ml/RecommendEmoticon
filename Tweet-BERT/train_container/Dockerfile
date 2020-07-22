# 기존의  Pre-built-in TF2.1-gpu image를 가져옴
FROM 763104351884.dkr.ecr.us-west-2.amazonaws.com/tensorflow-training:2.1.1-gpu-py36-cu101-ubuntu18.04

# transformers 설치
RUN pip install transformers==2.8.0


ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

ENV PATH="/opt/ml/code:${PATH}"

# Copy training code
COPY tf_script_bert_tweet.py /opt/ml/code/
 
WORKDIR /opt/ml/code

ENV SAGEMAKER_PROGRAM tf_script_bert_tweet.py



