from fastapi import APIRouter
from model.recommender import get_recommendations
from services.analysis import knn_model, book_dna, df_rec

router = APIRouter()

@router.get("/recommend/{book}")
def recommend(book: str):

    recs = get_recommendations(book, knn_model, book_dna, df_rec)

    return {
        "input_book": book,
        "recommendations": recs
    }
@router.post("/user/read")
def user_read(book: str, user_id: int):
    return {
        "message": "User interaction recorded",
        "user": user_id,
        "book": book
    }