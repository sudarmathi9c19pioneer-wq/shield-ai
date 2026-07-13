import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score


# Load Excel dataset
data = pd.read_excel(
    "dataset/fake_job_dataset.xlsx",
    sheet_name="Job Offers"
)


# Display first 5 rows
print(data.head())


# Keep only required columns
data = data[["Type", "Job Offer Text"]]


# Remove empty rows
data = data.dropna()


# Convert labels
# Real = 0
# Fake = 1

data["Type"] = data["Type"].map({
    "Real": 0,
    "Fake": 1
})


# Input and Output
X = data["Job Offer Text"]
y = data["Type"]


print("Dataset Loaded Successfully")
print("Total Records :", len(data))
# Split dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# Convert text into numerical features

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_train_vector = vectorizer.fit_transform(X_train)
X_test_vector = vectorizer.transform(X_test)


# Train Machine Learning Model

model = MultinomialNB()

model.fit(X_train_vector, y_train)


# Predict

prediction = model.predict(X_test_vector)


# Accuracy

accuracy = accuracy_score(y_test, prediction)

print("--------------------------------")
print("Model Training Completed")
print("Accuracy :", round(accuracy * 100, 2), "%")
print("--------------------------------")
# Save the trained model

joblib.dump(model, "model.pkl")

# Save the TF-IDF vectorizer

joblib.dump(vectorizer, "vectorizer.pkl")

print("Model saved as model.pkl")
print("Vectorizer saved as vectorizer.pkl")


# Test with a sample job offer

sample_job = [
    "Congratulations! Pay ₹5000 registration fee to get selected immediately. No interview required."
]

sample_vector = vectorizer.transform(sample_job)

prediction = model.predict(sample_vector)

if prediction[0] == 1:
    print("\nPrediction: FAKE JOB")
else:
    print("\nPrediction: REAL JOB")