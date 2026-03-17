from services.analysis import load_data
from fastapi import FastAPI
from routes import recommendation, seller

app = FastAPI(
    title="ShelfSense API",
    description="AI powered recommendation system for bookstores",
    version="1.0"
)

# include route files
app.include_router(recommendation.router)
app.include_router(seller.router)


@app.get("/")
def home():
    return {"message": "ShelfSense backend running"}