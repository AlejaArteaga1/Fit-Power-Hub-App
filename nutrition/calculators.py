def calculate_bmr(age, weight, height, gender='M'):
    """
    Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
    weight in kg, height in cm
    """
    if gender == 'F':  # Female
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:  # Male
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    
    return bmr

def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure
    """
    return bmr * activity_level

def calculate_target_calories(tdee, goal):
    """
    Calculate target calories based on fitness goal
    """
    if goal == 'WL':  # Weight loss (deficit of 500 calories)
        return tdee - 500
    elif goal == 'MG':  # Muscle gain (surplus of 300 calories)
        return tdee + 300
    else:  # Maintenance
        return tdee

def calculate_macronutrients(calories, protein_ratio=0.3, carbs_ratio=0.4, fat_ratio=0.3):
    """
    Calculate macronutrient grams from calories and ratios
    """
    # Validate ratios sum to 1
    total_ratio = protein_ratio + carbs_ratio + fat_ratio
    if abs(total_ratio - 1.0) > 0.01:
        # Normalize ratios
        protein_ratio /= total_ratio
        carbs_ratio /= total_ratio
        fat_ratio /= total_ratio
    
    # Calculate calories per macronutrient
    protein_calories = calories * protein_ratio
    carbs_calories = calories * carbs_ratio
    fat_calories = calories * fat_ratio
    
    # Convert to grams (protein & carbs: 4 cal/g, fat: 9 cal/g)
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