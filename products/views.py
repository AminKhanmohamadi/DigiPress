from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.views.generic import ListView, DetailView

from django.db.models import Case, When, Value, DecimalField

from products.models import Product, Category, SubCategory
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

# Create your views here.

class AllProductListView(ListView):
    model = Product
    template_name = 'products/all_product.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', 'newest')  # دریافت پارامتر sort_by از GET
        products = Product.objects.all()

        # محاسبه قیمت نهایی با توجه به فیلدهای off_price و sell_price
        products = products.annotate(
            final_price=Case(
                When(off_price__isnull=False, then='off_price'),
                default='sell_price',
                output_field=DecimalField()  # استفاده از IntegerField
            )
        )

        # مرتب‌سازی محصولات بر اساس قیمت نهایی
        if sort_by == 'price_asc':
            products = products.order_by('final_price')
        elif sort_by == 'price_desc':
            products = products.order_by('-final_price')

        return products

    def render_to_response(self, context, **response_kwargs):
        # بررسی درخواست AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('products/partials/all_product_partial.html', context)
            return JsonResponse({'html': html})

        # در صورت نبود درخواست AJAX، صفحه کامل رندر شود
        return super().render_to_response(context, **response_kwargs)













class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        sort_by = self.request.GET.get('sort_by', 'newest')  # دریافت پارامتر sort_by از GET
        products = Product.objects.all()  # دریافت تمام محصولات

        # فیلتر بر اساس زیرمجموعه (SubCategory) اگر slug مربوط به زیرمجموعه باشد
        try:
            sub_category = SubCategory.objects.get(slug=slug)
            products = products.filter(sub_category=sub_category).distinct()
        except SubCategory.DoesNotExist:
            pass

        # فیلتر بر اساس دسته‌بندی (Category) اگر slug مربوط به دسته‌بندی باشد
        try:
            category = Category.objects.get(slug=slug)
            products = products.filter(category=category).distinct()
        except Category.DoesNotExist:
            pass

        # محاسبه قیمت نهایی با استفاده از Case و When
        products = products.annotate(
            final_price=Case(
                When(off_price__isnull=False, then='off_price'),
                default='sell_price',
                output_field=DecimalField()
            )
        )

        # مرتب‌سازی بر اساس پارامتر sort_by
        if sort_by == 'price_asc':
            products = products.order_by('final_price')
        elif sort_by == 'price_desc':
            products = products.order_by('-final_price')

        return products



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context

    def render_to_response(self, context, **response_kwargs):
        # بررسی درخواست AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('products/partials/product_partial.html', context)
            return JsonResponse({'html': html})

        # در صورت نبود درخواست AJAX، صفحه کامل رندر شود
        return super().render_to_response(context, **response_kwargs)




class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # محصولات مشابه بر اساس دسته‌بندی اصلی
        similar_products_by_category = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(id=product.id)

        # همچنین می‌توانید بر اساس زیرمجموعه نیز فیلتر کنید
        similar_products_by_subcategory = Product.objects.filter(
            sub_category=product.sub_category,
            is_active=True
        ).exclude(id=product.id)

        # افزودن محصولات مشابه به کانتکست
        context['similar_products'] = similar_products_by_category | similar_products_by_subcategory
        context['sub_category'] = product.sub_category

        return context



