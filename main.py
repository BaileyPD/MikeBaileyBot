import TwitterHandling2
import RedditScraperV2
import time
import pickle

# TODO Add check to see if Pi is connected to the internet, add a try catch for this error



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


TwitterHandling2.post_tweet_with_image("Test", "trialPlot.png")

