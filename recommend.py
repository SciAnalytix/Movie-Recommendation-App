import joblib
import requests
import io

# URLs of uploaded files on HuggingFace (Corrected)
DF_URL = "https://huggingface.co/datasets/SciAnalytix/Dataset/resolve/main/df_cleaned.pkl"
COSINE_SIM_URL = "https://huggingface.co/datasets/SciAnalytix/Dataset/resolve/main/cosine_sim.pkl"

# Function to download and load joblib files
def download_joblib_file(url):
    response = requests.get(url)
    file_like_object = io.BytesIO(response.content)
    return joblib.load(file_like_object)

# Load data
df = download_joblib_file(DF_URL)
cosine_sim = download_joblib_file(COSINE_SIM_URL)

def recommend_movies(movie_name, top_n=5):
    idx = df[df['title'].str.lower() == movie_name.lower()].index
    if len(idx) == 0:
        return None
    idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]
    result_df = df[['title']].iloc[movie_indices].reset_index(drop=True)
    result_df.index = result_df.index + 1
    result_df.index.name = "S.No."
    return result_df
