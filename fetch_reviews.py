import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the values from the .env file
API_URL = os.getenv("GOOGLE_PLACES_API_URL")
API_KEY = os.getenv("GOOGLE_API_KEY")
PLACE_ID = os.getenv("PLACE_ID")

# Check if environment variables are loaded correctly
if not API_URL or not API_KEY or not PLACE_ID:
    raise ValueError("Missing environment variables: Please check .env file.")

def fetch_reviews():
    reviews = []
    next_page_token = None
    retry_count = 0  # Counter to keep track of retries

    while True:
        # Construct the URL for the API request
        url = f"{API_URL}?placeid={PLACE_ID}&key={API_KEY}"
        if next_page_token:
            url += f"&pagetoken={next_page_token}"

        # Make the API request
        print(f"Making request to URL: {url}")
        response = requests.get(url)
        data = response.json()

        # Handle rate-limiting
        if response.status_code == 429:
            print("Rate-limited. Waiting before retrying...")
            retry_count += 1
            wait_time = 2 ** retry_count  # Exponential backoff (e.g., 2, 4, 8 seconds)
            print(f"Retrying after {wait_time} seconds...")
            time.sleep(wait_time)
            continue  # Retry the request after delay

        # Check for API errors
        if "error_message" in data:
            print(f"Error: {data['error_message']}")
            break

        if "result" in data:
            reviews.extend(data["result"].get("reviews", []))
        else:
            print("Error fetching reviews:", data)
            break

        # Check if there is a next page of reviews
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break  # Exit the loop if no more reviews are available

        # Delay to avoid making too many requests too quickly
        print("Waiting for next page...")
        time.sleep(2)  # Sleep for 2 seconds before fetching the next page

    return reviews

# Save reviews to a file
def save_reviews_to_file(reviews):
    with open("reviews_log.txt", "a") as file:
        for review in reviews:
            original_review = review.get("text", "No Review")
            rating = review.get("rating", "No Rating")
            file.write(f"Original Review: {original_review}\n")
            file.write(f"Rating: {rating}\n")
            file.write("-" * 40 + "\n")
    print(f"Total reviews fetched: {len(reviews)}")
