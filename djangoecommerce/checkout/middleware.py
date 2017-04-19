from .models import CartItem


def cart_item_middleware(get_response):
    """Atualiza session_key.

    Caso o usuario tenha montado um carrinho de compras antes de logar
    e ao logar sua session_key mudou pois o carrinho esta ligado a session_key
    verifica-se se isso ocorreu e atualiza o carrinho dps do user logar.
    """
    def middleware(request):
        session_key = request.session.session_key
        response = get_response(request)
        if session_key != request.session.session_key:
            CartItem.objects.filter(cart_key=session_key).update(
                cart_key=request.session.session_key
            )
        return response
    return middleware
