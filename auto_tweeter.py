import os
import time
import tweepy
import random
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Twitter API credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Game story structure
game_story = {
    "start": {
        "text": "🎮 Welcome to #TwitterQuest! You find yourself in a mysterious room. There's a dusty old book on a table and a strange mirror on the wall. What do you do?\n\nA) Examine the book\nB) Look in the mirror\n\n#TextGame #InteractiveFiction",
        "choices": {
            "A": "book_examine",
            "B": "mirror_examine"
        }
    },
    "book_examine": {
        "text": "📚 The book is titled 'Secrets of the Digital Realm'. As you open it, a small key falls out. The pages seem to be written in code.\n\nA) Try to decode the text\nB) Pick up the key\n\n#TwitterQuest",
        "choices": {
            "A": "decode_text",
            "B": "take_key"
        }
    },
    "mirror_examine": {
        "text": "🪞 The mirror ripples like water when you approach. You see strange symbols floating in its surface. Your reflection looks... different.\n\nA) Touch the mirror\nB) Read the symbols\n\n#TwitterQuest",
        "choices": {
            "A": "touch_mirror",
            "B": "read_symbols"
        }
    },
    "decode_text": {
        "text": "🔍 The code seems to be a simple cipher. You decode: 'The mirror leads to digital worlds, but only the chosen key will unlock its power.'\n\nA) Go to the mirror\nB) Search for more clues\n\n#TwitterQuest",
        "choices": {
            "A": "mirror_examine",
            "B": "search_room"
        }
    },
    "take_key": {
        "text": "🔑 You pick up the key. It's warm to the touch and seems to pulse with a faint blue light.\n\nA) Try it on the mirror\nB) Look for a keyhole in the room\n\n#TwitterQuest",
        "choices": {
            "A": "mirror_key",
            "B": "search_room"
        }
    },
    "touch_mirror": {
        "text": "✨ Your hand passes through! But something feels wrong - you need a key to stabilize the portal.\n\nA) Pull your hand back\nB) Search the room for a key\n\n#TwitterQuest",
        "choices": {
            "A": "start",
            "B": "search_room"
        }
    },
    "read_symbols": {
        "text": "📝 The symbols form a riddle: 'Through glass and code, a world awaits, but only with the key can you pass these gates.'\n\nA) Look for the key\nB) Try to enter anyway\n\n#TwitterQuest",
        "choices": {
            "A": "search_room",
            "B": "touch_mirror"
        }
    },
    "search_room": {
        "text": "🔍 You search the room carefully. Besides the book and mirror, you notice strange markings on the floor.\n\nA) Return to the book\nB) Examine the markings\n\n#TwitterQuest",
        "choices": {
            "A": "book_examine",
            "B": "floor_markings"
        }
    },
    "mirror_key": {
        "text": "🌟 The key fits perfectly! The mirror's surface becomes a swirling portal. Congratulations, you've solved the first puzzle! Stay tuned for your next #TwitterQuest adventure!\n\nA) Start a new game\n\n#TextGame",
        "choices": {
            "A": "start"
        }
    },
    "floor_markings": {
        "text": "📍 The markings form a circle with symbols matching those in the mirror. There's a small indentation that looks key-shaped.\n\nA) Check the book again\nB) Return to the mirror\n\n#TwitterQuest",
        "choices": {
            "A": "book_examine",
            "B": "mirror_examine"
        }
    }
}

# Store the current game state
current_game_state = "start"
last_tweet_id = None

def create_tweet():
    """
    Create and return the current game scenario
    """
    global current_game_state, last_tweet_id
    
    # If there's a last tweet, check for replies to determine next state
    if last_tweet_id:
        try:
            # Get replies to the last tweet
            replies = api.search_tweets(q=f"to:@{api.verify_credentials().screen_name}", since_id=last_tweet_id)
            
            if replies:
                # Get the most recent valid choice
                for reply in replies:
                    choice = reply.text.strip().upper()
                    if choice in game_story[current_game_state]["choices"]:
                        current_game_state = game_story[current_game_state]["choices"][choice]
                        break
        except Exception as e:
            print(f"Error checking replies: {str(e)}")
    
    return game_story[current_game_state]["text"]

def send_tweet():
    """Send a tweet using the Twitter API"""
    global last_tweet_id
    try:
        tweet_content = create_tweet()
        tweet = api.update_status(tweet_content)
        last_tweet_id = tweet.id
        print(f"Tweet sent successfully: {tweet_content}")
    except Exception as e:
        print(f"Error sending tweet: {str(e)}")

def main():
    print("Starting TwitterQuest...")
    while True:
        try:
            send_tweet()
            # Wait for 20 minutes
            time.sleep(20 * 60)
        except KeyboardInterrupt:
            print("\nStopping TwitterQuest...")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            # Wait for 1 minute before retrying in case of an error
            time.sleep(60)

if __name__ == "__main__":
    main()
