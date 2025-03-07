from fastapi import FastAPI
from fetch_reviews import fetch_reviews, save_reviews_to_file
import threading
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

# Store all fetched reviews
all_reviews = []

# Fetch and store reviews on startup
@app.on_event("startup")
async def on_startup():
    fetch_and_store_reviews()
    start_review_polling()

# Function to fetch and store reviews
def fetch_and_store_reviews():
    new_reviews = fetch_reviews()
    all_reviews.extend(new_reviews)
    save_reviews_to_file(new_reviews)  # Save reviews to the file
    print("🚀 Reviews fetched and stored.")

# Background job to fetch new reviews every 5 minutes
def fetch_new_reviews():
    new_reviews = fetch_reviews()
    all_reviews.extend(new_reviews)
    save_reviews_to_file(new_reviews)  # Save new reviews to the file
    print("🔄 New reviews fetched.")

# Start background review fetching
def start_review_polling():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_new_reviews, 'interval', minutes=5)
    scheduler.start()

# API Endpoint: Retrieve all reviews
@app.get("/fetch_and_display_reviews")
async def get_reviews():
    return {"reviews": all_reviews}

# API Endpoint: Submit a new review
@app.post("/submit_review")
async def submit_review(review: dict):
    original_review = review.get('review')
    rating = review.get('rating')
    
    # Store review
    all_reviews.append({"review": original_review, "rating": rating})
    save_reviews_to_file([{"text": original_review, "rating": rating}])  # Save new review to the file

    return {"message": "Review submitted successfully", "review": original_review, "rating": rating}

if __name__ == "__main__":
    threading.Thread(target=start_review_polling).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
