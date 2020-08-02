# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.


import json
import tensorflow as tf
import requests

from transformers import DistilBertTokenizer

tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
max_seq_length = 32

def input_handler(data, context):
    """ Pre-process request input before it is sent to TensorFlow Serving REST API
    Args:
        data (obj): the request data, in format of dict or string
        context (Context): an object containing request and configuration details
    Returns:
        (dict): a JSON-serializable dict that contains request body and headers
    """

    if context.request_content_type == 'application/json':
        
        instances = data.read().decode('utf-8')
        # Convert request stream to String
        instances = json.loads(instances)
        print("instances: \n", instances)
        
        transformed_instances = []

        for instance in instances:
            print("instance: ", instance)
            encode_plus_tokens = tokenizer.encode_plus(instance,
                                                       pad_to_max_length=True,
                                                       max_length= max_seq_length)

            input_ids = encode_plus_tokens['input_ids']
            input_mask = encode_plus_tokens['attention_mask']
            segment_ids = [0] * max_seq_length

            transformed_instance = {"input_ids": input_ids, 
                                    "input_mask": input_mask, 
                                    "segment_ids": segment_ids}
            
            print("transformed_instance: \n", transformed_instance)

            transformed_instances.append(transformed_instance)


        transformed_data = {"instances": transformed_instances}
        
        print("transformed_data: \n", transformed_data)

        return json.dumps(transformed_data)

    else:
        _return_error(415, 'Unsupported content type "{}"'.format(
            context.request_content_type or 'Unknown'))


        
def output_handler(data, context):
    """Post-process TensorFlow Serving output before it is returned to the client.
    Args:
        data (obj): the TensorFlow serving response
        context (Context): an object containing request and configuration details
    Returns:
        (bytes, string): data to return to client, response content type
    """
    if data.status_code != 200:
        raise Exception(data.content.decode('utf-8'))
        
    response_content_type = context.accept_header
    prediction = data.content
    log_probabilities = json.loads(prediction)['predictions']
    print("###############################")
    print("log_probabilities: \n", log_probabilities)
    print("###############################")    


    
    return json.dumps(log_probabilities), response_content_type    


def _return_error(code, message):
    raise ValueError('Error: {}, {}'.format(str(code), message))



