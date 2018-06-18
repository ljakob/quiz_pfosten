#!/usr/bin/env python

import json
import pprint
import sseclient
import requests
import LedAnimation
import time

def with_urllib3(url):
    import urllib3
    http = urllib3.PoolManager()
    return http.request('GET', url, preload_content=False)

def with_requests(url):
    import requests
    return requests.get(url, stream=True)

url = 'http://docker.o11.net:7999/stream'
response = requests.get(url, stream=True, allow_redirects=False, headers={'Accept': 'text/event-stream'})
print("Event handler is waiting for messages...")

def event_loop():
    client = sseclient.SSEClient(response.iter_content())
    for event in client.events():
        try:
            json_message = json.loads(event.data)
            pprint.pprint(json_message)
        except (ValueError):
            print("Warning: event handler did not understand your message :(")
            continue

        if 'quizevent' not in json_message:
            print("Warning: event handler did not receive quizevent")
            continue
        quiz_event = json_message['quizevent']

	if 'score' not in json_message:
            print("Warning: event handler dit not receive score")
            continue
        score = int(json_message['score'])

        handle_event(quiz_event, score)

def handle_event(quiz_event, score):
    print("Receveived quiz_event=" + quiz_event + " with score=" + str(score))
    quiz_event = '' + quiz_event
    print(len(quiz_event))
    if quiz_event == 'start':
        print("start")
        LedAnimation.led_idle_stop()
        LedAnimation.led_busy_start()

    elif quiz_event == 'end':
        print("end")
        LedAnimation.led_idle_start()

    elif quiz_event == 'correct':
        print("correct")
        LedAnimation.led_busy_stop()
        LedAnimation.led_event_correct()
        LedAnimation.led_show_score_ani(score)
	time.sleep(2)
        LedAnimation.led_busy_start()

    elif quiz_event == 'incorrect':
        print("incorrect")
        LedAnimation.led_busy_stop()
        LedAnimation.led_event_incorrect()
        LedAnimation.led_show_score_ani(score)
	time.sleep(2)
        LedAnimation.led_busy_start()
    else:
        print("Warning: unknown event received")
    print("Event processing done.")

LedAnimation.led_setup()
LedAnimation.led_idle_start()

event_loop()
