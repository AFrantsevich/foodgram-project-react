import tablib


from import_export import resources


from import_export.fields import Field


from .models import Cart, RecipeTable
from .scripts import delete_dub


class CartResource(resources.ModelResource):
    ingredient = Field(attribute='ingredient__name', column_name='Продукт')
    amount = Field(attribute='amount', column_name='Количество')
    measurement_unit = Field(
        attribute='ingredient__measurement_unit', column_name='Ед.изм')

    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user

    class Meta:
        model = RecipeTable
        fields = ('ingredient', 'amount', 'measurement_unit')
        export_order = ('ingredient', 'amount', 'measurement_unit',)

    def export(self, queryset=None, *args, **kwargs):
        cart_filt = Cart.objects.filter(user=self.user)
        cart_list = []
        for i in cart_filt:
            odj = RecipeTable.objects.get(recipe_id=i.recipe_id)
            cart_list.append(odj)
        ricipe_list = []
        i = 0
        for b in cart_list:
            ricipe_list.append([])
            ricipe_list[i].append(b.ingredient.name)
            ricipe_list[i].append(b.amount)
            ricipe_list[i].append(b.ingredient.measurement_unit)
            i += 1
        ing_list = delete_dub(ricipe_list)
        headers = self.get_export_headers()
        data = tablib.Dataset(headers=headers)
        for obj in ing_list:
            data.append(obj)
        return data
