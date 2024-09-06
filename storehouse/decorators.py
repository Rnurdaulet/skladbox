from django.contrib.auth.decorators import user_passes_test


def is_storehouse(user):
    return user.groups.filter(name='Склад').exists()


def storehouse_required(view_func):
    decorated_view_func = user_passes_test(is_storehouse, login_url='/login/')(view_func)
    return decorated_view_func


def is_mover(user):
    return user.groups.filter(name='Грузчик').exists()


def mover_required(view_func):
    decorated_view_func = user_passes_test(is_mover, login_url='/login/')(view_func)
    return decorated_view_func
