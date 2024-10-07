from datetime import datetime
from django.views.generic import View
from django.shortcuts import render
from newsapi import NewsApiClient
import requests


class ExchangeRateAndNewsView(View):
    template_name = 'homepage.html'

    def get(self, request):
        api_key_to_exchange_rate = '7e7b84e97a8aca30f461303188fdf667'
        exchange_rate_url = (f'http://data.fixer.io/api/latest?access_key={api_key_to_exchange_rate}'
                             f'&symbols=USD,EUR,PLN,UAH')

        try:
            # Отримання курсів валют
            response = requests.get(exchange_rate_url)
            response.raise_for_status()
            currency_data = response.json()

            usd_to_uah = round(currency_data['rates']['UAH'] / currency_data['rates']['USD'], 2)
            eur_to_uah = round(currency_data['rates']['UAH'] / currency_data['rates']['EUR'], 2)
            pln_to_uah = round(currency_data['rates']['UAH'] / currency_data['rates']['PLN'], 2)

            # Ініціалізація NewsApiClient
            newsapi = NewsApiClient(api_key='b189317af9df4e1a8d0c052cbd4f1e32')

            # Список категорій новин
            categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
            news_by_category = {}

            # Отримання новин для кожної категорії
            for category in categories:
                news_data = newsapi.get_top_headlines(category=category)

                articles = []
                for article in news_data.get('articles', [])[:3]:  # Отримати перші 3 новини
                    published_at = article['publishedAt']
                    date_object = datetime.fromisoformat(published_at[:-1])
                    formatted_date = date_object.strftime("%d %B %Y, %H:%M")

                    articles.append({
                        'title': article['title'],
                        'description': article['description'],
                        'url': article['url'],
                        'published_at': formatted_date,
                        'author': article.get('author', 'Unknown'),
                    })

                news_by_category[category] = articles  # Додаємо новини в словник за категорією

            context = {
                'usd_to_uah': usd_to_uah,
                'eur_to_uah': eur_to_uah,
                'pln_to_uah': pln_to_uah,
                'news_by_category': news_by_category,  # Передаємо новини по категоріях
                'error': None,
            }
            return render(request, self.template_name, context)

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            return render(request, self.template_name,
                          {'error': 'Failed to get data. Try again later.', 'articles': []})
