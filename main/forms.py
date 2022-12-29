from crum import get_current_user
from django.forms import ModelForm
from .models import Categoria, Despesas, Ganho
from django import forms


class DespesasForm(forms.ModelForm):
    class Meta:
        model = Despesas
        fields = ["descricao", "categoria", "valor", "data"]

        widgets = {
            "descricao": forms.Textarea(
                attrs={"class": "form-control", "type": "text"}
            ),
            "categoria": forms.Select(),
            "valor": forms.TextInput(attrs={"class": "form-control", "type": "text"}),
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(DespesasForm, self).__init__(*args, **kwargs)
        self.fields["categoria"].queryset = self.fields["categoria"].queryset.filter(
            user=request.user
        )


class DespesasEditForm(ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super(DespesasEditForm, self).__init__(*args, **kwargs)
        self.fields["categoria"].queryset = self.fields["categoria"].queryset.filter(
            user=request.user
        )
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Despesas
        fields = [
            "descricao",
            "categoria",
            "valor",
            "data",
        ]

        widgets = {
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }


class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Categoria
        fields = ["nome"]


class GanhoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GanhoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Ganho
        fields = ["descricao", "valor", "data"]

        widgets = {
            "data": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
        }
