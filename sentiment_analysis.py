from textblob import TextBlob

from textblob import TextBlob

# Function to analyze sentiment
def analyze_sentiment(review_text):
    blob = TextBlob(review_text)
    sentiment = blob.sentiment.polarity
    
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"


def convert_review_to_emoji(review_text, rating):
    """
    Convert review text and rating into a sentiment and emoji format.
    :param review_text: The text of the review
    :param rating: The rating of the review (e.g., 5, 4, 3, etc.)
    :return: Tuple of sentiment and emoji representation of rating
    """
    sentiment = analyze_sentiment(review_text)
    star_emojis = "⭐" * int(rating)  # Convert numeric rating to stars
    return sentiment, star_emojis
