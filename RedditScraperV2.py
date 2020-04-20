import praw
import ProcessingConfig as PC

client_id = PC.myreddit['client_id']
client_secret = PC.myreddit['secret']
username = PC.myreddit['username']
password = PC.myreddit['password']
user_agent = PC.myreddit['user_agent']


reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username,
                     password=password)


# TODO: Add sentiment Analysis
# TODO: Add functions which allow input of subreddit name, number of submissions, return average sentiment
# TODO: Add function which allows input of subreddit name, number of submissions, return list of submissions

def get_subreddit_submissions(subreddit_name: [], limit: int) -> []:
    submissions = []
    for current_sub in subreddit_name:
        subreddit = reddit.subreddit(current_sub)
        posts = subreddit.hot(limit=limit)
        for sub in posts:
            submissions.append(sub)
    return submissions


def get_subreddit_submissions_single(subreddit_name: str, limit = int):
    submissions = []
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.hot(limit=limit)
    for sub in posts:
        submissions.append(sub)
        print(sub.title)


def get_subreddit_submission_comments(subreddit_name: [], limit: int) -> []:
    comments = []
    submissions_comment = get_subreddit_submissions(subreddit_name, limit)
    for sub_com in submissions_comment:
        comments_new = list(sub_com.comments)
        for idv_com in comments_new:
            comments.append(idv_com)
    return comments


def get_hottest_submission(subreddits: [], limit: int) -> []:
    top_posts = []
    #print("Subreddits:" + str(subreddits))
    subscribers = []
    cap = 0
    for sub in subreddits:
        internal_posts = []
        subscribers = get_subreddit_subscriber_count(sub)
        for post in get_subreddit_submissions([sub], limit):
            internal_posts.append(post)
        for x in internal_posts:
            normalized_score = x.score / subscribers
            #print("Normalized Score: " + str(normalized_score) + "| Title: " + x.title)
            if normalized_score > cap:
                cap = normalized_score
                top_posts.insert(0, x)
    #print("Current Cap Value: " + str(cap))
    return top_posts


def get_subreddit_subscriber_count(subreddit_name: str) -> int:
    return reddit.subreddit(subreddit_name).subscribers


def get_subreddit_subscriber_count_multi(subreddit_names: []) -> []:
    subcount_list = []
    for x in subreddit_names:
        subcount_list.append(reddit.subreddit(x).subscribers)
    return subcount_list


#get_subreddit_submissions_single("News", limit=10)
#for x in get_subreddit_submissions(["News", "WorldNews", "Politics"], limit=10):
#    print(x.title)
#print(get_hottest_submission(['News', 'WorldNews', 'Politics'], limit=10).title)
#for_loop_testing(['News', 'WorldNews', 'Politics'])