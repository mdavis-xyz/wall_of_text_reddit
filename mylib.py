def max_paragraph_size(text):
    paragraphs = text.split('\n')
    largest_para = max([len(p) for p in paragraphs])
    return(largest_para)

# returns True if the text body is eligible for a reply
def eligible_body(text):
    ret = max_paragraph_size(text) > 3000
    return(ret)

