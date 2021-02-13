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


# ger twilio account sid
def sid(): 
    return os.getenv("TWILIO_ACCOUNT_SID")

#get twilio auth token
def twilioAuth():
    return os.getenv("TWILIO_AUTH_TOKEN")

#get twitter bearer token
def auth():
    return os.getenv("BEARER_TOKEN")

# funtion that returns witter timeline url 
def create_url():
    user_id = 1358539990670536705 # elon: 44196397 # test account: 1358539990670536705
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

#returns tweet parameters for twitter api 
def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,attachments"}

#authenticate bearer token 
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# connect to twitter api and return json
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

# function that return similarity index of 2 strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def main():
    lastDate = datetime.strptime('2021-01-01 20:05:25.000', '%Y-%m-%d %H:%M:%S.%f')

    #twilio setup
    account_sid = sid()
    auth_token = twilioAuth()
    client = Client(account_sid, auth_token)
    phone_number = os.getenv("PHONE_NUMBER")
    twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")


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

    time.sleep(5)

    #constant loop that runs every 2 minutes
    while True:
        json_response = connect_to_endpoint(url, headers, params) #get latest tweets
        #print(json.dumps(json_response, indent=4, sort_keys=True))
        tweets = json_response['data']
        #print(tweets)
        print("Search: ")
        for tweet in tweets:
            tweetDate = datetime.strptime(tweet['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f') #get the time the tweet was posted
            if tweetDate > lastDate: # check if tweet has already been analyzed based on time of last tweet analyzed
                tweetContent = tweet['text'].lower() #format all letters to lowercase 
                splitTweetContent = tweetContent.split() #split tweet into words 


                with open ('cryptos.json') as cryptoJsonFile: 
                    cryptoData = json.load(cryptoJsonFile) #get cryptodata from cryptos.json file
                    for crypto in cryptoData['cryptos']: #iterate through each cryto 
                        for word in splitTweetContent: #iterate through each word in the tweet
                            if similar(word, crypto['symbol'].lower() ) > 0.75 or similar(word, crypto['name'].lower()) > 0.65 : #check if word is similar to crypto symbol or name
                                cryptoMessage = "crypto found: " + crypto['name'] + " in Elon's tweet: " + tweet['text'] #generate crypto found message
                                print(cryptoMessage)
                               #send SMS with Twilio
                                client.messages.create(
                                    body=cryptoMessage,
                                    from_=twilio_phone_number,
                                    to=phone_number
                                )
                                print("\n")

                with open('stocks.json') as stocksJsonFile:
                    stockData = json.load(stocksJsonFile) #get stockData from stocks.json file
                    for stock in stockData['popular_stocks']: #iterate through each stock
                        for word in splitTweetContent: #iterate through each word in the tweet
                            if similar(word, stock['name'].lower()) > 0.75: #check if word is similar to stock name
                                stockMessage = "stock found: " + stock['name'] + " in Elon's tweet: " + tweet['text'] #generate stock found message
                                print(stockMessage)
                                #send SMS with Twilio
                                client.messages.create(
                                    body=cryptoMessage,
                                    from_=twilio_phone_number,
                                    to=phone_number
                                )
                                print("\n")
                               
                # check tweets for images
                try:
                    if "attachments" in tweet: # if tweet potentially contains images
                        requestURL = "https://api.twitter.com/2/tweets?ids=" + tweet['id'] +"&expansions=attachments.media_keys&media.fields=duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width" #send request to get tweet by tweet ID
                        requestTweet = requests.get(requestURL, headers={"Authorization": "Bearer {}".format(bearer_token)})
                        for media in requestTweet.json()['includes']['media']: #iterate through media array of tweet
                            imageURL = media['url']
                            urllib.request.urlretrieve(imageURL,"tweeted-image.jpg") #retrieve and download image from media
                            time.sleep(5)
                            #use imageAI to detect objects in image
                            detections = detector.detectObjectsFromImage(
                                input_image=os.path.join(current_directory, "tweeted-image.jpg"),
                                output_image_path=os.path.join(current_directory, "labeled-tweeted-image.jpg"))
                            for eachObject in detections: #iterate through each object in image
                                if eachObject["name"] == "dog": #check if object is dog
                                    dogeMessage = "found dog in image: " + imageURL
                                    print(dogeMessage)
                                    #send SMS with Twilio
                                    client.messages.create(
                                    body=cryptoMessage,
                                    from_=twilio_phone_number,
                                    to=phone_number
                                    )
                except:
                    print("error")

        lastDate = datetime.strptime(tweets[0]['created_at'][:-1], '%Y-%m-%dT%H:%M:%S.%f')
        print("Waiting 2 minutes")
        time.sleep(60)
        print("Waiting 60 seconds")
        time.sleep(60)





if __name__ == "__main__":
    main()