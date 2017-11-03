#27/10/2017

import tweepy
import csv
import codecs

CONSUMER_KEY='625ZQfhSVfqsvyKCr55jEzRUc'
CONSUMER_SECRET='cDKtARpFvLd1zabnlOv0U2w8UiJ5FkH5r5Y6xHwNTJYYaUUSHY'
ACCESS_KEY='233141182-P7WsuaHjsmnMYYyiLhbq9pBpQUSJyPPTKUHIistT'
ACCESS_SECRET='SHhl4hM0uDfUXQJBoFLdvmavrGHREyoGueQV2nx3Bs4Q6'

#Create twitter client - this information is obtained from the documentation,
#it is hard to make sense of it without reference to the twitter documentation.
auth=tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api_client=tweepy.API(auth)

tweets=tweepy.Cursor(api_client.search,
                     q="vitamin D", #search string, can add multiple words seperated with space
                     result_type="recent", #most recent results, can use "popular", "recent",
                     include_entities=True,
                     lang="en").items(20)

'''
ItemIterator objects are like lists but they contain much more metadata about the items in the list.

In python there are three ways(roughly) of dealing with ItemIterator objects:
    1.
    Put the ItemIterator inside a for loop, for example:
        for t in tweets:
            print(t.text)

2. Cast the ItemIterator into a list, then you can access it like a list, for example:
tweet_lists = list(tweets)
my_first_tweet = tweet_list[0]

3. Use the next() method of the ItemIterator objects, for example:
My_first_tweet = tweet_list.next()
'''

def get_tweets(expression_in, count_in):

    list_out=[]

    tweets = tweepy.Cursor(api_client.search,
                       q=expression_in,  # search string, can add multiple words seperated with space
                        result_type="recent",  # most recent results, can use "popular", "recent",
                        include_entities=True,
                        lang="en").items(count_in)

    #this just writes out the text only
    #for t in tweets:
    #    list_out.append(t.text)

    #more advanced to print out extra info on the author screen name, follower count and text
    tweets_list=list(tweets)
    for t in tweets_list:
        list_out.append((t.author.screen_name, t.author.followers_count, t.text))



    #write_to_csv(list_out)
    return list_out



def write_info_to_csv(tweet_info_list, csv_file_name):

    csv_file=[]
    #with open(csv_file_name, 'w')as my_file:  # open with write flag, if #file exists it is overwritten, but will be created if it doesn't exist.  #Without newline leaves one blank line inbetween each data row
    with codecs.open(csv_file_name, 'w', encoding='utf8') as my_file:
        my_writer = csv.writer(my_file, dialect='excel')
        my_writer.writerows(tweet_info_list)

    return


def print_tweets(tweet_info_list):
    for t in tweet_info_list:
        print("User {}, with {} followers, tweeted:".format(t[0], t[1]))
        print(t[2])
        print("\n")
    return


#31/10/2017

def get_word_freq(string_in):
    freq_table={}

    #Example:
    #get_word_freq( 'I saw the dog yesterday with two other dogs.  One of the dogs ws really big.')
    #freq_table=
    #{'I':1,
    # 'saw':1,
    # 'the':3,
    # 'dog':2,
    # ...
    # ...

    #freq_table.keys()
    #sum( freq_table.values() )

    #all_words=freq_table.keys() #returns all the unique words into a list, so lose
    #all_words.sort(keys=lamdba x: freq_table(x) )) #sort the unique words in terms of frequency in the
    # dictionary using the key based on freq

    for w in string_in.split():
        #print(w)
        if w in freq_table: #if already exists, need to increment value by 1
            #print(freq_table.items(), 'duplicate')
            freq_table[w]=freq_table[w]+1
        else: #if doesn't exist, set value to 1
            #print(freq_table.items(), 'doesnt exist')
            freq_table[w]=1

    #insert into tuple and then sort
    freq_table=list(freq_table.items())
    freq_table.sort(key=lambda x: x[1], reverse=True)
    return freq_table



def get_word_freq2(string_in):
    freq_table={}
    # this is your code for get_word_freq. Longer method than class solution

    unique_words = string_in.split()
    
    #now have list, made up of individual words
    print(unique_words, 'unique words')
    dict_out={}

    for w in unique_words:
        print(w, 'w value')

        if w in dict_out.keys(): #duplicate, then need to increment value
            already_list=dict_out[w]
            already_list+=1
            dict_out[w]=already_list

        else: #unique value, so add key and value of 1
            dict_out[w]=1

    return dict_out



#01/11/2017

def aggregate_tweets(tweets_list_in):

    # input: ['this is the text in tweet1','Here we have text in tweet2','More text but from tweet3']
    # output: 'this is the text in  tweet1, Here we have text in tweet2, More text but from tweet3'

    tweet_string_out=' '.join(tweets_list_in) #join is the opposite of split

    return tweet_string_out


def aggregate_tweets2(tweets_list_in):
    tweet_string_out = ''

    for tweet in tweets_list_in:
        tweet_string_out=tweet_string_out + ' ' + tweet

    return tweet_string_out[1:] #ignore first character, as has a leading space in the string otherwise


def write_freq_to_csv(freq_table, csv_file_name):
    #same code as write_info_to_csv
    csv_file=[]
    #with open(csv_file_name, 'w')as my_file:  # open with write flag, if #file exists it is overwritten, but will be created if it doesn't exist.  #Without newline leaves one blank line inbetween each data row
    with codecs.open(csv_file_name, 'w', encoding='utf8') as my_file:
        my_writer = csv.writer(my_file, dialect='excel')
        my_writer.writerows(freq_table)

    return


my_blacklist=['and','or','the','RT','in','at','on','a','this','&amp;','to','be']

def gen_csv(expression_in, count_in, tweet_file_name, freq_file_name):

    tweets=get_tweets(expression_in, count_in)
    write_info_to_csv(tweets, tweet_file_name)

    my_tweet_string=[x[2] for x in tweets]
    tweet_string=aggregate_tweets(my_tweet_string)
    frequencies=get_word_freq(tweet_string)
    frequencies=filter_words(my_blacklist, frequencies)

    write_freq_to_csv(frequencies, freq_file_name)

    return


my_marketing_list=[
    ('tesco', 50, 'tesco_tweets.csv', 'tesco_freq.csv'),
    ('sainsbury',50, 'sainsbury_tweets.csv','sainsbury_freq.csv'),
    ('asda',50, 'asda_tweets.csv','asda_freq.csv'),
    ('waitrose',50, 'waitrose_tweets.csv','waitrose_freq.csv')
]


def auto_gen_csv(marketing_list):

    for m in marketing_list:
        gen_csv(m[0], m[1], m[2], m[3])
    return


def filter_words(blacklist, freq_list_in):
    # example blacklist=['and','it','a']
    # example freq_list_in=[('london',10),('tesco',5),('and',2),('home',3),('it',2)]

    #output should be:
    #[ ('london',10),('tesco',5),('home',3) ]

    return [f for f in freq_list_in if (f[0] not in blacklist) and ('@' not in f[0][0]) and ('http' not in f[0][0])]