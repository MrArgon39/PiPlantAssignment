from time import sleep
from datetime import datetime
import tweepy
from picamera import PiCamera
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
    )

auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
    )
tweet = tweepy.API(auth)
camera = PiCamera()
camera.rotation = 180

picture_title = datetime.now().strftime('%d|%m_%H:%M:%S')
camera.start_preview()
sleep(3)
camera.capture('/home/pi/Desktop/Tweepy/Photos/%s.jpg' % picture_title)
camera.stop_preview()
image = tweet.media_upload(filename = '/home/pi/Desktop/Tweepy/Photos/%s.jpg' %picture_title)
#print(image)

message = "This image was taken at %s" %picture_title
tweet.update_status(status=message, media_ids=[image.media_id])
#print("Tweeted: %s" % message)