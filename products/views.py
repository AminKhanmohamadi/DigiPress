from django.views.generic import ListView, DetailView

from products.models import Product, Category, SubCategory
from cart.forms import AddToCartProductForm

# Create your views here.

class AllProductListView(ListView):
    model = Product
    template_name = 'products/all_product.html'
    paginate_by = 2
    context_object_name = 'products'
    ordering = ['sub_category']






class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        slug = self.kwargs.get('slug')

        # ابتدا بررسی کنید که آیا slug مربوط به زیرمجموعه است
        try:
            sub_category = SubCategory.objects.get(slug=slug)
            # اگر زیرمجموعه پیدا شد، فیلتر محصولات بر اساس زیرمجموعه
            return  Product.objects.filter(sub_category=sub_category).distinct()
        except SubCategory.DoesNotExist:
            pass

        # سپس بررسی کنید که آیا slug مربوط به دسته‌بندی است
        try:
            category = Category.objects.get(slug=slug)
            # اگر دسته‌بندی پیدا شد، فیلتر محصولات بر اساس دسته‌بندی
            return  Product.objects.filter(category=category).distinct()
        except Category.DoesNotExist:
            # در صورت عدم یافتن هر کدام، تمام محصولات را برمی‌گرداند
            return Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context






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


