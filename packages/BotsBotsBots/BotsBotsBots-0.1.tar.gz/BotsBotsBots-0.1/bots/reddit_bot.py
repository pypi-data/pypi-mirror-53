import inspect
import pprint

import praw

with open('credentials.txt', 'r') as handle:
    lines = handle.readlines()
    client_id = lines[0].strip()
    client_secret = lines[1].strip()
    password = lines[2].strip()
    user_agent = lines[3].strip()
    username = lines[4].strip()


# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
def get_read_only_reddit():
    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent=user_agent)


def get_authorized_reddit():
    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent=user_agent,
                       username=username,
                       password=password)


def read_only_test():
    reddit = get_read_only_reddit()

    print(reddit.read_only)

    for submission in reddit.subreddit('dankmemes').hot(limit=2):
        print(submission.title)
        print('SUBMISSION ATTRIBUTES:')
        pprint.pprint(vars(submission))
        print('SUBMISSION METHODS:')
        pprint.pprint(inspect.getmembers(submission, predicate=inspect.ismethod))
        print('\n')


def authorized_reddit_test():
    reddit = get_authorized_reddit()
    return reddit


def available_attributes():
    # assume you have a Reddit instance bound to variable `reddit`
    reddit = get_read_only_reddit()
    submission = reddit.submission(id='39zje0')
    print(submission.title)  # to make it non-lazy
    pprint.pprint(vars(submission))


read_only_test()

# # Create a submission to /r/test
# reddit.subreddit('test').submit('Test Submission', url='https://reddit.com')
#
# # Comment on a known submission
# submission = reddit.submission(url='https://www.reddit.com/comments/5e1az9')
# submission.reply('Super rad!')
#
# # Reply to the first comment of a weekly top thread of a moderated community
# submission = next(reddit.subreddit('mod').top('week'))
# submission.comments[0].reply('An automated reply')
#
# # Output score for the first 256 items on the frontpage
# for submission in reddit.front.hot(limit=256):
#     print(submission.score)
#
# # Obtain the moderator listing for redditdev
# for moderator in reddit.subreddit('redditdev').moderator:
#     print(moderator)
