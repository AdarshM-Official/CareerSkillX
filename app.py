from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "supersecret"  # Required for session

# Load dataset
df = pd.read_csv("dataset/career_guidance_dataset.csv")

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.form

    field = data.get("field")
    interests = data.get("interests")

    # Filter similar entries
    filtered_df = df[
        (df["Field_of_Study"].str.lower() == field.lower()) &
        (df["Career_Interests"].str.lower().str.contains(interests.lower()))
    ]

    if filtered_df.empty:
        top_career = "No match found"
        recommended_counts = {}
    else:
        recommended_counts = filtered_df["Recommended_Career_Path"].value_counts().to_dict()
        top_career = max(recommended_counts, key=recommended_counts.get)

    # Store data in session
    session["top_career"] = top_career
    session["scores"] = recommended_counts

    return redirect(url_for("result"))

@app.route("/result")
def result():
    return render_template("career.html", 
                           top_career=session.get("top_career", "N/A"), 
                           scores=session.get("scores", {}))

if __name__ == "__main__":
    app.run(debug=True)
