import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import boto3
from botocore.exceptions import ClientError

# ================= CONFIG =================
SOURCE_URL = "https://icanpathfinder.com/"
DOWNLOAD_DIR = "downloads"

YEAR_RANGE = range(2018, 2025)  # 2018–2024

SUPABASE_ENDPOINT = "https://fbjekiepmbsxknkhtzbj.storage.supabase.co/storage/v1/s3"
BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.getenv("SUPABASE_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("SUPABASE_SECRET_KEY")

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME]):
    raise RuntimeError("Missing Supabase credentials")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ================= S3 CLIENT =================
s3 = boto3.client(
    "s3",
    endpoint_url=SUPABASE_ENDPOINT,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def exists_in_bucket(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise

def extract_year(text):
    for y in YEAR_RANGE:
        if str(y) in text:
            return y
    return None

# ================= SCRAPE =================
print("🔍 Fetching ICAN Pathfinder homepage...")
resp = requests.get(SOURCE_URL, timeout=30)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
links = soup.find_all("a", href=True)

pdfs = []

for link in links:
    href = link["href"]
    text = link.get_text(" ", strip=True)

    if not href.lower().endswith(".pdf"):
        continue

    year = extract_year(href + " " + text)
    if not year:
        continue

    pdf_url = urljoin(SOURCE_URL, href)
    filename = os.path.basename(urlparse(pdf_url).path)

    pdfs.append({
        "url": pdf_url,
        "year": year,
        "filename": filename
    })

if not pdfs:
    raise RuntimeError("❌ No past question PDFs found")

print(f"📄 Found {len(pdfs)} past question PDFs")

# ================= PROCESS =================
for item in pdfs:
    pdf_url = item["url"]
    year = item["year"]
    filename = item["filename"]

    s3_key = f"past_questions/{year}/{filename}"

    if exists_in_bucket(BUCKET_NAME, s3_key):
        print(f"⏭️  Exists, skipped: {s3_key}")
        continue

    print(f"⬇️ Downloading: {filename}")
    r = requests.get(pdf_url, stream=True, timeout=60)
    r.raise_for_status()

    local_path = os.path.join(DOWNLOAD_DIR, filename)
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)

    print(f"☁️ Uploading → {s3_key}")
    s3.upload_file(
        local_path,
        BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": "application/pdf"}
    )

print("\n✅ ICAN past questions successfully uploaded")
