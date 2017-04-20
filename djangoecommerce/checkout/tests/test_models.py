from django.test import TestCase
from django.conf import settings
from model_mommy import mommy

from checkout.models import CartItem, Order


class CartItemTestCase(TestCase):

    def setUp(self):
        """Cria 3 objetos CartItem.

        A variavel _quantity eh a quantidade de objetos criados. NAO tem a Ver
        com o atributo quantity do modelo.
        """
        mommy.make(CartItem, _quantity=3)

    def test_post_save_cart_item(self):
        """Testa se quantity = 0 remove o item do carrinho.

        Seleciona o primeiro cart_item, criado pelo setup (3 no total),
        seta sua quantidade pra 0,deve ser apagado devido ao signal do models.
        Verifica se a quantidade restante de cart_item eh 2 (3 - 1 = 2).
        """
        cart_item = CartItem.objects.all()[0]
        cart_item.quantity = 0
        cart_item.save()
        self.assertEquals(CartItem.objects.count(), 2)


class OrderTestCase(TestCase):

    def setUp(self):
        self.cart_item = mommy.make(CartItem)
        self.user = mommy.make(settings.AUTH_USER_MODEL)

    def test_create_order(self):
        Order.objects.create_order(self.user, [self.cart_item])
        self.assertEquals(Order.objects.count(), 1)
        order = Order.objects.get()
        self.assertEquals(order.user, self.user)
        order_item = order.items.get()
        self.assertEquals(order_item.product, self.cart_item.product)
