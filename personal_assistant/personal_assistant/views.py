from django.shortcuts import render
from news_app.views import ExchangeRateView, NewsView
from django.views import View


class HomePageView(View):
    template_name = 'home.html'

    def get(self, request):
        # Получаем данные о курсах валют
        exchange_view = ExchangeRateView()
        exchange_data = exchange_view.get_exchange_rates()

        # Получаем новости
        news_view = NewsView()
        news_data = news_view.get_news()

        # Собираем данные в контекст
        context = {
            **exchange_data,
            'news_by_category': news_data,
        }

        return render(request, self.template_name, context)
