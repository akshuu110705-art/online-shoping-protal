import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product

fix_products = [
    {'name': 'iPhone 15', 'img': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400'},
    {'name': 'Samsung Galaxy S24', 'img': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400'},
    {'name': 'Laptop Pro', 'img': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400'},
    {'name': 'Wireless Earbuds', 'img': 'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=400'},
    {'name': 'Smart Watch', 'img': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400'},
    {'name': 'Night Dress Pink', 'img': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400'},
    {'name': 'Night Dress White', 'img': 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400'},
    {'name': 'Woolen Winter Socks', 'img': 'https://images.unsplash.com/photo-1582552938357-32b906df40cb?w=400'},
]


class Command(BaseCommand):
    help = 'Fix missing product images'

    def handle(self, *args, **kwargs):
        for p in fix_products:
            try:
                product = Product.objects.get(name=p['name'])
                resp = requests.get(p['img'], timeout=15)
                if resp.status_code == 200:
                    filename = f"{p['name'].replace(' ', '_')}.jpg"
                    product.image.save(filename, ContentFile(resp.content), save=True)
                    self.stdout.write(f"OK: {p['name']}")
                else:
                    self.stdout.write(f"HTTP {resp.status_code}: {p['name']}")
            except Product.DoesNotExist:
                self.stdout.write(f"Not found in DB: {p['name']}")
            except Exception as e:
                self.stdout.write(f"Error {p['name']}: {str(e)}")
        self.stdout.write(self.style.SUCCESS('Done!'))
