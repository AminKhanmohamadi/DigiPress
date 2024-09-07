
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, TemplateView

from products.models import Category, Product


# Create your views here.





class Home_page(View):
    def get(self, request):
        products = Product.objects.all()[:5]
        products_cat = Product.objects.filter(category_id=4)[:10]
        categories = get_object_or_404(Category, id=4)
        context ={
            'products':products,
            'products_cat':products_cat,
            'categories':categories,

        }
        return render(request , 'pages/home_page.html' , context)





class HomePageView(TemplateView):
    template_name = 'pages/category_sort.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # لیست همه دسته‌بندی‌ها را برای نمایش در صفحه اصلی
        context['categories'] = Category.objects.all()

        return context






class HeaderResponsive(TemplateView):
    template_name = 'pages/header_responsive.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # لیست همه دسته‌بندی‌ها را برای نمایش در صفحه اصلی
        context['categories'] = Category.objects.all()

        return context



