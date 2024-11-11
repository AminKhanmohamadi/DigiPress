from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView

from products.models import Category, Product
from .models import Favorite


# Create your views here.

class Home_page(View):
    def get(self, request):
        products = Product.objects.select_related('sub_category' , 'category').all()[:5]
        products_cat = Product.objects.select_related('sub_category' , 'category').filter(category_id=1)[:10]
        categories = get_object_or_404(Category, id=1)
        context ={
            'products':products,
            'products_cat':products_cat,
            'categories':categories,

        }
        return render(request , 'pages/home_page.html' , context)





class HomePageView(View):
   def get(self , request):
       categories = Category.objects.prefetch_related('children').all()
       return render(request , 'pages/category_sort.html' , {'categories':categories}) 


   





class HeaderResponsive(TemplateView):
    template_name = 'pages/header_responsive.html'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # لیست همه دسته‌بندی‌ها را برای نمایش در صفحه اصلی
    #     context['categories'] = Category.objects.all()

    #     return context






@login_required
def add_to_favorite_view(request , product_id):

    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite.objects.filter(user=request.user,product=product_id)

    if not favorite.exists():
        favorite = Favorite.objects.create(user=request.user, product=product)
        favorite.save()
        messages.success(request, 'Favorite added')
    else:
        messages.error(request, 'Favorite already added')
        return redirect('product_detail' , product_id)


    return redirect('pages:favorite_products')




@login_required
def remove_favorite_view(request , product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite.objects.filter(product=product).first()

    if favorite:
        favorite.delete()

        messages.warning(request, 'Favorite has been removed from your favorite')
    else:
        messages.error(request, 'Favorite does not exist')

    return redirect('pages:favorite_products')





@login_required
def favorite_list_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')

    return render(request, 'pages/favorite_list.html', {'favorites':favorites})


@login_required
def len_favorites(request):
    favorites_count = Favorite.objects.all()
    context = {'favorites':favorites}

    return render(request, 'pages/header.html', context)




