from django.db import models


class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):  # Verifica se produto ja ta no
        #  carrinho, se ja estiver aumenta quantidade.
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
            cart_item.save()
        else:
            created = True
            cart_item = CartItem.objects.create(cart_key=cart_key,
                                                product=product,
                                                price=product.price)
        return cart_item, created


class CartItem(models.Model):

    cart_key = models.CharField('Chave do Carrinho', max_length=40,
                                db_index=True)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto')
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    price = models.DecimalField('Preco', decimal_places=2, max_digits=8)

    objects = CartItemManager()

    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        # Evita duplicidade de produtos no mesmo Carrinho.
        # Inves de ter 2 produtos tem 1 produto com quantidade 2.
        unique_together = (('cart_key', 'product'),)

    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity)


def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()


models.signals.post_save.connect(post_save_cart_item, sender=CartItem,
                                 dispatch_uid='post_save_cart_item')
