import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# -----------------------------
# 🔹 EMBEDDING MODEL
# -----------------------------
embedding = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# -----------------------------
# 🔹 DB PATH (SAFE)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# -----------------------------
# 🔹 CREATE VECTOR DB
# -----------------------------
db = Chroma(
    collection_name="jobs_memory",
    embedding_function=embedding,
    persist_directory=DB_PATH
)

# -----------------------------
# 🔹 SAVE JOB
# -----------------------------
def save_job(job):

    try:
        text = f"{job['title']} at {job['company']}"

        db.add_texts(
            texts=[text],
            metadatas=[job]
        )

        db.persist()  # 🔥 important

    except Exception as e:
        print("Error saving job:", e)


# -----------------------------
# 🔹 CHECK SIMILAR JOB
# -----------------------------
def is_similar(job):

    try:
        query = f"{job['title']} {job['company']}"

        results = db.similarity_search_with_score(query, k=1)

        if results:
            doc, score = results[0]

            print("🔍 Similarity score:", score)

            # 🔥 Tune threshold
            if score < 0.7:
                return True

        return False

    except Exception as e:
        print("Similarity check error:", e)
        return False


# -----------------------------
# 🔹 GET SIMILAR JOBS (OPTIONAL)
# -----------------------------
def get_similar_jobs(job):

    try:
        query = f"{job['title']} {job['company']}"

        results = db.similarity_search(query, k=3)

        return results

    except Exception as e:
        print("Error fetching similar jobs:", e)
        return []