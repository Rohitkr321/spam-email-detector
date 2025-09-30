# Spam Email Detection AI Agent

## Overview
This project is an **AI-powered email spam detection agent**. It connects to a Gmail inbox, fetches unread emails, predicts whether each email is **spam or ham** using a **Naive Bayes classifier** with **TF-IDF features**, and saves predicted spam emails into a CSV file for further retraining.

---

## Features
- Connects securely to Gmail via **IMAP**.
- Fetches **unread emails**.
- Cleans and preprocesses email text:
  - Removes HTML tags
  - Removes URLs
  - Removes special characters
  - Converts text to lowercase
- Predicts spam using a **Naive Bayes + TF-IDF** model.
- Saves predicted spam emails to `collected_spam.csv` with:
  - Sender email
  - Subject
  - Body
  - Timestamp
  - Manual review flag
- Avoids duplicates using a **fingerprint hash**.

---

## Libraries Used

| Library | Purpose |
|---------|---------|
| `imapclient` | Connect to IMAP email servers (Gmail). |
| `pyzmail` | Parse raw email messages (subject, sender, text/HTML). |
| `pandas` | Read/write CSV files and manage data. |
| `re` | Clean email text using regular expressions. |
| `hashlib` | Generate unique fingerprint for each email. |
| `datetime` | Add timestamps for collected spam emails. |
| `sklearn.feature_extraction.text.TfidfVectorizer` | Convert email text into numerical vectors for ML. |
| `sklearn.naive_bayes.MultinomialNB` | Naive Bayes classifier to predict spam/ham. |

---

## Project Structure

           ┌───────────────────────────┐
           │      Start Script          │
           └─────────────┬────────────┘
                         │
                         ▼
           ┌───────────────────────────┐
           │ Connect to Gmail via IMAP │
           └─────────────┬────────────┘
                         │
                         ▼
           ┌───────────────────────────┐
           │ Fetch Unread Emails       │
           │ (UNSEEN)                  │
           └─────────────┬────────────┘
                         │
                         ▼
           ┌───────────────────────────┐
           │ Extract Email Details:    │
           │ - From                     │
           │ - Subject                  │
           │ - Body (text or HTML)      │
           └─────────────┬────────────┘
                         │
                         ▼
           ┌───────────────────────────┐
           │ Clean Email Text          │
           │ - Remove HTML tags        │
           │ - Remove URLs             │
           │ - Remove special chars    │
           │ - Lowercase text          │
           └─────────────┬────────────┘
                         │
                         ▼
           ┌───────────────────────────┐
           │ Generate Fingerprint      │
           │ (SHA1 of from+subject+snippet) │
           └─────────────┬────────────┘
                         │
                         ▼
           ┌───────────────────────────┐
           │ Check if Email Already     │
           │ Exists in CSV (duplicate) │
           └─────────────┬────────────┘
                         │
             ┌───────────┴─────────────┐
             │                         │
             ▼                         ▼
       Already Saved                Not Saved
             │                         │
             │                         ▼
             │               ┌───────────────────────────┐
             │               │ Predict Spam or Ham        │
             │               │ (Naive Bayes + TF-IDF)    │
             │               └─────────────┬────────────┘
             │                             │
             ▼                             ▼
       Skip Email                   Is Spam?
                                       │
                    ┌──────────────────┴─────────────┐
                    │                                │
                   Yes                               No
                    │                                │
           ┌───────────────────┐                ┌─────────┐
           │ Save Email to CSV │                │ Skip    │
           │ collected_spam.csv│                │ Email   │
           │ reviewed = "no"   │                └─────────┘
           └───────────────────┘
                    │
                    ▼
           ┌───────────────────┐
           │ Repeat for All    │
           │ Unread Emails     │
           └─────────────┬─────┘
                         ▼
           ┌───────────────────┐
           │ Logout from Gmail │
           └─────────────┬─────┘
                         ▼
           ┌───────────────────┐
           │ End Script        │
           └───────────────────┘
