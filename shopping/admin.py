""" Solution modified from https://ostack.cn/?qa=812883/&show=812884#a812884 """
from django.contrib import admin
from django.forms import models, widgets

from .models import ItemsOrder, Order


class CachingModelChoicesForm(models.ModelForm):
    """
    Gets cached choices from `CachingModelChoicesFormSet` and uses them in model
    choice fields in order to reduce number of DB queries when used in admin inlines.
    """

    @property
    def model_choice_fields(self):
        return [
            field_name
            for field_name, field in self.fields.items()
            if isinstance(field, (models.ModelChoiceField, models.ModelMultipleChoiceField))
        ]

    def __init__(self, *args, **kwargs):
        cached_choices: dict[str] = kwargs.pop("cached_choices", {})
        super().__init__(*args, **kwargs)
        for field_name, choices in cached_choices.items():
            if choices is not None and field_name in self.fields:
                self.fields[field_name].choices = choices


class CachingModelChoicesFormSet(models.BaseInlineFormSet):
    """
    Used to avoid duplicate DB queries by caching choices and passing them all the forms.
    To be used in conjunction with `CachingModelChoicesForm`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # django.forms.models.py/BaseModelFormSet._construct_form
        # django.forms.models.py/BaseInlineFormSet._construct_form
        sample_form: CachingModelChoicesForm = self._construct_form(0)
        self.cached_choices: dict[str] = {}
        try:
            model_choice_fields: list[str] = sample_form.model_choice_fields
        except AttributeError:
            pass
        else:
            for field_name in model_choice_fields:
                if field_name in sample_form.fields and not isinstance(
                    sample_form.fields[field_name].widget,
                    widgets.HiddenInput,
                ):
                    self.cached_choices[field_name] = [c for c in sample_form.fields[field_name].choices]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["cached_choices"] = self.cached_choices
        return kwargs


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    class ItemsOrderInline(admin.TabularInline):
        class ItemsOrderForm(CachingModelChoicesForm):
            model = ItemsOrder

        model = ItemsOrder
        form = ItemsOrderForm
        formset = CachingModelChoicesFormSet

    inlines = (ItemsOrderInline,)
