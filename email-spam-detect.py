# email-spam-detect-save-spam.py
import imapclient
import pyzmail
import re
import pandas as pd
import hashlib
import time
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# --------- load base model (or train quick model as you had) ----------
df = pd.read_csv("SMSSpamCollection", sep="\t", names=["label", "text"])
vectorizer = TfidfVectorizer(stop_words="english")
X = vectorizer.fit_transform(df["text"])
model = MultinomialNB()
model.fit(X, df["label"])

# --------- helper functions ----------
def clean_email(text):
    if not text:
        return ""
    text = re.sub(r'<.*?>', ' ', text)                 # remove HTML
    text = re.sub(r'http\S+|www.\S+', ' ', text)       # remove URLs
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)           # keep letters and spaces
    return text.lower().strip()

def finger_of(from_addr, subject, snippet):
    payload = (from_addr or "") + "|" + (subject or "") + "|" + (snippet or "")
    return hashlib.sha1(payload.encode('utf-8')).hexdigest()

def detect_spam(message):
    vec = vectorizer.transform([clean_email(message)])
    return model.predict(vec)[0]

# --------- CSV file where we collect predicted spam ----------
COLLECTED_FILE = "collected_spam.csv"

# ensure file exists with header
if not pd.io.common.file_exists(COLLECTED_FILE):
    df_empty = pd.DataFrame(columns=["fingerprint","from","subject","body","predicted","timestamp","reviewed"])
    df_empty.to_csv(COLLECTED_FILE, index=False)

# --------- connect to IMAP and fetch unseen emails ----------
EMAIL = "your@gmail.com"
PASSWORD = "gamil-app-password"  # use Gmail App Password for google security
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login(EMAIL, PASSWORD)
imapObj.select_folder('INBOX', readonly=True)

UIDs = imapObj.search(['UNSEEN'])
if not UIDs:
    print("No unseen emails.")
else:
    existing = pd.read_csv(COLLECTED_FILE)
    existing_fp = set(existing['fingerprint'].astype(str).tolist())

    for uid in UIDs:
        raw_message = imapObj.fetch([uid], ['BODY[]', 'FLAGS'])
        message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])

        subject = message.get_subject()
        from_addrs = message.get_addresses('from')
        from_str = from_addrs[0][1] if from_addrs and from_addrs[0][1] else str(from_addrs)
        if message.text_part:
            text = message.text_part.get_payload().decode(message.text_part.charset or 'utf-8', errors='ignore')
        elif message.html_part:
            text = message.html_part.get_payload().decode(message.html_part.charset or 'utf-8', errors='ignore')
        else:
            text = ""

        snippet = (text[:200]).replace("\n", " ").replace("\r", " ")
        fp = finger_of(from_str, subject, snippet)
        if fp in existing_fp:
            print("Already saved:", subject)
            continue

        label = detect_spam(text)
        if label == "spam":
            row = {
                "fingerprint": fp,
                "from": from_str,
                "subject": subject,
                "body": text,
                "predicted": label,
                "timestamp": datetime.utcnow().isoformat(),
                "reviewed": "no"
            }
            pd.DataFrame([row]).to_csv(COLLECTED_FILE, mode='a', header=False, index=False)
            print("Saved spam:", subject)
        else:
            print("Not spam:", subject)

imapObj.logout()
