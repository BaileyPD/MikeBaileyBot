import TwitterHandling2
import RedditScraperV2
import time
import pickle


def tweet_top_reddit_posts(subreddits: [], hashtags: [], freq: int, limit: int):
    next_post = RedditScraperV2.get_hottest_submission(subreddits, limit)
    file_name = "SavedTweets.p"
    post_id = unpickle_list(file_name)
    cont = True
    count_limit = 5
    while cont:
        current_count = 0
        for curr_post in next_post:
            if curr_post.id not in post_id:
                print(curr_post.url)
                TwitterHandling2.post_tweet(curr_post.title + " " + hashtags[0] + " " + curr_post.url)
                post_id.append(curr_post.id)
                current_count = current_count + 1
                break
            else:
                continue
        if current_count >= count_limit:
            pickle_list(post_id, file_name)
        time.sleep(3600 / freq)


def pickle_list(input_list: [], filename: str):
    file = open(file=filename, mode="wb")
    data = pickle.dump(input_list, file)
    file.close()
    return data


def unpickle_list(filename: str) -> []:
    file = open(file=filename, mode="rb")
    data = pickle.load(file)
    file.close()
    return data


pickle_list([], filename="SavedTweets.p")
tweet_top_reddit_posts(["News", "WorldNews", "Politics", "coronavirus"], ["#News"], freq=2, limit=10)
