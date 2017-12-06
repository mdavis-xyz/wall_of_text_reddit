def max_paragraph_size(text):
    paragraphs = text.split('\n')
    largest_para = max([len(p) for p in paragraphs])
    return(largest_para)

# returns True if the text body is eligible for a reply
def eligible_body(text):
    # threshold: https://www.reddit.com/r/relationship_advice/comments/7hx5d3/i_22m_am_getting_confused_by_a_friend_21f_i_need/
    ret = max_paragraph_size(text) > 2300
    return(ret)

# TODO: check for keywords like suicide
