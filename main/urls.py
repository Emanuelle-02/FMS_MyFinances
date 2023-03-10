from django.urls import path
from . import views

urlpatterns = [
    path("", views.index.as_view(), name="main"),
    path("minhas_despesas", views.ListarDespesasView.as_view(), name="minhas_despesas"),
    path("criar_despesa", views.CreateDespesaView.as_view(), name="despesa_form"),
    path(
        "editar_despesa/<int:pk>", views.DespesaEditView.as_view(), name="despesa_form"
    ),
    path(
        "delete_despesa/<int:pk>",
        views.DespesaDeleteView.as_view(),
        name="delete_despesa",
    ),
    path(
        "listagem_categorias",
        views.ListCategoriasView.as_view(),
        name="listagem_categorias",
    ),
    path("add_categoria", views.CategoriaCreateView.as_view(), name="categoria_form"),
    path(
        "delete_categoria/<int:pk>",
        views.CategoriaDeleteView.as_view(),
        name="delete_categoria",
    ),
    path("listagem_renda", views.ListGanhosView.as_view(), name="listagem_renda"),
    path("add_renda", views.RendaCreateView.as_view(), name="renda_form"),
    path("editar_renda/<int:pk>", views.RendaEditView.as_view(), name="renda_form"),
    path("delete_renda/<int:pk>", views.RendaDeleteView.as_view(), name="delete_renda"),
    path(
        "graph/", views.view_graph.as_view(), name="graph"
    ),  # gráfico por categoria de despesa
    path(
        "graph2/", views.view_graph2.as_view(), name="graph2"
    ),  # gráfico de renda por mês
    path(
        "graph3/", views.view_graph3.as_view(), name="graph3"
    ),  # gráfico de renda por ano
    path("exportar_excel", views.exportar_excel, name="exportar_excel"),
    path("estatistica", views.GraphDespesasView.as_view(), name="estatistica"),
    path("estatistica_renda", views.GraphRendaView.as_view(), name="estatistica_renda"),
    path(
        "graph_despesas_mensal",
        views.graph_despesas_mensal.as_view(),
        name="graph_despesas_mensal",
    ),
    path(
        "graph_despesas_anual",
        views.graph_despesas_anual.as_view(),
        name="graph_despesas_anual",
    ),
]
