import streamlit as st
from recommend import df, recommend_movies
from omdb_utlis import get_movie_details

# OMDB API key from Streamlit Secrets
OMDB_API_KEY = st.secrets["omdb"]["api_key"]

# Streamlit page configuration
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# Title of the Streamlit app
st.title("🎬 Movie Recommender")

# Movie selection from the list of unique movie titles
movie_list = sorted(df['title'].dropna().unique())  # Ensure df has the 'title' column
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

# Button to trigger the recommendation process
if st.button("🚀 Recommend Similar Movies"):
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)  # Get movie recommendations

        # Check if no recommendations are found
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")

            # Loop through the recommended movies
            for _, row in recommendations.iterrows():
                movie_title = row['title']

                # Get the plot and poster of the movie using the OMDB API
                plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                # Display movie poster and plot
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=100)  # Display movie poster
                        else:
                            st.write("❌ No Poster Found")
                    with col2:
                        st.markdown(f"### {movie_title}")  # Display movie title
                        st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")  # Display plot
