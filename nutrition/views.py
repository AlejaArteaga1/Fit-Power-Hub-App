from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json

from .models import MealPlan
from .forms import MealPlanForm
from .calculators import calculate_bmr, calculate_tdee, calculate_target_calories

@login_required
def meal_planner_view(request):
    """Meal planner main view"""
    meal_plans = MealPlan.objects.filter(user=request.user, is_active=True)
    
    context = {
        'meal_plans': meal_plans
    }
    return render(request, 'nutrition/meal_planner.html', context)

@login_required
def calculate_macros_view(request):
    """Calculate macros API endpoint"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            age = int(data.get('age', 25))
            weight = float(data.get('weight', 70))
            height = float(data.get('height', 170))
            activity_level = float(data.get('activity_level', 1.375))
            goal = data.get('goal', 'MT')
            gender = data.get('gender', 'M')
            
            # Calculate everything
            bmr = calculate_bmr(age, weight, height, gender)
            tdee = calculate_tdee(bmr, activity_level)
            target_calories = calculate_target_calories(tdee, goal)
            
            # Macronutrient distribution based on goal
            if goal == 'WL':  # Weight loss
                protein_ratio = 0.35
                carbs_ratio = 0.35
                fat_ratio = 0.30
            elif goal == 'MG':  # Muscle gain
                protein_ratio = 0.40
                carbs_ratio = 0.40
                fat_ratio = 0.20
            else:  # Maintenance
                protein_ratio = 0.30
                carbs_ratio = 0.40
                fat_ratio = 0.30
            
            protein_grams = round((target_calories * protein_ratio) / 4, 1)
            carbs_grams = round((target_calories * carbs_ratio) / 4, 1)
            fat_grams = round((target_calories * fat_ratio) / 9, 1)
            
            return JsonResponse({
                'success': True,
                'bmr': round(bmr),
                'tdee': round(tdee),
                'target_calories': round(target_calories),
                'protein_grams': protein_grams,
                'carbs_grams': carbs_grams,
                'fat_grams': fat_grams,
                'protein_ratio': protein_ratio,
                'carbs_ratio': carbs_ratio,
                'fat_ratio': fat_ratio,
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required
def create_meal_plan_view(request):
    """Create a new meal plan"""
    if request.method == 'POST':
        form = MealPlanForm(request.POST)
        if form.is_valid():
            meal_plan = form.save(commit=False)
            meal_plan.user = request.user
            
            # Calculate nutritional values
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            activity_level = form.cleaned_data['activity_level']
            goal = form.cleaned_data['goal']
            
            # Get gender from user profile if available
            try:
                gender = request.user.profile.gender or 'M'
            except:
                gender = 'M'
            
            # Perform calculations
            bmr = calculate_bmr(age, weight, height, gender)
            tdee = calculate_tdee(bmr, activity_level)
            target_calories = calculate_target_calories(tdee, goal)
            
            # Set calculated values
            meal_plan.bmr = bmr
            meal_plan.tdee = tdee
            meal_plan.target_calories = target_calories
            
            meal_plan.save()
            
            messages.success(request, 'Meal plan created successfully!')
            return redirect('meal_planner')
    else:
        form = MealPlanForm()
    
    context = {'form': form}
    return render(request, 'nutrition/create_meal_plan.html', context)

@login_required
def meal_plan_detail_view(request, plan_id):
    """View meal plan details"""
    meal_plan = get_object_or_404(MealPlan, id=plan_id, user=request.user)
    
    # Calculate macros for display
    macros = meal_plan.calculate_macros()
    
    context = {
        'meal_plan': meal_plan,
        'macros': macros,
    }
    
    return render(request, 'nutrition/meal_plan_detail.html', context)