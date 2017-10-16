import praw
import os
import pprint as pp

post_replied_fname = './data/post_replied.txt'


def max_paragraph_size(text):
    paragraphs = text.split('\n')
    largest_para = max([len(p) for p in paragraphs])
    return(largest_para)

# returns True if the text body is eligible for a reply
def eligible_body(text):
    ret = max_paragraph_size(text) > 3000
    return(ret)

def generate_reply(submission):
    reply_template_fname = './data/reply_template.md'
    with open(reply_template_fname,'r') as f:
        reply_msg = f.read()
    return(reply_msg)

def check_subreddit(subreddit, posts_replied_to):


    skipped_posts = 0
    for submission in subreddit.hot(limit=50):
        if submission.is_self and \
           (submission.id not in posts_replied_to) and \
           eligible_body(submission.selftext):
            length = max_paragraph_size(submission.selftext)
            print('-'*6)
            print('Post %s has length %d' % \
                  (submission.id,length))
            print('Replying to this post:\n%s' % submission.url)

            reply_msg = generate_reply(submission)

            # append this post ID to the list
            posts_replied_to.append(submission.id)
            with open(post_replied_fname, "a") as myfile:
                myfile.write(submission.id + '\n')

            reply_obj = submission.reply(reply_msg)
            print('The return value of submission reply was\n')
            try:
                pp.pprint(reply_obj)
            except:
                print('woops, couldnt print it')
            print('-'*6)
        else:
            skipped_posts += 1

    print('Skipped %d posts' % skipped_posts)

def main():
    reddit = praw.Reddit('bot1')
    subreddits = ['relationship_advice']

    if not os.path.isfile(post_replied_fname):
        posts_replied_to = []
    else:
        with open(post_replied_fname,'r') as f:
            posts_replied_to = [p for p in f.read().split('\n') if p != None]

    for sub_name in subreddits:
        print('subreddit: ' + sub_name)
        subreddit = reddit.subreddit(sub_name)
        check_subreddit(subreddit,posts_replied_to)
    # pp.pprint(posts_replied_to)

def unit_tests():
    print("Doing unit tests")
    inputs = [('data/example_long.txt',True),('data/example_short.txt',False)]
    for (fname,expected) in inputs:
        with open(fname,'r') as f:
            msg = f.read()
            assert(eligible_body(msg) == expected)

    print('Unit Tests Passed')

if __name__ == '__main__':
    print('\n\nTriggered\n')
    unit_tests()
    main()
    print('\nDone!\n')
