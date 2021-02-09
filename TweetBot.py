import requests
import json
from dotenv import load_dotenv
load_dotenv()
import os
import time
from datetime import datetime
from twilio.rest import Client
import urllib.request
from imageai.Detection import ObjectDetection
from difflib import SequenceMatcher


def sid():
    return os.getenv("TWILIO_ACCOUNT_SID")

def twilioAuth():
    return os.getenv("TWILIO_AUTH_TOKEN")

def auth():
    return os.getenv("BEARER_TOKEN")

def create_url():
    user_id = 44196397 # elon: 44196397 # test account: 1358539990670536705
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,attachments"}

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():
    lastDate = datetime.strptime('2021-01-01 20:05:25.000', '%Y-%m-%d %H:%M:%S.%f')

    #twilio setup
    numbers_to_message = ['+000000000'] #enter numbers here
    account_sid = sid()
    auth_token = twilioAuth()
    client = Client(account_sid, auth_token)


    #twitter setup
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    params = get_params()

    #ImageAi setup
    current_directory = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(current_directory, "yolo.h5"))
    detector.loadModel()

    while True:
        json_response = connect_to_endpoint(url, headers, params)
        #print(json.dumps(json_response, indent=4, sort_keys=True))
        tweets = json_response['data']
        #print(tweets)
        print("Search: ")
        for tweet in tweets:
            tweetDate = datetime.strptime(tweet['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
            if tweetDate > lastDate:
                tweetContent = tweet['text'].lower()
                splitTweetContent = tweetContent.split()


                with open ('cryptos.json') as cryptoJsonFile:
                    cryptoData = json.load(cryptoJsonFile)
                    for crypto in cryptoData['cryptos']:
                        for word in splitTweetContent:
                            if similar(word, crypto['symbol'].lower() ) > 0.75 or similar(word, crypto['name'].lower()) > 0.65 :
                                cryptoMessage = "crypto found: " + crypto['name'] + " in Elon's tweet: " + tweet['text']
                                print(cryptoMessage)
                                '''

                                for number in numbers_to_message:
                                    client.messages.create(
                                        body=cryptoMessage,
                                        from_='+00000000',
                                        to=number
                                    )
                                    '''

                                print("\n")

                with open('stocks.json') as stocksJsonFile:
                    stockData = json.load(stocksJsonFile)
                    for stock in stockData['popular_stocks']:
                        for word in splitTweetContent:
                            if (similar(word, stock['name'].lower() ) > 0.75 ): #or similar(word, stock['tinker'].lower() ) > 0.9
                                stockMessage = "stock found: " + stock['name'] + " in Elon's tweet: " + tweet['text']
                                print(stockMessage)
                                '''
                                for number in numbers_to_message:
                                    client.messages.create(
                                        body=stockMessage,
                                        from_='+00000000',
                                        to=number
                                    )
                                print("\n")
                                '''

                try:
                    if "attachments" in tweet:
                        requestURL = "https://api.twitter.com/2/tweets?ids=" + tweet['id'] +"&expansions=attachments.media_keys&media.fields=duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width"
                        requestTweet = requests.get(requestURL, headers={"Authorization": "Bearer {}".format(bearer_token)})
                        for media in requestTweet.json()['includes']['media']:
                            imageURL = media['url']
                            urllib.request.urlretrieve(imageURL,"tweeted-image.jpg")
                            time.sleep(5)
                            detections = detector.detectObjectsFromImage(
                                input_image=os.path.join(current_directory, "tweeted-image.jpg"),
                                output_image_path=os.path.join(current_directory, "labeled-tweeted-image.jpg"))
                            for eachObject in detections:
                                if eachObject["name"] == "dog":
                                    dogeMessage = "found dog in image: " + imageURL
                                    print(dogeMessage)
                                    '''

                                    for number in numbers_to_message:
                                        client.messages.create(
                                            body=dogeMessage,
                                            from_='+000000000',
                                            to=number
                                        )
                                        '''
                except:
                    print("error")

        lastDate = datetime.strptime(tweets[0]['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
        print("Waiting 2 minutes")
        time.sleep(60)
        print("Waiting 60 seconds")
        time.sleep(60)





if __name__ == "__main__":
    main()