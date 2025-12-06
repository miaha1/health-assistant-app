# Convert AI to speech using AWS Polly

import boto3
import uuid

polly = boto3.client('polly')
s3 = boto3.client('s3')

def generate_audio_response(text,bucket):
    """ Convert text to speech and upload to S3 
        Returns S3 key of the audio file"""
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )

    # # Generate unique key
    output_key = f"outputs/response-{uuid.uuid4()}.mp3"

    # Upload to S3
    s3.put_object(Bucket=bucket, 
                  Key=output_key,
                  Body=response['AudioStream'].read(),
                  ContentType='audio/mpeg')

    return output_key