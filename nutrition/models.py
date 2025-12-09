from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class MealPlan(models.Model):
    WEIGHT_LOSS = 'WL'
    MUSCLE_GAIN = 'MG'
    MAINTENANCE = 'MT'
    ENDURANCE = 'EN'
    
    GOAL_CHOICES = [
        (WEIGHT_LOSS, 'Weight Loss'),
        (MUSCLE_GAIN, 'Muscle Gain'),
        (MAINTENANCE, 'Maintenance'),
        (ENDURANCE, 'Endurance'),
    ]
    
    SEDENTARY = 1.2
    LIGHT = 1.375
    MODERATE = 1.55
    ACTIVE = 1.725
    VERY_ACTIVE = 1.9
    
    ACTIVITY_CHOICES = [
        (SEDENTARY, 'Sedentary (little or no exercise)'),
        (LIGHT, 'Light (exercise 1-3 days/week)'),
        (MODERATE, 'Moderate (exercise 3-5 days/week)'),
        (ACTIVE, 'Active (exercise 6-7 days/week)'),
        (VERY_ACTIVE, 'Very active (hard exercise daily)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    name = models.CharField(max_length=100)
    goal = models.CharField(max_length=2, choices=GOAL_CHOICES)
    activity_level = models.FloatField(choices=ACTIVITY_CHOICES)
    
    # User stats
    age = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])
    weight = models.FloatField(help_text="Weight in kg", validators=[MinValueValidator(30), MaxValueValidator(300)])
    height = models.FloatField(help_text="Height in cm", validators=[MinValueValidator(100), MaxValueValidator(250)])
    
    # Calculated values
    bmr = models.FloatField(blank=True, null=True, help_text="Basal Metabolic Rate")
    tdee = models.FloatField(blank=True, null=True, help_text="Total Daily Energy Expenditure")
    target_calories = models.FloatField(blank=True, null=True)
    
    # Macronutrient ratios
    protein_ratio = models.FloatField(default=0.3, validators=[MinValueValidator(0.1), MaxValueValidator(0.6)])
    carbs_ratio = models.FloatField(default=0.4, validators=[MinValueValidator(0.1), MaxValueValidator(0.7)])
    fat_ratio = models.FloatField(default=0.3, validators=[MinValueValidator(0.1), MaxValueValidator(0.5)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
    
    def calculate_macros(self):
        """Calculate and return macronutrient breakdown"""
        if self.target_calories:
            protein_calories = self.target_calories * self.protein_ratio
            carbs_calories = self.target_calories * self.carbs_ratio
            fat_calories = self.target_calories * self.fat_ratio
            
            # Convert calories to grams (protein & carbs: 4 cal/g, fat: 9 cal/g)
            protein_grams = protein_calories / 4
            carbs_grams = carbs_calories / 4
            fat_grams = fat_calories / 9
            
            return {
                'protein': round(protein_grams, 1),
                'carbs': round(carbs_grams, 1),
                'fat': round(fat_grams, 1),
                'protein_calories': round(protein_calories),
                'carbs_calories': round(carbs_calories),
                'fat_calories': round(fat_calories),
            }
        return None