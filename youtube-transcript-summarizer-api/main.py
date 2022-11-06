"""
Project Name: YouTube Transcript Summarizer
YouTube Transcript Summarizer API
"""


from flask import Flask, request, jsonify
from flask_cors import CORS

from model import nlp_model, text_model
from downloadvideo import Video_link
from convertToAudio import convert2audio
from uploadtobucket import upload_blob
from speechtotext import transcribe_gcs

app = Flask(__name__)
CORS(app)


@app.route('/api/', methods=['GET'])
def respond():

    # Retrieve the video_id from url parameter
    # vid_url = request.args.get("video_url", None)
    vid_url =  request.args.get("video_url", None)
    if "youtube.com" in vid_url:

        try:
            video_id = vid_url.split("=")[1]

            try:
                video_id = video_id.split("&")[0]

            except:
                video_id = "False"

        except:
            video_id = "False"

    elif "youtu.be" in vid_url:

        try:
            video_id = vid_url.split("/")[3]

        except:

            video_id = "False"

    else:
        video_id = "False"

    # For debugging
    # print(f"got name {video_id}")

    body = {}
    data = {}

    # Check if user doesn't provided  at all
    if not video_id:
        data['message'] = "Failed"
        data['error'] = "no video id found, please provide valid video id."

    # Check if the user entered a invalid instead video_id
    elif str(video_id) == "False":
        data['message'] = "Failed"
        data['error'] = "video id invalid, please provide valid video id."

    # Now the user has given a valid video id
    else:

        if nlp_model(video_id) == "0":
            Video_link(vid_url)
            convert2audio()
            upload_blob('yts_audio','video.mp3','yts-audio-file')
            text = transcribe_gcs("gs://yts_audio/yts-audio-file")
            data['original_txt_length'], data['final_summ_length'], data['eng_summary'], data['hind_summary'], data['guj_summary'] = text_model(
                text)
            # Upload the downloaded file in bucket 
            # call the speech to text method 
            # Pass the text to model in order to sumarize the text
            # Get the sumarized text prepare the body

            data['message'] = "Success"
            data['id'] = video_id

        else:
            data['message'] = "Success"
            data['id'] = video_id
            data['original_txt_length'], data['final_summ_length'], data['eng_summary'], data['hind_summary'], data['guj_summary'] = nlp_model(
                video_id)

    body["data"] = data

    # Return the response in json format
    return buildResponse(body)


# Welcome message to our server
@app.route('/hell')
def index():

    body = {}
    body['message'] = "Success"
    body['data'] = "Welcome to YTS API."

    return buildResponse(body)


def buildResponse(body):

    # from flask import json, Response
    # res = Response(response=json.dumps(body), status=statusCode, mimetype="application/json")
    # res.headers["Content-Type"] = "application/json; charset=utf-8"
    # return res

    response = jsonify(body)
    # response.headers.add('Access-Control-Allow-Origin', '*')

    return response


if __name__ == '__main__':

    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)

# Deployment to Heroku Cloud.
