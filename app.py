import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:8000"

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="ShelfSense AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ShelfSense AI Platform")
st.markdown(
"""
AI-powered **Book Recommendation & Seller Intelligence System**

This platform helps:
- Readers discover similar books
- Sellers analyze reading trends
- Predict future book demand
"""
)

# ----------------------------------
# SIDEBAR
# ----------------------------------

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "📖 Book Recommendation",
        "👤 User Behaviour",
        "🏪 Seller Dashboard"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
"""
ShelfSense AI converts **reader behaviour into business intelligence**.

Sellers can identify:
- Trending books
- Future demand
- Reader interests
"""
)

# ----------------------------------
# PAGE 1 : BOOK RECOMMENDATION
# ----------------------------------

if page == "📖 Book Recommendation":

    st.header("📖 Book Recommendation Engine")

    st.write(
    """
    Enter a book name to find **similar books that readers also enjoyed**.
    """
    )

    book = st.text_input(
        "Enter Book Name",
        placeholder="Example: Harry Potter"
    )

    if st.button("Get Recommendations"):

        if book == "":
            st.warning("Please enter a book name")

        else:

            with st.spinner("Finding similar books..."):

                try:

                    r = requests.get(f"{API}/recommend/{book}")
                    r.raise_for_status()

                    data = r.json()

                    recs = data.get("recommendations", [])

                    if len(recs) == 0:

                        st.info("No recommendations found")

                    else:

                        st.success("📚 Top Recommended Books")

                        col1, col2, col3 = st.columns(3)

                        for i, rec in enumerate(recs):

                            if i % 3 == 0:
                                col1.markdown(f"📘 **{rec}**")

                            elif i % 3 == 1:
                                col2.markdown(f"📗 **{rec}**")

                            else:
                                col3.markdown(f"📙 **{rec}**")

                except:

                    st.error("Backend API not responding")


# ----------------------------------
# PAGE 2 : USER BEHAVIOUR
# ----------------------------------

elif page == "👤 User Behaviour":

    st.header("👤 Simulate User Reading Behaviour")

    st.write(
    """
    This module simulates how users interact with books.
    These interactions help the system learn **reader preferences**.
    """
    )

    col1, col2 = st.columns(2)

    with col1:
        user_id = st.number_input("User ID", min_value=1)

    with col2:
        book_read = st.text_input(
            "Book Name",
            placeholder="Example: Atomic Habits"
        )

    if st.button("Record Reading Behaviour"):

        if book_read == "":
            st.warning("Enter a book name")

        else:

            with st.spinner("Recording interaction..."):

                try:

                    r = requests.post(
                        f"{API}/user/read",
                        params={
                            "book": book_read,
                            "user_id": user_id
                        }
                    )

                    r.raise_for_status()

                    st.success(
                        "User interaction recorded successfully"
                    )

                except:

                    st.error("Could not record interaction")


# ----------------------------------
# PAGE 3 : SELLER DASHBOARD
# ----------------------------------

elif page == "🏪 Seller Dashboard":

    st.header("🏪 Seller Intelligence Dashboard")

    st.success(
    """
    📊 This dashboard converts **user reading behaviour into business insights**.

    Sellers can identify:
    - Which books are trending
    - Which books may trend soon
    - What readers are currently reading
    """
    )

    col1, col2 = st.columns(2)

    # ----------------------------------
    # TRENDING BOOKS
    # ----------------------------------

    with col1:

        st.subheader("📈 Trending Books (Based on User Activity)")

        if st.button("Load Trending Books"):

            with st.spinner("Analyzing reading trends..."):

                try:

                    r = requests.get(f"{API}/seller/trending")
                    r.raise_for_status()

                    data = r.json()

                    df = pd.DataFrame(data["trending_books"])

                    st.metric("Trending Books", len(df))

                    st.bar_chart(
                        df.set_index("title")["trend_score"]
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    top_book = df.iloc[0]["title"]

                    st.info(
                        f"""
                        📊 Insight:

                        **{top_book}** is currently trending because multiple
                        users are interacting with this book.

                        📌 Sellers should consider increasing inventory
                        for this title.
                        """
                    )

                except:

                    st.error("Could not load trending data")


    # ----------------------------------
    # DEMAND PREDICTION
    # ----------------------------------

    with col2:

        st.subheader("📊 Demand Prediction")

        if st.button("Predict Future Demand"):

            with st.spinner("Running prediction model..."):

                try:

                    r = requests.get(
                        f"{API}/seller/predict-demand"
                    )

                    r.raise_for_status()

                    data = r.json()

                    df = pd.DataFrame(
                        data["predicted_trending_books"]
                    )

                    st.metric(
                        "Books Likely to Trend",
                        len(df)
                    )

                    st.bar_chart(
                        df.set_index("title")["demand_score"]
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    predicted = df.iloc[0]["title"]

                    st.info(
                        f"""
                        🔮 Prediction Insight:

                        **{predicted}** shows high demand probability
                        based on user behaviour and reading patterns.

                        📌 Sellers should prepare inventory for this title.
                        """
                    )

                except:

                    st.error("Prediction service unavailable")

    st.divider()

    # ----------------------------------
    # USER INSIGHTS
    # ----------------------------------

    st.subheader("📊 User Reading Behaviour Insights")

    if st.button("Analyze User Reads"):

        with st.spinner("Analyzing reading behaviour..."):

            try:

                r = requests.get(
                    f"{API}/seller/user-insights"
                )

                r.raise_for_status()

                data = r.json()

                books = data.get(
                    "books_users_are_reading",
                    []
                )

                if len(books) == 0:

                    st.warning("No user data available")

                else:

                    df = pd.DataFrame(
                        books,
                        columns=["Book", "Reads"]
                    )

                    st.metric(
                        "Books Analyzed",
                        len(df)
                    )

                    st.bar_chart(
                        df.set_index("Book")["Reads"]
                    )

                    st.dataframe(
                        df,
                        use_container_width=True
                    )

                    top = df.iloc[0]["Book"]

                    st.success(
                        f"""
                        📚 Behaviour Insight:

                        Readers are currently most interested in
                        **{top}** based on reading frequency.
                        """
                    )

                    st.markdown(
                    """
                    ### 📌 Seller Strategy Recommendations

                    - Increase stock for highly read books  
                    - Promote trending books in marketing campaigns  
                    - Recommend similar titles to readers  
                    - Track emerging reading patterns early  
                    """
                    )

            except:

                st.error("Could not analyze user behaviour")