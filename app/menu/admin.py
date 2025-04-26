from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from menu.models import Menu, MenuItem


class MenuItemForm(ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if menu := getattr(self.instance, 'menu', None):
            self.fields['parent'].queryset = MenuItem.objects.filter(menu=menu).exclude(id=self.instance.pk)
        else:
            self.fields['parent'].queryset = MenuItem.objects.none()


class MenuItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        id_to_parent = {}

        for form in self.forms:
            if form.cleaned_data.get('DELETE', False):
                continue

            instance = form.instance
            parent = form.cleaned_data.get('parent')

            instance_id = instance.pk or id(instance)
            parent_id = parent.pk or id(parent) if parent else None

            id_to_parent[instance_id] = parent_id

        for item_id in id_to_parent:
            visited = set()
            current_id = id_to_parent[item_id]

            while current_id:
                if current_id == item_id:
                    raise ValidationError('Circular reference detected')
                if current_id in visited:
                    break
                visited.add(current_id)
                current_id = id_to_parent.get(current_id)


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    form = MenuItemForm
    formset = MenuItemInlineFormSet
    extra = 0
    prepopulated_fields = {
        "slug": ("name",)
    }


class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]
    list_display = (
        'name',
    )


class MenuItemAdmin(admin.ModelAdmin):
    model = MenuItem
    form = MenuItemForm
    prepopulated_fields = {
        "slug": ("name",)
    }


admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
