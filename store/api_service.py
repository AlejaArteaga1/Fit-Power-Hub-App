import requests
import json
from django.core.cache import cache
import random

class ProductAPIService:
    def __init__(self):
        self.base_url = "https://dummyjson.com/products"
        self.cache_timeout = 3600  # 1 hora
    
    def get_all_products(self, limit=20):
        cache_key = f"api_products_all_{limit}"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        try:
            response = requests.get(f"{self.base_url}?limit={limit}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, self.cache_timeout)
                return data
        except:
            pass
        
        return {'products': []}
    
    def get_products_by_category(self, category, limit=10):
        # Mapear nuestras categorías a las de la API
        category_map = {
            'SUP': 'beauty',  # Suplementos -> Belleza/Salud
            'CLO': 'fashion', # Ropa -> Moda
            'EQU': 'home-decoration', # Equipo -> Decoración
            'FOO': 'groceries' # Comida -> Alimentos
        }
        
        api_category = category_map.get(category, '')
        if not api_category:
            return {'products': []}
        
        cache_key = f"api_products_{api_category}_{limit}"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        try:
            response = requests.get(f"{self.base_url}/category/{api_category}?limit={limit}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, self.cache_timeout)
                return data
        except:
            pass
        
        return {'products': []}
    
    def search_products(self, query, limit=10):
        cache_key = f"api_search_{query}_{limit}"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        try:
            response = requests.get(f"{self.base_url}/search?q={query}&limit={limit}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, 300)  # 5 minutos para búsquedas
                return data
        except:
            pass
        
        return {'products': []}
    
    def get_product_detail(self, product_id):
        cache_key = f"api_product_{product_id}"
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        try:
            response = requests.get(f"{self.base_url}/{product_id}", timeout=5)
            if response.status_code == 200:
                data = response.json()
                cache.set(cache_key, data, self.cache_timeout)
                return data
        except:
            pass
        
        return None