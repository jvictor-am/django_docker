# data_loader/admin.py
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import path
from django.urls import reverse
from .models import DataRecord, Product
from .management.commands.load_data import Command  # Import your load_data command


class DataRecordAdmin(admin.ModelAdmin):
    list_display = ('nome', 'idade', 'cep', 'endereco', 'uf', 'regiao')
    search_fields = ('nome', 'cep')
    list_filter = ('idade', 'uf', 'regiao')
    ordering = ('nome',)
    list_per_page = 10

    def cep_display(self, obj):
        return obj.cep
    cep_display.short_description = 'CEP'

    def endereco_display(self, obj):
        return obj.endereco or 'Não disponível'
    endereco_display.short_description = 'Endereço'

# Register the model with the custom admin interface
admin.site.register(DataRecord, DataRecordAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')  # Campos a serem exibidos na lista
    search_fields = ('name',)  # Campos pesquisáveis
    list_filter = ('stock',)  # Filtros disponíveis
    ordering = ('-created_at',)  # Ordenar por data de criação
    list_per_page = 10  # Itens por página

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('product-summary/', self.admin_site.admin_view(self.product_summary_view), name='product_summary'),
            path('product/<int:product_id>/', self.admin_site.admin_view(self.product_detail_view), name='product_detail'),
        ]
        return custom_urls + urls

    def product_summary_view(self, request):
        """Exibe um resumo dos produtos."""
        products = Product.objects.all()  # Busca todos os produtos
        total_products = products.count()
        total_value = sum(product.price * product.stock for product in products)  # Valor total em estoque
        
        context = {
            'products': products,
            'total_products': total_products,
            'total_value': total_value,
            'title': 'Resumo dos Produtos',
        }
        return render(request, 'admin/product_summary.html', context)

    def product_detail_view(self, request, product_id):
        """Exibe detalhes de um produto específico."""
        product = get_object_or_404(Product, id=product_id)  # Busca o produto pelo ID
        context = {
            'product': product,
        }
        return render(request, 'admin/product_detail.html', context)

# Registro do modelo Product com o admin customizado
admin.site.register(Product, ProductAdmin)