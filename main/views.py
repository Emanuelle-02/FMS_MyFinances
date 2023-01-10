import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import *
from django.contrib import messages
from .forms import CategoriaForm, DespesasEditForm, DespesasForm, GanhoForm
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Sum
import xlwt
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class index(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        despesas = Despesas.objects.filter(user=request.user)
        ganhos = Ganho.objects.filter(user=request.user)
        total_despesas = 0
        total_ganhos = 0
        saldo = 0

        for despesa in despesas:
            total_despesas += despesa.valor
        for ganho in ganhos:
            total_ganhos += ganho.valor

        saldo = total_ganhos - total_despesas

        context = {
            "despesas": despesas,
            "ganhos": ganhos,
            "total_despesas": total_despesas,
            "total_ganhos": total_ganhos,
            "saldo": saldo,
        }

        return render(request, "despesas/index.html", context)


class CreateDespesaView(LoginRequiredMixin, CreateView):
    login_url = "/auth/login"
    model = Despesas
    form_class = DespesasForm
    template_name = "despesas/despesa_form.html"

    def get_form_kwargs(self):
        kwargs = super(CreateDespesaView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("minhas_despesas")


class ListarDespesasView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        despesas = Despesas.objects.filter(user=request.user)
        ganhos = Ganho.objects.filter(user=request.user)
        total_despesas = 0
        total_ganhos = 0
        saldo = 0

        for despesa in despesas:
            total_despesas += despesa.valor
        for ganho in ganhos:
            total_ganhos += ganho.valor

        saldo = total_ganhos - total_despesas
        paginator = Paginator(despesas, 5)
        pagina_num = request.GET.get("page")
        obj_pagina = Paginator.get_page(paginator, pagina_num)
        context = {
            "despesas": despesas,
            "ganhos": ganhos,
            "total_despesas": total_despesas,
            "total_ganhos": total_ganhos,
            "saldo": saldo,
            "obj_pagina": obj_pagina,
        }
        return render(request, "despesas/minhas_despesas.html", context)


class DespesaEditView(LoginRequiredMixin, UpdateView):
    login_url = "/auth/login"
    model = Despesas
    form_class = DespesasEditForm
    template_name = "despesas/despesa_form.html"
    success_url = "/minhas_despesas"

    def get_form_kwargs(self):
        kwargs = super(DespesaEditView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


class DespesaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/auth/login"
    model = Despesas
    success_url = "/minhas_despesas"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ListCategoriasView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        categorias = Categoria.objects.filter(user=request.user)
        paginator = Paginator(categorias, 10)
        pagina_num = request.GET.get("page")
        obj_pagina = Paginator.get_page(paginator, pagina_num)
        context = {"categorias": categorias, "obj_pagina": obj_pagina}
        return render(request, "despesas/listagem_categorias.html", context)


class CategoriaCreateView(LoginRequiredMixin, CreateView):
    login_url = "/auth/login"
    model = Categoria
    form_class = CategoriaForm
    template_name = "despesas/categoria_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("listagem_categorias")


class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/auth/login"
    model = Categoria
    success_url = "/listagem_categorias"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ListGanhosView(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        rendas = Ganho.objects.filter(user=request.user)
        paginator = Paginator(rendas, 5)
        pagina_num = request.GET.get("page")
        obj_pagina = Paginator.get_page(paginator, pagina_num)
        rendas = Ganho.objects.filter(user=request.user)
        total_ganho = 0

        for renda in rendas:
            total_ganho += renda.valor

        context = {
            "rendas": rendas,
            "obj_pagina": obj_pagina,
            "rendas": rendas,
            "total_ganho": total_ganho,
        }
        return render(request, "rendas/listagem_renda.html", context)


class RendaCreateView(LoginRequiredMixin, CreateView):
    login_url = "/auth/login"
    model = Ganho
    form_class = GanhoForm
    template_name = "rendas/renda_form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect("listagem_renda")


class RendaEditView(LoginRequiredMixin, UpdateView):
    login_url = "/auth/login"
    model = Ganho
    form_class = GanhoForm
    template_name = "rendas/renda_form.html"
    success_url = "/listagem_renda"


class RendaDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "/auth/login"
    model = Ganho
    success_url = "/listagem_renda"

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


# Gera gráfico de gastos por categoria
class view_graph(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        labels = []
        data = []

        queryset = (
            Despesas.objects.values("categoria__nome")
            .annotate(categoria_valor=Sum("valor"))
            .order_by("-categoria_valor")
            .filter(user=request.user)
        )
        for entry in queryset:
            labels.append(entry["categoria__nome"])
            data.append(entry["categoria_valor"])

        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )


# Gera gráfico de renda por mês
class view_graph2(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        labels = []
        data = []

        queryset = (
            Ganho.objects.values("data__month")
            .annotate(ganho_valor=Sum("valor"))
            .order_by("data__month")
            .filter(user=request.user)
        )
        for entry in queryset:
            labels.append(entry["data__month"])
            data.append(entry["ganho_valor"])

        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )


class view_graph3(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        labels = []
        data = []

        queryset = (
            Ganho.objects.values("data__year")
            .annotate(ganho_valor=Sum("valor"))
            .order_by("data__year")
            .filter(user=request.user)
        )
        for entry in queryset:
            labels.append(entry["data__year"])
            data.append(entry["ganho_valor"])

        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )


class graph_despesas_mensal(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        labels = []
        data = []

        queryset = (
            Despesas.objects.values("data__month")
            .annotate(ganho_valor=Sum("valor"))
            .order_by("data__month")
            .filter(user=request.user)
        )
        for entry in queryset:
            labels.append(entry["data__month"])
            data.append(entry["ganho_valor"])

        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )


class graph_despesas_anual(LoginRequiredMixin, View):
    login_url = "/auth/login"

    def get(self, request):
        labels = []
        data = []

        queryset = (
            Despesas.objects.values("data__year")
            .annotate(ganho_valor=Sum("valor"))
            .order_by("data__year")
            .filter(user=request.user)
        )
        for entry in queryset:
            labels.append(entry["data__year"])
            data.append(entry["ganho_valor"])

        return JsonResponse(
            data={
                "labels": labels,
                "data": data,
            }
        )


# View gráficos de despesas
class GraphDespesasView(LoginRequiredMixin, ListView):
    login_url = "/auth/login"
    model = Despesas
    template_name = "despesas/estatistica.html"


class GraphRendaView(LoginRequiredMixin, ListView):
    login_url = "/auth/login"
    model = Ganho
    template_name = "rendas/estatistica_renda.html"


def exportar_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = (
        "attachment; filename=Despesas" + str(datetime.datetime.now()) + ".xls"
    )
    wb = xlwt.Workbook(encoding="UTF-8")
    ws = wb.add_sheet("Despesas")
    row_num = 0
    sum = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    cols = ["Descrição", "Categoria", "Valor", "Data"]

    for col_num in range(len(cols)):
        ws.write(row_num, col_num, cols[col_num], font_style)
    font_style = xlwt.XFStyle()

    rows = Despesas.objects.filter(user=request.user).values_list(
        "descricao", "categoria__nome", "valor", "data"
    )
    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response
