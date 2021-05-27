import requests
import os
import json
import time
from difflib import SequenceMatcher
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

# headers for Twitter API from Twitter sample code 
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

# return tweet parameters for twitter api 
def get_params():
    return {"tweet.fields": "created_at,attachments"}

# defins rules for filtered stream
# from Twitter sample code  
def get_rules(headers, params):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers, params=params
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()

# delete rules for filtered stream
# from Twitter sample code  
def delete_all_rules(headers, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))

# set rules for filtered stream
# from Twitter sample code  
def set_rules(headers):
    # adjust the rules if needed
    sample_rules = [
        {"value": "from:44196397"}, # user_id of Elon's account: 44196397  ( user_id of test account @farzin03167666 : 1358539990670536705 )
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

# Twitter filtered stream
def get_stream(headers, params, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, params=params, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response["data"]
            tweet_content = tweet['text'].lower()
            split_tweet_content = tweet_content.split()

            with open ('public/json/cryptos.json') as crypto_json_file:
                        crypto_data = json.load(crypto_json_file) #get crypto_data from cryptos.json file
                        for crypto in crypto_data['cryptos']: #iterate through each cryto
                            for word in split_tweet_content: #iterate through each word in the tweet
                                if similar(word, crypto['symbol'].lower() ) > 0.75 or similar(word, crypto['name'].lower()) > 0.65 : #check if word is similar to crypto symbol or name
                                    crypto_message = "crypto found: " + crypto['name'] + " in Elon's tweet: " + tweet['text'] #generate crypto found message
                                    print(crypto_message)
                                   #send SMS with Twilio
                                    sms(crypto_message)
                                    print("\n")

            with open('public/json/stocks.json') as stocks_json_file:
                        stock_data = json.load(stocks_json_file) #get stock_data from stocks.json file
                        for stock in stock_data['popular_stocks']: #iterate through each stock
                            for word in split_tweet_content: #iterate through each word in the tweet
                                if similar(word, stock['name'].lower()) > 0.75: #check if word is similar to stock name
                                    stock_message = "stock found: " + stock['name'] + " in Elon's tweet: " + tweet['text'] #generate stock found message
                                    print(stock_message)
                                    #send SMS with Twilio
                                    sms(stock_message)
                                    print("\n")
             # check tweets for images
            try:
                if "attachments" in tweet: # if tweet potentially contains images
                    request_URL = "https://api.twitter.com/2/tweets?ids=" + tweet['id'] +"&expansions=attachments.media_keys&media.fields=duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width" #send request to get tweet by tweet ID
                    request_tweet = requests.get(request_URL, headers={"Authorization": "Bearer {}".format(bearer_token)})
                    for media in request_tweet.json()['includes']['media']: #iterate through media array of tweet
                        image_URL = media['url']
                        annotated_image = imageRecognition(image_URL) #get json responce from Google Vision AI
                        try:
                            with open ('public/json/cryptos.json') as crypto_json_file:
                                crypto_data = json.load(crypto_json_file) #get crypto_data from cryptos.json file
                                for crypto in crypto_data['cryptos']: #iterate through each cryto
                                    for objectDescription in annotated_image['responses'][0]['labelAnnotations']: #iterate through each annotation in the image
                                        if similar(objectDescription['description'], crypto['symbol'].lower() ) > 0.75 or similar(objectDescription['description'], crypto['name'].lower()) > 0.65 : #check if annotation is similar to crypto symbol or name
                                            crypto_message = "crypto found: " + crypto['name'] + " in Elon's tweet: " + image_URL #generate crypto found message
                                            print(crypto_message)
                                            #send SMS with Twilio
                                            sms(crypto_message)
                                            print("\n")
                            with open('public/json/stocks.json') as stocks_json_file:
                                stock_data = json.load(stocks_json_file) #get stock_data from stocks.json file
                                for stock in stock_data['popular_stocks']: #iterate through each stock
                                    for objectDescription in annotated_image['responses'][0]['labelAnnotations']: #iterate through each annotation in the image
                                        if similar(objectDescription['description'], stock['name'].lower()) > 0.75: #check if annotation is similar to stock name
                                            stock_message = "stock found: " + stock['name'] + " in Elon's tweet: " + image_URL #generate stock found message
                                            print(stock_message)
                                            #send SMS with Twilio
                                            sms(stock_message)
                                            print("\n")
                        except:
                            pass
                        try:
                            with open ('public/json/cryptos.json') as crypto_json_file:
                                crypto_data = json.load(crypto_json_file) #get crypto_data from cryptos.json file
                                for crypto in crypto_data['cryptos']: #iterate through each cryto
                                    for objectDescription in annotated_image['responses'][0]['logoAnnotations']: #iterate through each annotation in the image
                                        if similar(objectDescription['description'], crypto['symbol'].lower() ) > 0.75 or similar(objectDescription['description'], crypto['name'].lower()) > 0.65 : #check if annotation is similar to crypto symbol or name
                                            crypto_message = "crypto found: " + crypto['name'] + " in Elon's tweet: " + image_URL #generate crypto found message
                                            print(crypto_message)
                                            #send SMS with Twilio
                                            sms(crypto_message)
                                            print("\n")
                            with open('public/json/stocks.json') as stocks_json_file:
                                stock_data = json.load(stocks_json_file) #get stock_data from stocks.json file
                                for stock in stock_data['popular_stocks']: #iterate through each stock
                                    for objectDescription in annotated_image['responses'][0]['logoAnnotations']: #iterate through each annotation in the image
                                        if similar(objectDescription['description'], stock['name'].lower()) > 0.75: #check if annotation is similar to stock name
                                            stock_message = "stock found: " + stock['name'] + " in Elon's tweet: " + image_URL #generate stock found message
                                            print(stock_message)
                                            #send SMS with Twilio
                                            sms(stock_message)
                                            print("\n")                                     
                        except:
                            pass
                        try:
                            with open ('public/json/cryptos.json') as crypto_json_file:
                                crypto_data = json.load(crypto_json_file) #get crypto_data from cryptos.json file
                                for crypto in crypto_data['cryptos']: #iterate through each cryto
                                    for objectDescription in annotated_image['responses'][0]['textAnnotations']: #iterate through each annotation in the image
                                        if similar(objectDescription['description'], crypto['symbol'].lower() ) > 0.75 or similar(objectDescription['description'], crypto['name'].lower()) > 0.65 : #check if annotation is similar to crypto symbol or name
                                            crypto_message = "crypto found: " + crypto['name'] + " in Elon's tweet: " + image_URL #generate crypto found message
                                            print(crypto_message)
                                            #send SMS with Twilio
                                            sms(crypto_message)
                                            print("\n")
                            with open('public/json/stocks.json') as stocks_json_file:
                                stock_data = json.load(stocks_json_file) #get stock_data from stocks.json file
                                for stock in stock_data['popular_stocks']: #iterate through each stock
                                    for objectDescription in annotated_image['responses'][0]['textAnnotations']: #iterate through each annotation in the image
                                        if similar(objectDescription['description'], stock['name'].lower()) > 0.75: #check if annotation is similar to stock name
                                            stock_message = "stock found: " + stock['name'] + " in Elon's tweet: " + image_URL #generate stock found message
                                            print(stock_message)
                                            #send SMS with Twilio
                                            sms(stock_message)
                                            print("\n")                                                
                        except:
                            pass
            

            except:
                print("error")



# get Twilio SID
def sid(): 
    return os.getenv("TWILIO_ACCOUNT_SID")

# get Twilio auth token
def twilio_auth():
    return os.getenv("TWILIO_AUTH_TOKEN")

# use SequenceMatcher to return similarity of two strings 
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# send sms with twilio client
def sms(message):
    account_sid = sid()
    auth_token = twilio_auth()
    client = Client(account_sid, auth_token)
    phone_number = os.getenv("PHONE_NUMBER")
    twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
    client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=phone_number
    )
    
# get Google VisionAI API key 
def vison_ai_api_key():
    return os.getenv("VISIONAI_API_KEY")

# use Google Vision AI to annotate image and return annotations json responce 
def imageRecognition(url):
    visionAI_request_body = {
        "requests": [
        {
            "image": {
                "source": {
                "imageUri": ""
                }
            },
            "features": [
            {
                "type": "LABEL_DETECTION",
                "maxResults": 5
            },
            {
                "type": "LOGO_DETECTION",
                "maxResults": 5
            },
            {
                "type": "TEXT_DETECTION",
                "maxResults": 5
            }
            ]
        }
    ]
    }
    visionAI_request_body["requests"][0]["image"]["source"]["imageUri"] = url
    visionAI_request_json = json.dumps(visionAI_request_body)
    visionAI_api_key = vison_ai_api_key()
    response = requests.post('https://vision.googleapis.com/v1/images:annotate?key=' + visionAI_api_key, data= visionAI_request_json)
    return response.json()

def main():
    bearer_token = os.getenv("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    params = get_params()
    rules = get_rules(headers, params)
    delete = delete_all_rules(headers, rules)
    set = set_rules(headers)
    while True:
        try:
            get_stream(headers, params, bearer_token)
        except:
            print("something went wrong")
            time.sleep(60)


if __name__ == "__main__":
    main()
