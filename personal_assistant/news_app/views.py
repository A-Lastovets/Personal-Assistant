from django.shortcuts import render
from django.views.generic import View
from datetime import datetime
from newsapi import NewsApiClient
import requests

class ExchangeRateView(View):
    def get_exchange_rates(self):
        api_key_to_exchange_rate = 'c5733a77747980d8a23de9c56352963e'
        exchange_rate_url = (f'http://data.fixer.io/api/latest?access_key={api_key_to_exchange_rate}'
                             f'&symbols=USD,EUR,PLN,UAH')

        try:
            response = requests.get(exchange_rate_url)
            response.raise_for_status()
            currency_data = response.json()

            # Проверка наличия ключа 'rates' в ответе
            if 'rates' in currency_data:
                usd_to_uah = round(
                    currency_data['rates']['UAH'] / currency_data['rates']['USD'], 2)
                eur_to_uah = round(
                    currency_data['rates']['UAH'] / currency_data['rates']['EUR'], 2)
                pln_to_uah = round(
                    currency_data['rates']['UAH'] / currency_data['rates']['PLN'], 2)

                return {
                    'usd_to_uah': usd_to_uah,
                    'eur_to_uah': eur_to_uah,
                    'pln_to_uah': pln_to_uah,
                }
            else:
                return {'error': 'Не удалось получить курсы валют. Попробуйте позже.'}

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            return {'error': 'Не удалось получить данные о курсах валют. Попробуйте позже.'}


class NewsView(View):
    def get_news(self):
        newsapi = NewsApiClient(api_key='435a219a6e2a412ebb8e1c5358571e6d')
        categories = ['business', 'entertainment', 'general',
                      'health', 'science', 'sports', 'technology']
        news_by_category = {}

        for category in categories:
            news_data = newsapi.get_top_headlines(category=category)

            articles = []
            for article in news_data.get('articles', []):
                # Перевірка на "[Removed]" у title, description та author
                if (article.get('title') == '[Removed]' or
                        article.get('description') == '[Removed]' or
                        (article.get('author') == '[Removed]' or not article.get('author'))):
                    continue  # Пропустити цю статтю, якщо є "[Removed]"

                published_at = article.get('publishedAt', None)
                if published_at:
                    date_object = datetime.fromisoformat(published_at[:-1])
                    formatted_date = date_object.strftime("%d %B %Y, %H:%M")
                else:
                    formatted_date = 'Unknown'

                # Збереження статті у список
                articles.append({
                    'title': article.get('title', 'No title available'),
                    'description': article.get('description', 'No description available'),
                    'url': article.get('url', '#'),
                    'published_at': formatted_date,
                    'author': article.get('author', 'Unknown'),
                })

            # Додаємо лише непорожні статті для даної категорії
            news_by_category[category] = articles

        return news_by_category


class ExchangeRateNewsView(View):
    template_name = 'news.html'

    def get(self, request):
        # Отримання даних з ExchangeRateView
        exchange_view = ExchangeRateView()
        exchange_data = exchange_view.get_exchange_rates()

        # Отримання даних з NewsView
        news_view = NewsView()
        news_data = news_view.get_news()

        # Комбінування обох результатів в один контекст
        context = {
            **exchange_data,  # Курс валют
            'news_by_category': news_data,  # Новини за категоріями
        }

        return render(request, self.template_name, context)
