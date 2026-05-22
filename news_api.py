# news_api.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv(
    "NEWS_API_KEY"
)


def get_food_news():

    query = (
        "(healthy food OR nutrition OR "
        "wellness OR food safety OR low sugar)"
    )

    url = (
        "https://newsapi.org/v2/everything?"
        f"q={query}"
        "&language=en"
        "&sortBy=publishedAt"
        "&pageSize=12"
        "&domains="
        "healthline.com,"
        "medicalnewstoday.com,"
        "eatingwell.com"
        f"&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    articles = []

    for article in data.get(
        "articles",
        []
    ):

        articles.append({

            "title":
                article.get("title"),

            "description":
                article.get("description"),

            "url":
                article.get("url"),

            "image":
                article.get("urlToImage"),

            "source":
                article.get(
                    "source",
                    {}
                ).get(
                    "name"
                ),

            "published_at":
                article.get(
                    "publishedAt"
                )
        })

    return {
        "articles": articles
    }
