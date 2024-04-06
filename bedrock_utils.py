import json
import boto3

def invoke_claude_3_multimodal(client, prompt, base64_image_data):
    """
    Invokes Anthropic Claude 3 Sonnet to run a multimodal inference using the input
    provided in the request body.

    :param prompt:            The prompt that you want Claude 3 to use.
    :param base64_image_data: The base64-encoded image that you want to add to the request.
    :return: Inference response from the model.
    """


    # Invoke the model with the prompt and the encoded image
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_image_data,
                        },
                    },
                ],
            }
        ],
    }

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body),
        )

        # Process and print the response
        result = json.loads(response.get("body").read())
      

        return result
    except Exception as err:
        print(
            "Couldn't invoke Claude 3 Sonnet. Here's why: ", err
        )


