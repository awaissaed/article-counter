# article-counter
Article Reporting Utility

The Article Reporting Utility is a web-based tool to analyze and report published articles across multiple websites and companies. It generates interactive company and site-level reports, lets you view detailed articles in a popup with pagination, highlights missing mappings, and allows exporting CSV reports.

Features
✅ Upload Excel files for website-to-company mapping and published articles
✅ Generate Company Report and Site Report
✅ Clickable details popup showing all articles per company or site
✅ Pagination for easy navigation of large datasets
✅ Highlight missing mappings
✅ Download CSV reports
✅ Automatic URL normalization (ensures https:// is prefixed)
✅ Total articles summary

The Article Reporting Utility is a web-based tool to analyze and report published articles across multiple websites and companies. It generates interactive company and site-level reports, lets you view detailed articles in a popup with pagination, highlights missing mappings, and allows exporting CSV reports.Installation
Clone this repository:
git clone https://github.com/your-username/article-reporting-utility.git
cd article-reporting-utility
Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Run the Flask app:
python app.py

The app will be available at: http://127.0.0.1:5000

Usage
Open the web app in your browser.
Upload your Website Mapping Excel (columns: site, company).
Upload your Articles Excel (column: url).
Click Process to generate reports.
View Company Report and Site Report.
Click View buttons to see detailed articles in a popup.
Use pagination if there are many articles.
Download the site report as CSV.
Excel File Format

Website Mapping Excel (2 columns):

site	company
lapzoocom.com	GuestifySolutions
totoking111com.com	LinkGuiders

Articles Excel (1 column):

url
https://lapzoocom.com/article-title

https://totoking111com.com/article-title


