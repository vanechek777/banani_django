from .models import *
from django.shortcuts import render
from django.http import HttpResponse
import templates
from django.conf import settings
from django_telegram_login.authentication import verify_telegram_authentication
from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError

from django_telegram_login.widgets.constants import LARGE
from django_telegram_login.widgets.generator import create_redirect_login_widget
from django.views.decorators.csrf import csrf_protect


def index(request):
    all_users = User.objects.all()
    all_ids = []
    for i in all_users:
        all_ids.append(i.user_tg_id)

    if request.COOKIES.get('user_id'):
        id = request.COOKIES.get('user_id')
        user_data = all_users.get(user_tg_id=id)
        photo = user_data.user_picture
        name = user_data.user_name

        context = {
            'user_name': name,
            'user_pic': photo,
        }
        return render(request, 'index.html', context)

    else:
        telegram_log_w = create_redirect_login_widget('user', settings.TELEGRAM_BOT_NAME, LARGE)
        tel_widg = telegram_log_w
        context = {'tel_widg': tel_widg}
        return render(request, 'index_unauth.html', context)


def user(request):
    print('got it!')
    if not request.GET.get('hash'):
        return HttpResponse('Handle the missing Telegram data in the response.')

    try:
        result = verify_telegram_authentication(
            bot_token=settings.TELEGRAM_BOT_TOKEN, request_data=request.GET
        )

    except TelegramDataIsOutdatedError:
        return HttpResponse('Authentication was received more than a day ago.')

    except NotTelegramDataError:
        return HttpResponse('The data is not related to Telegram!')

    user_id = result['id']
    user_name = result['first_name']
    user_pic = result['photo_url']

    all_users = User.objects.all()
    all_ids = []
    for i in all_users:
        all_ids.append(i.user_tg_id)

    if int(user_id) not in all_ids:
        User.objects.create(user_tg_id=user_id, user_picture=user_pic, user_name=user_name, total_points=0)
    else:
        pass

    context = {
        'user_name': user_name,
        'user_pic': user_pic,
    }

    r = render(request, 'index.html', context)
    r.set_cookie('user_id', user_id)
    return r


def play(request):
    all_users = User.objects.all()
    all_ids = []
    for i in all_users:
        all_ids.append(i.user_tg_id)

    if request.COOKIES.get('user_id'):
        id = request.COOKIES.get('user_id')
        user_data = all_users.get(user_tg_id=id)
        photo = user_data.user_picture
        name = user_data.user_name
        total = user_data.total_points
        coins_per_sec = user_data.coins_per_sec
        level = user_data.lvl
        till_next = user_data.till_next_level
        bar_percent_ = str(-(100 - (total / till_next * 100)))
        bar_percent = bar_percent_.replace(',', '.')

        if request.method == 'POST':
            if request.headers.get('click') == '1':
                if user_data.total_points != till_next:
                    user_data.total_points += 1
                else:
                    user_data.total_points += 1
                    user_data.lvl += 1
                    user_data.till_next_level = user_data.till_next_level * 3 + user_data.till_next_level
                user_data.save()
            else:
                print('Warn -> Else data')
            if request.headers.get('skill'):
                skill_num = request.headers.get()


        sorted_db = User.objects.order_by("total_points")
        sort_list = []
        for i in sorted_db:
            sort_list.append(i.user_tg_id)
        sort_list.reverse()

        context = {
            'user_name': name,
            'user_pic': photo,
            'per_sec': coins_per_sec,
            'total': total,
            'lvl': level,
            'till_next': till_next,
            'top': sort_list.index(user_data.user_tg_id) + 1,
            'prog_bar': bar_percent,
        }

        return render(request, 'mainfolder.html', context)
    else:
        telegram_log_w = create_redirect_login_widget('user', settings.TELEGRAM_BOT_NAME, LARGE)
        tel_widg = telegram_log_w
        context = {'tel_widg': tel_widg}
        return render(request, 'index_unauth.html', context)


def about(request):
    return render(request, 'about_us.html', context='')


def how_to(request):
    pass
