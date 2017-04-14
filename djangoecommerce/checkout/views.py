from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView, TemplateView
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from catalog.models import Product

from .models import CartItem


class CreateCartItemView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # Resgata produto atraves da url parametrizada.
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        # Cria objeto com atributo session_key e slug do produto
        cart_item, created = CartItem.objects.add_item(
            self.request.session.session_key, product
        )
        if created:
            messages.success(self.request, 'Produto adicionado com sucesso')
        else:
            messages.success(self.request, 'Produto atualizado com sucesso')
        return reverse_lazy('checkout:cart_item')


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'


    def get_formset(self, clear=False):
        CartItemFormSet = modelformset_factory(CartItem, fields=('quantity',),
                                               can_delete=True, extra=0)
        session_key = self.request.session.session_key
        if session_key:
            if clear:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key))
            else:
                formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    data=self.request.POST or None
                )
        else:
            formset = CartItemFormSet(queryset=CartItem.objects.none())
        return formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        context['formset'] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset()
        context = self.get_context_data(**kwargs)
        if formset.is_valid():
            formset.save()  # Busca todos os forms validos com os dados atuais e salva o objeto
            messages.success(request, 'Carrinhjo atualizado com sucesso')
            context['formset'] = self.get_formset(clear=True)
        return self.render_to_response(context)


class CheckoutView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'

    def get(self, request, *args, **kwargs):
        """Renderiza o template.

        Altera o funcionamento natural, e depois chama o comportamento natural.
        """
        session_key = request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(
                user=request.user, cart_items=cart_items
            )
        else:
            messages.info(request, 'Nao ha itens no carrinho de compras')
            return redirect('checkout:cart_item')
        return super(CheckoutView, self).get(request, *args, **kwargs)


create_cartitem = CreateCartItemView.as_view()
cart_item = CartItemView.as_view()
