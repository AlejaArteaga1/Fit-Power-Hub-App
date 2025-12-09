from django import forms
from .models import MealPlan

class MealPlanForm(forms.ModelForm):
    class Meta:
        model = MealPlan
        fields = [
            'name', 'goal', 'activity_level', 
            'age', 'weight', 'height',
            'protein_ratio', 'carbs_ratio', 'fat_ratio'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., Muscle Gain Plan'
            }),
            'goal': forms.Select(attrs={'class': 'form-select'}),
            'activity_level': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': 10, 'max': 100}),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'E.g., 70.5'
            }),
            'height': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'E.g., 175.0'
            }),
            'protein_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.1',
                'max': '0.6'
            }),
            'carbs_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.1',
                'max': '0.7'
            }),
            'fat_ratio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.1',
                'max': '0.5'
            }),
        }
        labels = {
            'weight': 'Weight (kg)',
            'height': 'Height (cm)',
            'protein_ratio': 'Protein Ratio',
            'carbs_ratio': 'Carbs Ratio',
            'fat_ratio': 'Fat Ratio',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that ratios sum to approximately 1
        protein_ratio = cleaned_data.get('protein_ratio', 0)
        carbs_ratio = cleaned_data.get('carbs_ratio', 0)
        fat_ratio = cleaned_data.get('fat_ratio', 0)
        
        total = protein_ratio + carbs_ratio + fat_ratio
        
        if abs(total - 1.0) > 0.01:
            raise forms.ValidationError(
                f"Ratios must sum to 1.0 (current: {total:.2f}). "
                f"Adjust values so protein ({protein_ratio:.2f}) + "
                f"carbs ({carbs_ratio:.2f}) + fat ({fat_ratio:.2f}) = 1.0"
            )
        
        # Validate age, weight, height
        age = cleaned_data.get('age')
        if age and (age < 10 or age > 100):
            raise forms.ValidationError("Age must be between 10 and 100 years")
        
        weight = cleaned_data.get('weight')
        if weight and (weight < 30 or weight > 300):
            raise forms.ValidationError("Weight must be between 30 and 300 kg")
        
        height = cleaned_data.get('height')
        if height and (height < 100 or height > 250):
            raise forms.ValidationError("Height must be between 100 and 250 cm")
        
        return cleaned_data