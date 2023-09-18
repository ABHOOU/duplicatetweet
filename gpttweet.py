import tweepy
import openai

# Configuration des clés d'API Twitter
consumer_key = 'consumer key here'
consumer_secret = 'consumer secret here'
access_token = 'access token here'
access_token_secret = 'access token here'

# Configuration des clés d'API OpenAI GPT-3
openai.api_key = 'chat gpt api here'

# Fonction pour récupérer les nouveaux tweets d'un compte Twitter
def get_new_tweets(username, since_id):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=username, since_id=since_id, tweet_mode="extended")
    return tweets

def get_new_tweets_v2(username, since_id):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        user = api.get_user(username)
        user_id = user.id
        tweets = api.user_timeline(user_id=user_id, since_id=since_id)
        return tweets
    except AttributeError:
        print(f"Une erreur s'est produite lors de la récupération des tweets : {str(e)}")
        return []
# Fonction pour modifier un tweet en utilisant GPT-3
def modify_tweet_with_gpt3(tweet_text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Modifiez le tweet suivant : '{tweet_text}'",
        max_tokens=50  # Nombre maximum de tokens dans la réponse
    )
    modified_tweet = response.choices[0].text
    return modified_tweet

# Fonction pour publier un tweet modifié
def post_tweet(api, modified_tweet):
    api.update_status(modified_tweet)

# Compte Twitter source (celui dont vous voulez récupérer les tweets)
source_username = ''
# Compte Twitter destination (celui sur lequel vous voulez publier les tweets modifiés)
destination_username = ''

# ID du dernier tweet traité (pour éviter de traiter les tweets déjà traités)
last_processed_tweet_id = None

while True:
    try:
        # Récupérer les nouveaux tweets depuis le dernier tweet traité
        new_tweets = get_new_tweets_v2(source_username, last_processed_tweet_id)

        # Traiter les nouveaux tweets
        for tweet in new_tweets:
            tweet_text = tweet.text  # Utilisez .text pour obtenir le texte du tweet
            # Effectuez ici les modifications nécessaires avec GPT-3

            # Marquez le tweet comme traité
            last_processed_tweet_id = tweet.id

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
