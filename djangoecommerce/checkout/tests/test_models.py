from django.test import TestCase

from model_mommy import mommy

from checkout.models import CartItem

class CartItemTestCase(TestCase):

    def setUp(self):
        mommy.make(CartItem, _quantity=3)  # _quantity eh a quantidade de itens do modelo a serem gerados, nao eh a propriedade quantity do modelo.

    def test_post_save_cart_item(self):
        cart_item = CartItem.objects.all()[0]
        cart_item.quantity = 0
        cart_item.save()
        self.assertEquals(CartItem.objects.count(), 2)
