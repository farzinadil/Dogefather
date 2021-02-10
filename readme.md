# DogeCEO

## About
This is a program that checks for new tweets from a Twitter user (Elon Musk by default) and checks if the tweets contain the name of popular stocks or cryptocurrencies. The program checks for tweets every 2 minutes. If the tweet contains text, it will scan the text for potential names of companies with commonly traded stocks or popular cryptocurrencies. If the tweet contains an image or multiple images, the program will use ImageAI to locate images of Dogecoin or images of dogs. If the program finds images of dogecoin or text containing stocks or cryptocurrencies, it will send an SMS to the configured phone number using the Twilio API.

## Installation

1. <code>pip install requests</code>
2. <code>pip install -U python-dotenv</code>
3. <code>pip install twilio</code>
4. <code>pip install numpy</code>
5. <code>pip install tensorflow</code>
6. <code>pip install keras</code>
7. <code>pip install pillow</code>
8. <code>pip install scipy</code>
9. <code>pip install h5py</code>
10. <code>pip install opencv-python</code>
11. <code>pip install matplotlib</code>
12. <code>pip install keras-resnet</code>
13. <code>pip install imageai --upgrade</code>
14. Create a .env file add Twitter API consumer key, consumer secret key, and bearer token as shown in .env.example
15. Add the Twilio account sid and Twilio auth token to .env file as shown in the .env.example file
16. Replace line 67 with an array of phone numbers to SMS when stocks or cryptos are found in tweets.
```python
numbers_to_message = ['+000000000']
```
11. Replace line 110, 127, and 151 with Twilio number to send messages from. 
```python
from_='+000000000'
```

## Examples
### Image Recognition
<img src="public/img/doge-image.jpeg" width="600">

### Find stock in tweet
<img src="public/img/gamestop.png" width="600">

### Find crypto in tweet
<img src="public/img/dogecoin.png" width="600">

### Send alerts 
<img src="public/img/twilio-texts.PNG" width="600">
