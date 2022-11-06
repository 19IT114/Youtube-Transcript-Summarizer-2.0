
# Imports the Google Cloud client library
from google.cloud import speech
from download import makeTextFile
from model import text_summarizer

# def speechtotext():
#     # Instantiates a client
#     # authenticates on the basis of a key.
#     client = speech.SpeechClient.from_service_account_json('key.json')

#     # The name of the audio file to transcribe
#     # Need to change the gcs uri as per the name of the file
#     gcs_uri = "gs://yts_audio/yts-audio-file"

#     audio = speech.RecognitionAudio(uri=gcs_uri)

#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
#         sample_rate_hertz=16000,
#         language_code="en-US",
#     )

#     # Detects speech in the audio file
#     response = client.recognize(config=config, audio=audio)
#     transcript=''
#     for result in response.results:
#         transcript = transcript+(result.alternatives[0].transcript)

#     print(transcript)

# message TranscriptOutputConfig {

#     oneof output_type {
     
#       string gcs_uri = 1;
#     }
#   }


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=1000)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcript = ''
    for result in response.results:
        transcript = transcript+text_summarizer(result.alternatives[0].transcript)
    return transcript
    

# transcribe_gcs("gs://yts_audio/yts-audio-file")