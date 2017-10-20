import praw
import os
import pprint as pp
import mylib

comments_deleted_fname = './data/comments_deleted.txt'
comments_for_shortened_fname = './data/comments_for_shortened.txt'


def max_paragraph_size(text):
    paragraphs = text.split('\n')
    largest_para = max([len(p) for p in paragraphs])
    return(largest_para)

# returns True if the text body is eligible for a reply
def eligible_body(text):
    ret = max_paragraph_size(text) > 3000
    return(ret)

# reason is 'downvoted' or 'shortened'
def generate_comment(reason,comment):
    # comment options
    # ['MISSING_COMMENT_MESSAGE', 'STR_FIELD', 'approved_at_utc', 'approved_by', 'archived', 'author', 
    # 'author_flair_css_class', 'author_flair_text', 'banned_at_utc', 'banned_by', 'block', 'body', 
    # 'body_html', 'can_gild', 'can_mod_post', 'clear_vote', 'collapse', 'collapsed', 'collapsed_reason', 
    # 'controversiality', 'created', 'created_utc', 'delete', 'disable_inbox_replies', 'distinguished', 
    # 'downs', 'downvote', 'edit', 'edited', 'enable_inbox_replies', 'fullname', 'gild', 'gilded', 'id', 
    # 'is_root', 'is_submitter', 'likes', 'link_author', 'link_id', 'link_permalink', 'link_title', 
    # 'link_url', 'mark_read', 'mark_unread', 'mod', 'mod_reports', 'name', 'num_comments', 'num_reports', 
    # 'over_18', 'parent', 'parent_id', 'parse', 'permalink', 'quarantine', 'refresh', 'removal_reason', 
    # 'replies', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'score_hidden', 'stickied', 
    # 'submission', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_type', 'uncollapse', 
    # 'unsave', 'ups', 'upvote', 'user_reports']
    print('Editing comment %s for reason %s for post %s' % (comment.id,reason,comment.link_url))
    reply_template_fname = './data/templates/%s.md' % reason
    with open(reply_template_fname,'r') as f:
        msg = f.read()
    comment.edit(msg)        

def main():
    reddit = praw.Reddit('bot1')

    if not os.path.isfile(comments_deleted_fname):
        comments_deleted = []
    else:
        with open(comments_deleted_fname,'r') as f:
            comments_deleted = [p for p in f.read().split('\n') if p != None]


    comments_skipped = 0
    comments_deleted = 0
    short_skipped = 0
    short_deleted = 0

    print('fetching comments')
    comments = reddit.redditor('paragraphiser_bot').comments.controversial(time_filter='week')
    print('fetched comments')
    for c in comments:
        #print('processing comment ' + str(c.id))
        still_long = mylib.eligible_body(c.submission.selftext)
        if (c.score < 0) and (c.id not in comments_deleted):
            generate_comment('downvoted',c)
            comments_deleted += + 1
            if not still_long:
                short_deleted += 1
            with open(comments_deleted_fname, "a") as myfile:
                myfile.write(c.id + '\n')

        else:
            generate_comment('shortened',c)
            comments_skipped += 1
            if not still_long:
                short_skipped += 1
            with open(comments_for_shortened_fname, "a") as myfile:
                myfile.write(c.id + '\n')

    print('Deleted %d comments' % comments_deleted)
    print('   of which %d were now short enough' % short_deleted)
    print('Skipped %d comments' % comments_skipped)
    print('   of which %d are now short enough' % short_skipped)


def unit_tests():
    print("Doing unit tests")

    print('Unit Tests Passed')

if __name__ == '__main__':
    print('\n\nTriggered\n')
    unit_tests()
    main()
    print('\nDone!\n')
