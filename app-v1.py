from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from urllib.parse import urlparse
import io

app = Flask(__name__)

latest_csv = None


def extract_site(url):
    try:
        if not str(url).startswith(("http://", "https://")):
            url = "https://" + str(url)

        domain = urlparse(url).netloc.lower()
        return domain.replace("www.", "").strip()

    except:
        return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():

    global latest_csv

    mapping_file = request.files["mapping"]
    articles_file = request.files["articles"]

    # ===== READ MAPPING =====
    mapping_df = pd.read_excel(mapping_file)
    mapping_df.columns = ["site", "company"]

    mapping_df["site"] = mapping_df["site"].str.lower().str.strip()
    mapping_df["company"] = mapping_df["company"].str.strip()

    site_company = dict(zip(mapping_df.site, mapping_df.company))

    # ===== READ ARTICLES =====
    articles_df = pd.read_excel(articles_file)
    articles_df.columns = ["url"]

    articles_df["site"] = articles_df["url"].apply(extract_site)

    # ===== SITE COUNT =====
    site_counts = articles_df["site"].value_counts().reset_index()
    site_counts.columns = ["site", "article_count"]

    # ===== MAP COMPANY =====
    site_counts["company"] = site_counts["site"].map(site_company)

    # capture missing BEFORE replacing
    missing = site_counts[site_counts["company"].isna()]["site"].tolist()

    # replace NaN with UNKNOWN (JSON safe + reporting safe)
    site_counts["company"] = site_counts["company"].fillna("UNKNOWN")

    # ===== COMPANY COUNT =====
    company_counts = (
        site_counts.groupby("company")["article_count"]
        .sum()
        .reset_index()
        .sort_values(by="article_count", ascending=False)
    )

    total_articles = int(site_counts["article_count"].sum())

    # ===== PREPARE CSV =====
    latest_csv = io.BytesIO()
    site_counts.to_csv(latest_csv, index=False)
    latest_csv.seek(0)

    # ===== JSON SAFE CONVERSION =====
    site_counts = site_counts.where(pd.notnull(site_counts), None)
    company_counts = company_counts.where(pd.notnull(company_counts), None)

    return jsonify({
        "site_table": site_counts.to_dict(orient="records"),
        "company_table": company_counts.to_dict(orient="records"),
        "total": total_articles,
        "missing": missing
    })


@app.route("/download")
def download():
    global latest_csv
    return send_file(
        latest_csv,
        as_attachment=True,
        download_name="site_report.csv",
        mimetype="text/csv"
    )


if __name__ == "__main__":
    app.run(debug=True)