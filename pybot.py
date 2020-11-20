import json
import tweepy
from helper import *
import time
import random
from os import path,system
filename = name+"_tweets.json"

# Cria Objeto de autenticacao
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Set up dos tokens
auth.set_access_token(access_token, access_token_secret)
# Cria objeto da api com autenticacao criada
api = tweepy.API(auth) 

#dicionario que vai guardar os tweetes
tweets = {}

#Funcao que adiciona um tweet novo ao dicionario, no formato adequado para fazer o parse pra json
def append_tweet(tweet):
    id = str(tweet.id)
    tweets[id] = {}
    tweets[id]['text'] = tweet.full_text
    tweets[id]['URL'] = "https://twitter.com/twitter/statuses/"+str(id)
    tweets[id]['online'] = True
    date = str(tweet.created_at)
    tweets[id]['day'] = date[8:10]
    tweets[id]['month'] = date[5:7]
    tweets[id]['year'] = date[0:4]

#Funcao que salva os dados no arquivo json
def save_file():
    database = open(filename,"w")
    database.write(json.dumps(tweets, indent=4))
    database.close()

#Tenta abrir o arquivo e fazer o parse do json
try:
    database = open(filename,"r")
    tweets = json.loads(database.read())
    database.close()
    print("Read json file")

#Se o arquivo nao existir ou nao estiver no formato certo pro parse
except:
    database = open(filename,"w")
    #Pega os ultimos 3000 tweets do usuario nome
    db = tweepy.Cursor(api.user_timeline, screen_name=name, tweet_mode="extended").items()
    for tweet in db:
        append_tweet(tweet)
    database.write(json.dumps(tweets, indent=4))
    database.close()
    print("Done saving files")

#Pra cada tweet salvo no json tenta acessar suas informacoes pela api, se tiver erro codigo 144 eh porque foi apagado
i = 0
for tweet_id in list(tweets.keys()):
    system('cls')    
    print("Analizing if current tweets in database still online (this take some time)...")
    print(str(i)+'/'+str(len(tweets)))
    try:
        api.get_status(int(tweet_id))
    except tweepy.TweepError as ex:
        if ex.api_code == 144:
            tweets[tweet_id]['online'] = False
    i+=1

save_file()
print("Done!")

print("Start listening to new tweets")
#loop infinito
while True:
    #pega todos os tweets
    results = tweepy.Cursor(api.user_timeline, screen_name=name, tweet_mode="extended").items()
    print("Retrieved " )

    #added = tweets antigos - tweets novos
    added = [tweet for tweet in results if str(tweet.id) not in list(tweets.keys())]
    if(len(added) > 0):
        print(str(len(added)) + " new tweets")

    #Adiciona os novos a lista
    for tweet in added:
        append_tweet(tweet)

    save_file()

    #para o codigo por delay segundos
    time.sleep(delay) 