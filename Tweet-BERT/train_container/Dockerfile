FROM 763104351884.dkr.ecr.us-east-2.amazonaws.com/tensorflow-training:2.1.1-gpu-py36-cu101-ubuntu18.04


RUN pip install transformers==2.8.0


ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

ENV PATH="/opt/ml/code:${PATH}"

# Copy code
COPY tf_script_bert_tweet.py /opt/ml/code/


 
WORKDIR /opt/ml/code

ENV SAGEMAKER_PROGRAM tf_script_bert_tweet.py



