from django.urls import path
from . import views

urlpatterns = [
    path('', views.meal_planner_view, name='meal_planner'),
    path('calculate/', views.calculate_macros_view, name='calculate_macros'),
    path('create/', views.create_meal_plan_view, name='create_meal_plan'),
    path('<int:plan_id>/', views.meal_plan_detail_view, name='meal_plan_detail'),
]