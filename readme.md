# DogeCEO

## About
This is a program that checks for new tweets from a Twitter user (Elon Musk by default) and checks if the tweets contain the name of popular stocks or cryptocurrencies. The program checks for tweets every 2 minutes. If the tweet contains text, it will scan the text for potential names of companies with commonly traded stocks or popular cryptocurrencies. If the tweet contains an image or multiple images, the program will use ImageAI to locate images of Dogecoin or images of dogs. If the program finds images of dogecoin or text containing stocks or cryptocurrencies, it will send an SMS to the configured phone number using the Twilio API.

## Installation

### Requiremmts
1. Python 3.8
2. Twitter developer account
3. Twilio account (trial account is fine)

### Instructions
1. Clone repository
2. <code>cd DogeCEO</code>
3. <code>pip install -r requirements.txt</code>
4. Download yolo.h5 from [ImageAI documentation](https://imageai.readthedocs.io/en/latest/detection/) to the DogeCEO folder
5. Create a .env file add Twitter API consumer key, consumer secret key, and bearer token as shown in .env.example
6. Add the Twilio account sid and Twilio auth token to .env file as shown in the .env.example file
7. Add the your phone number with +1 (ex: '+1800XXXXXXX') and your Twilio phone number in the same format as shown in .env.example
7. <code>python3 TweetBot.py</code>

## Examples
### Image Recognition
<img src="public/img/doge-image.jpeg" width="600">

### Find stock in tweet
<img src="public/img/gamestop.png" width="600">

### Find crypto in tweet
<img src="public/img/dogecoin.png" width="600">

### Send alerts 
<img src="public/img/twilio-texts.PNG" width="600">

## What's Next
1. Getting text from tweeted images to check for names of stocks or cryptocurrencies
2. Detecting images of cryptocurrency symbols in tweeted images
