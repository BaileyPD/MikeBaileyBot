import TwitterHandling2
import RedditScraperV2
import time
import pickle


def tweet_top_reddit_posts(subreddits: [], hashtags: [], freq: int, limit: int):
    file_name = "SavedTweets.p"
    post_id = unpickle_list(file_name)
    cont = True
    count_limit = 5
    while cont:
        next_posts = RedditScraperV2.get_hottest_submission(subreddits, limit)
        current_count = 0
        tweeted = False
        for curr_post in next_posts:
            if curr_post.id not in post_id:
                print(curr_post.url)
                hashtag_str = str
                for x in hashtags:
                    hashtag_str = hashtag_str + " "
                    print(hashtag_str)
                desired_tweet = curr_post.title + " " + hashtag_str + curr_post.url
                if (len(desired_tweet) - len(curr_post.url)) >= 165:
                    hashtag_len = len(hashtag_str)
                    # 165 is twitter char lim, 23 is the simplfied URL len, 2 for spaces, 3 for the "..."
                    post_stop_index = 165 - 23 - 2 - hashtag_len - 3
                    post_content = curr_post.title[0:post_stop_index]
                    desired_tweet = post_content + "... " + hashtags[0] + " " + curr_post.url
                    tweeted = TwitterHandling2.post_tweet(desired_tweet)
                else:
                    tweeted = TwitterHandling2.post_tweet(desired_tweet)
                post_id.append(curr_post.id)
                if current_count >= count_limit:
                    print("Saving IDs")
                    print("IDs: " + str(post_id))
                    if len(post_id) > (freq * 24):
                        post_id = post_id[12:len(post_id)-1]
                    pickle_list(post_id, file_name)
                if tweeted:
                    current_count = current_count + 1
                    break
                else:
                    continue
            else:
                continue
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
