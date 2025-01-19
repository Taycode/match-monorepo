import re


def tweet_length_with_shortened_links(text: str) -> int:
    """
    Calculate the length of a tweet, assuming that any URL is
    automatically shortened to 23 characters (typical Twitter behavior).

    :param text: The original tweet text (could include multiple links).
    :return: The integer length of the tweet after links are shortened.
    """
    # A simplistic URL-matching regex that looks for http/https links
    url_pattern = re.compile(r'https?://[^\s]+')

    # For each match, replace with 23 'x' characters (or any placeholder)
    # Then measure the resulting text length
    shortened_text = url_pattern.sub(lambda match: 'x' * 23, text)

    return len(shortened_text)
