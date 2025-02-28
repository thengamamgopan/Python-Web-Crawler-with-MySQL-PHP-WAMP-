Web Scraper with MySQL & PHP Dashboard

This project consists of a Python web scraper that extracts news articles from a website, stores them in a MySQL database, and displays them using a PHP-based dashboard.
Features

✅ Scrapes news articles (headlines, summaries, links, sources, and dates)
✅ Stores data in MySQL
✅ Displays news dynamically with PHP
✅ Date filtering for easy search
✅ Dark mode toggle for better readability
✅ Print & PDF export
Installation & Setup
1. Install Required Software

    WAMP Server (for MySQL & PHP)
    Python 3.x

2. Install Python Dependencies

Run the following command:

pip install -r requirements.txt

3. Set Up MySQL Database

    Open phpMyAdmin (http://localhost/phpmyadmin)
    Create a database:

CREATE DATABASE news;

Create a table:

    CREATE TABLE NewsArticles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        headline VARCHAR(255),
        link TEXT,
        summary TEXT,
        source VARCHAR(100),
        scrape_date DATE
    );

Usage
Run the Web Scraper

Execute the Python script to scrape and store data:

python scraper.py

View News Dashboard

    Place fetch.php inside C:\wamp64\www\news\
    Start WAMP Server
    Open your browser and go to:

    http://localhost/news/fetch.php

Files Included

📌 scraper.py → Python script to scrape and store news
📌 fetch.php → PHP script to display news articles
📌 requirements.txt → List of required Python libraries
📌 README.md → Project documentation
Future Enhancements

✅ Search functionality
✅ Pagination for large datasets
✅ More data sources
