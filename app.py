from flask import Flask, render_template, request, redirect, session
import pandas as pd
import joblib
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "fake_job_detector_secret_key"


# ==========================
# Load AI Model
# ==========================

model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# ==========================
# Create Users File
# ==========================

if not os.path.exists("users.csv"):

    users = pd.DataFrame(
        columns=[
            "username",
            "password"
        ]
    )

    users.to_csv(
        "users.csv",
        index=False
    )


# ==========================
# Create Verification History
# ==========================

if not os.path.exists("verification_history.csv"):

    history = pd.DataFrame(
        columns=[
            "Username",
            "Company",
            "Email",
            "Website",
            "Prediction",
            "Trust Score"
        ]
    )

    history.to_csv(
        "verification_history.csv",
        index=False
    )


# ==========================
# Home Page
# ==========================

@app.route("/")
def home():

    if "username" not in session:
        return redirect("/login")

    return redirect("/dashboard")
    # ==========================
# Register
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        users = pd.read_csv("users.csv")

        # Check if username already exists
        if username in users["username"].values:
            return render_template(
                "register.html",
                message="Username already exists!"
            )

        new_user = pd.DataFrame({
            "username": [username],
            "password": [password]
        })

        users = pd.concat(
            [users, new_user],
            ignore_index=True
        )

        users.to_csv(
            "users.csv",
            index=False
        )

        return redirect("/login")

    return render_template("register.html")


# ==========================
# Login
# ==========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        users = pd.read_csv("users.csv")

        user = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]

        if not user.empty:

            session["username"] = username

            return redirect("/dashboard")

        else:

            return render_template(
                "login.html",
                message="Invalid Username or Password"
            )

    return render_template("login.html")


# ==========================
# Logout
# ==========================

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/login")
# ==========================
# Dashboard
# ==========================

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    if "username" not in session:
        return redirect("/login")

    result = ""
    reason = ""
    score = 0
    ai_result = ""

    if request.method == "POST":

        company = request.form["company"].strip()
        email = request.form["email"].strip()
        website = request.form["website"].strip()
        job_offer = request.form["job_offer"].strip()


        # ==========================
        # AI Prediction
        # ==========================

        job_vector = vectorizer.transform([job_offer])

        prediction = model.predict(job_vector)

        if prediction[0] == 1:

            ai_result = "❌ Fake Job"

            score += 40

        else:

            ai_result = "✅ Real Job"



        # ==========================
        # Company Verification
        # ==========================

        verified_companies = [

            "Google",
            "Microsoft",
            "Amazon",
            "Zoho",
            "Infosys",
            "TCS",
            "IBM",
            "Accenture",
            "Wipro",
            "Cognizant"

        ]


        company_verified = False

        for c in verified_companies:

            if c.lower() == company.lower():

                company_verified = True

                break


        if company_verified:

            result += "✅ Company Verified\n"

        else:

            result += "⚠️ Company Not Verified\n"

            score += 20



        # ==========================
        # Email Verification
        # ==========================

        if "@gmail.com" in email.lower() or \
           "@yahoo.com" in email.lower() or \
           "@outlook.com" in email.lower():

            result += "⚠️ Personal Email Used\n"

            score += 20

        else:

            result += "✅ Official Company Email\n"



        # ==========================
        # Website Verification
        # ==========================

        if website.startswith("https://"):

            result += "✅ Secure Website\n"

        else:

            result += "⚠️ Website Not Secure\n"

            score += 20



        # ==========================
        # Trust Score
        # ==========================

        trust_score = 100 - score

        reason = ai_result
        # ==========================
        # Save Verification History
        # ==========================

        history = pd.read_csv("verification_history.csv")

        new_record = pd.DataFrame({

            "Username": [session["username"]],
            "Company": [company],
            "Email": [email],
            "Website": [website],
            "Prediction": [ai_result],
            "Trust Score": [trust_score]

        })

        history = pd.concat(
            [history, new_record],
            ignore_index=True
        )

        history.to_csv(
            "verification_history.csv",
            index=False
        )



    return render_template(

        "index.html",

        username=session["username"],

        result=result,

        reason=reason,

        score=score,

        trust_score=trust_score if request.method == "POST" else "",

        ai_result=ai_result

    )


# ==========================
# Run Flask App
# ==========================

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))