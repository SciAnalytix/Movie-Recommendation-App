import gdown
import joblib
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("recommend.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Google Drive file IDs
COSINE_SIM_FILE_ID = '1QPkZsaCsGl9yrZYi3hMxyJ7fMLTdG1XO'
DF_CLEANED_FILE_ID = '1jJGqYT0vgdpyknbDzxThq7aDrZsw9uin'

# Function to download files from Google Drive
def download_files():
    logging.info("🔁 Downloading data files from Google Drive...")

    # Download the files if they don't already exist
    if not os.path.exists('df_cleaned.pkl'):
        gdown.download(f'https://drive.google.com/uc?id={DF_CLEANED_FILE_ID}', 'df_cleaned.pkl', quiet=False)
    if not os.path.exists('cosine_sim.pkl'):
        gdown.download(f'https://drive.google.com/uc?id={COSINE_SIM_FILE_ID}', 'cosine_sim.pkl', quiet=False)
    logging.info("✅ Files downloaded successfully.")

# Download the files
download_files()

# Load the downloaded files
logging.info("🔁 Loading data...")

try:
    df = joblib.load('df_cleaned.pkl')
    cosine_sim = joblib.load('cosine_sim.pkl')
    logging.info("✅ Data loaded successfully.")
except Exception as e:
    logging.error("❌ Failed to load required files: %s", str(e))
    raise e


def recommend_movies(movie_name, top_n=5):
    logging.info("🎬 Recommending movies for: '%s'", movie_name)
    idx = df[df['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        logging.warning("⚠️ Movie not found in dataset.")
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    logging.info("✅ Top %d recommendations ready.", top_n)
    # Create DataFrame with clean serial numbers starting from 1
    result_df = df[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1  # Start from 1 instead of 0
    result_df.index.name = "S.No."

    return result_df
