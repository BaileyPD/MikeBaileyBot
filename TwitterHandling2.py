import twitter
import ProcessingConfig
import pandas as pd
import pickle
# Goal of this file is to create a robust program for finding, processing and storing Twitter data

consumer_key = ProcessingConfig.mytwitter['consumer_key']
consumer_secret = ProcessingConfig.mytwitter['consumer_secret']
access_token_key = ProcessingConfig.mytwitter['access_token_key']
access_token_secret = ProcessingConfig.mytwitter['access_token_secret']

api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret, tweet_mode='extended',
                  sleep_on_rate_limit=True)
# Standard dataFrame Column headers for storing tweets
column_names1 = ["Screen name", "User ID", "Tweet ID", "Followers Count", "Tweet", "Date"]
# Standard dataFrame Column headers for storing users
column_names_users = ["Screen Name", "User ID", "Followers Count"]

# TODO: Add sentiment analysis
# TODO: Add Tweeting functions (Tweet, Re-Tweet, Like, etc.)


def get_stream():
    stream = api.GetStreamFilter(filter_level="low")
    for x in stream:
        print(x)


def get_statues(screen_name):
    """
    Gets the statues of a specified user
    :param screen_name: Screen name of the desired user
    """
    print(api.GetStatuses(screen_name))


def search_user(screen_name: str) -> str:
    """
    Searches user based on screen name "@screen_name" and returns a list of users with that name
    :param screen_name: screen name to search
    :return: numerical id of the user as a string
    """
    try:
        search_results = (api.UsersLookup(screen_name=screen_name))
        result_length = len(search_results)
        if result_length > 1:
            for x in result_length:
                print(result_length[x].id_str)
        else:
            return search_results[0].id_str
    except twitter.error.TwitterError:
        print("Error found with screenname:" + screen_name)


def get_user_statuses(id: str) -> str:
    results = api.GetUserTimeline(user_id=id)
    return results


def strip_screen_names(tweet: str) -> []:
    """
    Takes in the string from a Tweet and parses for screen names mentioned. Likely not the fastest implementation
    :param tweet: String from the specified tweet
    :return: List of found screen names
    """
    stop_characters = [":", ".", " ", ","]
    parse_position = 0
    at_symbol_pos = 0
    at_found = False
    found_names = []
    for x in tweet:
        if at_found:
            if x in stop_characters:
                z = tweet[at_symbol_pos:parse_position]
                if z not in found_names:
                    found_names.append(tweet[at_symbol_pos+1:parse_position])
                at_found = False
        if x == "@":
            at_symbol_pos = parse_position
            at_found = True
        parse_position = parse_position + 1
    return found_names


def collect_data(screennames: list, filename: str) -> []:
    data = pd.DataFrame(columns=column_names1)
    found_names = []
    for x in screennames:
        found_user = search_user(x)
        statuses = get_user_statuses(found_user)
        for y in statuses:
            new_names = strip_screen_names(y.full_text)
            for w in new_names:
                if w not in found_names:

                    found_names.append(w)
            if y is not None:
                data_list = [[x, found_user, y.id_str, "1", y.full_text, y.created_at]]
                appended_data = pd.DataFrame(columns=column_names1, data=data_list)
                data = data.append(other=appended_data, ignore_index=True)
    data.to_csv(path_or_buf=filename, sep="|")
    return found_names


def collect_screen_names(initial_names: [], filename: str):
    found_names = []
    for x in initial_names:
        found_user = search_user(x)
        statuses = get_user_statuses(found_user)
        for y in statuses:
            new_names = strip_screen_names(y.full_text)
            for w in new_names:
                if w not in found_names:
                    found_names.append(w)
    print(found_names)
    pickle_list(found_names, filename)


def tweet_points(followers: float, retweets: float, likes: float) -> float:
    """
    Takes a persons tweet and specifies a point value for determining whether to re-tweet
    :param followers: Specified users followers
    :param retweets: How many times the user's tweet has been re-tweeted
    :param likes:  How many times the user's tweet had been like
    :return: The point value of the tweet
    TODO add logic to check the rate at which the tweet is gaining likes and retweets to find tweets on the rise
    """
    followers_coefficient = 0.05
    retweets_coefficient = 0.25
    likes_coefficient = 0.25
    point_value = (followers * followers_coefficient) + (retweets * retweets_coefficient) + (likes*likes_coefficient)
    return point_value


def get_followers(screename: str) -> int:
    return len(api.GetFollowers(screen_name=screename))


def get_followers_list(screennames: []) -> []:
    return api.GetFollowers(user_id=screennames)


def retweet_algo(screennames: list):
    """
    Algorithm which looks at recent tweets from a list of users and determines the best one to re-tweet
    :param screennames: List of screen names to check
    """
    latest_statuses = []
    for x in screennames:
        found_user = search_user(x)
        followers = get_followers(x)
        print(followers)
        statuses = get_user_statuses(found_user)
        print(statuses[1])
        latest_statuses.append(statuses[1])


def pickle_list(input_list: [], filename: str):
    pickle.dump(input_list, open(file=filename, mode="wb"))


def unpickle_list(filename:str) -> []:
    return pickle.load(open(file=filename, mode="rb"))


def get_pickled_list_len(filename: str):
    print(len(unpickle_list(filename=filename)))


def clean_screen_name_list(screen_names: [], follower_threshold: int) -> []:
    """
    Takes a list of screen names and removes all the users with fewer followers than the follower threshold
    :param screen_names: List of screen names to clean up
    :param follower_threshold: Number of minimum followers required to remain in the list
    :return: new list of screen names
    """
    cleaned_list = []
    for x in screen_names:
        if get_followers(x) >= follower_threshold:
            cleaned_list.append(x)
    return cleaned_list


def get_specific_tweet(tweet_id: int):
    """
    Gets a specific tweet based on the tweet id
    :param tweet_id: Identification number of the desired tweet
    """
    print(api.GetStatus(status_id=tweet_id))


def post_tweet(message: str) -> bool:
    try:
        api.PostUpdate(status=message)
        return True
    except twitter.error.TwitterError:
        print("Error occured, unable to tweet")
        return False


def post_tweet_with_image(message: str, image_filename: str):
    try:
        api.PostUpdate(status=message, media=image_filename)
        return True
    except twitter.error.TwitterError:
        print("Error occurred, unable to tweet")
        return False

