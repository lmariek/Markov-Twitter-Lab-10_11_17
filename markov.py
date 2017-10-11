"""A Markov chain generator that can tweet random messages."""

import os
import sys
from random import choice
import twitter
import time

str_punctuation = ['.', '!', '?']

def open_and_read_file(file_names):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """
    for file_path in file_names:
        with open(file_path) as markov_text:
            text_string = markov_text.read()   

    return text_string


def make_chains(text_string):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """

    chains = {}
    words_list = text_string.split()

    for i in range(len(words_list)-2):

        key = (words_list[i], words_list[i+1])
        value = words_list[i + 2]

        chains[key] = chains.get(key, [])
        #append the value to values the list at keys
        chains[key].append(value)

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []
    #creating a list of all keys from the chains dictionary
    all_keys = chains.keys()
    #choosing a random key, using the choice() module
    key = choice(all_keys)

    while True:
        #check if first character of first work is capitalized
        if key[0][0].isupper():
            #convert tuple to a list and set as the initial 'words' list
            words = list(key)
            break
        #if first character not capitalized, choose another random key
        else:
            key = choice(all_keys)

    while True:
        #if the key exists in the chains dictionary
        if key in chains:
            #create a new link (tuple)
            new_key = (key[1], choice(chains[key]))
            #append the link to the 'words' list
            words.append(new_key[1])
            #rebind key to the new link
            key = new_key
            #if key ends with punctuation mark, stop
            if key[1][-1] in str_punctuation:
                break
        else:
            break

    markov_chain_text = " ".join(words)

    #return the list of links as a string
    return markov_chain_text

def shorten_text(markov_chain_text):
    """ Takes a markov chain and returns a chain with less than 140 characters
        (to post to Twitter). """

    while True:
        #check the length of the markov chain
        if len(markov_chain_text) > 140:
            #if greater than 140 chars, generate a new chain
            new_chain = make_text(chains)
            #set value of chain to test to new chain
            markov_chain_text = new_chain
        else:
            #if less than 140, all good!
            break

    return markov_chain_text

def tweet(markov_chain_text):
    """Create a tweet and send it to the Internet."""

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # This will print info about credentials to make sure 
    # they're correct
    print api.VerifyCredentials()

    # Send a tweet
    status = api.PostUpdate(markov_chain_text)
    print status.text

    
#use sys.arg to pass multiple files as arguments, from the terminal
input_paths = sys.argv[1:]

# Open the file and turn it into one long string
input_text = open_and_read_file(input_paths)

# Get a Markov chain
chains = make_chains(input_text)

while True:

    # Produce random text
    markov_chain_text = make_text(chains)

    # Check char limit for twitter
    markov_tweet = shorten_text(markov_chain_text)

    print markov_tweet

    # Tweet out chain
    tweet(markov_tweet)

    time.sleep(10)

