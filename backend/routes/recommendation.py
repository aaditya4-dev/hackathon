from fastapi import APIRouter
from model.recommender import get_recommendations
from services.analysis import knn_model, book_dna, df_rec
from database.db import conn

router = APIRouter()


# ------------------------------
# RECOMMEND BOOKS
# ------------------------------
@router.get("/recommend/{book}")
def recommend(book: str):

    try:
        # AI recommendation
        recs = get_recommendations(book, knn_model, book_dna, df_rec)

        # track behaviour automatically
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_reads (user_id, book) VALUES (?, ?)",
            (1, book)
        )
        conn.commit()

        return {
            "input_book": book,
            "recommendations": recs
        }

    except Exception as e:
        return {
            "input_book": book,
            "recommendations": [],
            "error": str(e)
        }


# ------------------------------
# MANUAL USER READ (OPTIONAL)
# ------------------------------
@router.post("/user/read")
def user_read(book: str, user_id: int):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO user_reads (user_id, book) VALUES (?, ?)",
        (user_id, book)
    )

    conn.commit()

    return {
        "message": "User interaction recorded",
        "user": user_id,
        "book": book
    }