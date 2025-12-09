import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitfuelhub.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Product, Category, UserProfile
from nutrition.models import MealPlan

print("=== CREATING SAMPLE DATA ===")

# 1. Create superuser
print("\n1. Creating superuser...")
try:
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@fitfuelhub.com',
        password='admin123'
    )
    UserProfile.objects.create(user=admin)
    print("   ✓ Admin created: admin/admin123")
except:
    print("   ⚠ Admin already exists")

# 2. Create demo user
print("\n2. Creating demo user...")
try:
    demo = User.objects.create_user(
        username='demo',
        email='demo@fitfuelhub.com',
        password='demo123',
        first_name='Demo',
        last_name='User'
    )
    UserProfile.objects.create(
        user=demo,
        phone='+1234567890',
        address='123 Main Street, City',
        height=175.0,
        weight=70.0,
        fitness_goal='Build muscle'
    )
    print("   ✓ Demo user created: demo/demo123")
except:
    print("   ⚠ Demo user already exists")

# 3. Create categories
print("\n3. Creating categories...")
categories = [
    {'name': 'Proteins', 'slug': 'proteins', 'description': 'Protein supplements'},
    {'name': 'Creatine', 'slug': 'creatine', 'description': 'Creatine supplements'},
    {'name': 'Pre-Workout', 'slug': 'pre-workout', 'description': 'Pre-workout supplements'},
    {'name': 'Sportswear', 'slug': 'sportswear', 'description': 'Sports clothing'},
    {'name': 'Equipment', 'slug': 'equipment', 'description': 'Fitness equipment'},
    {'name': 'Healthy Food', 'slug': 'healthy-food', 'description': 'Healthy snacks and food'},
]

for cat_data in categories:
    cat, created = Category.objects.get_or_create(
        slug=cat_data['slug'],
        defaults={'name': cat_data['name'], 'description': cat_data['description']}
    )
    if created:
        print(f"   ✓ Category: {cat_data['name']}")

# 4. Create products
print("\n4. Creating products...")
products = [
    {
        'name': 'Whey Protein Chocolate',
        'slug': 'whey-protein-chocolate',
        'description': 'Premium whey protein concentrate, chocolate flavor. 25g protein per serving.',
        'price': 49.99,
        'category': 'SUP',
        'main_category': Category.objects.get(slug='proteins'),
        'stock': 50,
        'protein_per_serving': 25,
        'carbs_per_serving': 3,
        'fat_per_serving': 1,
        'calories_per_serving': 120,
        'is_active': True,
    },
    {
        'name': 'Creatine Monohydrate',
        'slug': 'creatine-monohydrate',
        'description': 'Pure creatine monohydrate powder. Increases strength and muscle mass.',
        'price': 29.99,
        'category': 'SUP',
        'main_category': Category.objects.get(slug='creatine'),
        'stock': 30,
        'protein_per_serving': 0,
        'carbs_per_serving': 0,
        'fat_per_serving': 0,
        'calories_per_serving': 0,
        'is_active': True,
    },
    {
        'name': 'Pre-Workout Energizer',
        'slug': 'pre-workout-energizer',
        'description': 'Energy boost for intense workouts. Contains caffeine and beta-alanine.',
        'price': 39.99,
        'category': 'SUP',
        'main_category': Category.objects.get(slug='pre-workout'),
        'stock': 40,
        'protein_per_serving': 0,
        'carbs_per_serving': 5,
        'fat_per_serving': 0,
        'calories_per_serving': 20,
        'is_active': True,
    },
    {
        'name': 'Sports T-Shirt',
        'slug': 'sports-t-shirt',
        'description': 'Breathable sports t-shirt for workouts. Dry-fit technology.',
        'price': 24.99,
        'category': 'CLO',
        'main_category': Category.objects.get(slug='sportswear'),
        'stock': 100,
        'protein_per_serving': None,
        'carbs_per_serving': None,
        'fat_per_serving': None,
        'calories_per_serving': None,
        'is_active': True,
    },
    {
        'name': 'Dumbbell Set 20kg',
        'slug': 'dumbbell-set-20kg',
        'description': 'Adjustable dumbbell set, 20kg total weight. Perfect for home workouts.',
        'price': 89.99,
        'category': 'EQU',
        'main_category': Category.objects.get(slug='equipment'),
        'stock': 15,
        'protein_per_serving': None,
        'carbs_per_serving': None,
        'fat_per_serving': None,
        'calories_per_serving': None,
        'is_active': True,
    },
    {
        'name': 'Protein Bars (12 pack)',
        'slug': 'protein-bars-12-pack',
        'description': 'High protein bars, 20g protein each. Low sugar, great for snacks.',
        'price': 24.99,
        'category': 'FOO',
        'main_category': Category.objects.get(slug='healthy-food'),
        'stock': 60,
        'protein_per_serving': 20,
        'carbs_per_serving': 15,
        'fat_per_serving': 8,
        'calories_per_serving': 180,
        'is_active': True,
    },
]

for prod_data in products:
    prod, created = Product.objects.get_or_create(
        slug=prod_data['slug'],
        defaults={
            'name': prod_data['name'],
            'description': prod_data['description'],
            'price': prod_data['price'],
            'category': prod_data['category'],
            'main_category': prod_data['main_category'],
            'stock': prod_data['stock'],
            'protein_per_serving': prod_data['protein_per_serving'],
            'carbs_per_serving': prod_data['carbs_per_serving'],
            'fat_per_serving': prod_data['fat_per_serving'],
            'calories_per_serving': prod_data['calories_per_serving'],
            'is_active': prod_data['is_active'],
        }
    )
    if created:
        print(f"   ✓ Product: {prod_data['name']} - ${prod_data['price']}")

# 5. Create sample meal plan
print("\n5. Creating sample meal plan...")
try:
    MealPlan.objects.create(
        user=demo,
        name='Muscle Gain Plan',
        goal='MG',
        activity_level=1.55,
        age=25,
        weight=70.0,
        height=175.0,
        bmr=1680,
        tdee=2604,
        target_calories=2904,
        protein_ratio=0.4,
        carbs_ratio=0.4,
        fat_ratio=0.2,
        is_active=True,
    )
    print("   ✓ Sample meal plan created")
except:
    print("   ⚠ Could not create meal plan")

print("\n=== SAMPLE DATA CREATED SUCCESSFULLY ===")
print("\nAccess Information:")
print("  • Application: http://localhost:8000")
print("  • Admin Panel: http://localhost:8000/admin")
print("  • Demo Login: demo / demo123")
print("  • Admin Login: admin / admin123")
print("\nAPI Endpoints:")
print("  • Products API: http://localhost:8000/store/api/products/")
print("  • Categories API: http://localhost:8000/store/api/categories/")
print("  • Statistics API: http://localhost:8000/store/api/stats/")