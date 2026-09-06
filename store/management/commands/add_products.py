import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product

# Fix missing images for existing products
FIX_IMAGES = [
    {'name': 'Sports Shoes', 'img': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'},
    {'name': 'Face Cream', 'img': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'},
    {'name': 'Sofa Set', 'img': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400'},
    {'name': 'Black Shorts', 'img': 'https://images.unsplash.com/photo-1591195853828-11db59a44f43?w=400'},
    {'name': 'Tennis Racket', 'img': 'https://images.unsplash.com/photo-1617083934555-ac7b4d500b5a?w=400'},
    {'name': 'Tennis Ball', 'img': 'https://images.unsplash.com/photo-1617083934555-ac7b4d500b5a?w=400'},
    {'name': 'Lipstick Red', 'img': 'https://images.unsplash.com/photo-1586495777744-4e6232bf2f9a?w=400'},
    {'name': 'Perfume Rose', 'img': 'https://images.unsplash.com/photo-1541643600914-78b084683702?w=400'},
    {'name': 'Yoga Mat', 'img': 'https://images.unsplash.com/photo-1601925228008-f5e4c5e5e5e5?w=400'},
]

# New products to add
NEW_PRODUCTS = [
    # More T-Shirt colors
    {'name': 'Orange T-Shirt', 'category': 'clothing', 'price': 15, 'stock': 60, 'description': 'Vibrant orange cotton t-shirt', 'img': 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400'},
    {'name': 'Purple T-Shirt', 'category': 'clothing', 'price': 15, 'stock': 60, 'description': 'Stylish purple cotton t-shirt', 'img': 'https://images.unsplash.com/photo-1529374255404-311a2a4f1fd9?w=400'},
    {'name': 'Pink T-Shirt', 'category': 'clothing', 'price': 15, 'stock': 60, 'description': 'Cute pink cotton t-shirt', 'img': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=400'},
    {'name': 'Grey T-Shirt', 'category': 'clothing', 'price': 15, 'stock': 60, 'description': 'Classic grey cotton t-shirt', 'img': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=400'},
    # More Shirts
    {'name': 'Black Formal Shirt', 'category': 'clothing', 'price': 30, 'stock': 35, 'description': 'Elegant black formal shirt', 'img': 'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400'},
    {'name': 'Green Casual Shirt', 'category': 'clothing', 'price': 25, 'stock': 40, 'description': 'Fresh green casual shirt', 'img': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400'},
    {'name': 'Striped Polo Shirt', 'category': 'clothing', 'price': 28, 'stock': 45, 'description': 'Classic striped polo shirt', 'img': 'https://images.unsplash.com/photo-1589310243389-96a5483213a8?w=400'},
    # More Shorts
    {'name': 'Red Shorts', 'category': 'clothing', 'price': 18, 'stock': 50, 'description': 'Bright red casual shorts', 'img': 'https://images.unsplash.com/photo-1591195853828-11db59a44f43?w=400'},
    {'name': 'Khaki Shorts', 'category': 'clothing', 'price': 20, 'stock': 45, 'description': 'Comfortable khaki shorts', 'img': 'https://images.unsplash.com/photo-1565084888279-aca607ecce0c?w=400'},
    # More Shoes
    {'name': 'Blue Sneakers', 'category': 'clothing', 'price': 58, 'stock': 28, 'description': 'Trendy blue sneakers', 'img': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'},
    {'name': 'Sandals Brown', 'category': 'clothing', 'price': 35, 'stock': 40, 'description': 'Comfortable brown sandals', 'img': 'https://images.unsplash.com/photo-1603487742131-4160ec999306?w=400'},
    # More Books
    {'name': 'Atomic Habits', 'category': 'books', 'price': 16, 'stock': 55, 'description': 'Build good habits by James Clear', 'img': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400'},
    {'name': 'Manga Comics Set', 'category': 'books', 'price': 22, 'stock': 30, 'description': 'Popular manga comics collection', 'img': 'https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=400'},
    {'name': 'Hindi Dictionary', 'category': 'books', 'price': 9, 'stock': 65, 'description': 'Hindi to English dictionary', 'img': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400'},
    {'name': 'Spanish Language Book', 'category': 'books', 'price': 15, 'stock': 35, 'description': 'Learn Spanish from scratch', 'img': 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400'},
    # More Beauty
    {'name': 'Blush Palette', 'category': 'beauty', 'price': 20, 'stock': 50, 'description': 'Natural blush palette 6 shades', 'img': 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400'},
    {'name': 'Lip Gloss Set', 'category': 'beauty', 'price': 16, 'stock': 65, 'description': 'Shiny lip gloss set 6 colors', 'img': 'https://images.unsplash.com/photo-1586495777744-4e6232bf2f9a?w=400'},
    {'name': 'Body Lotion', 'category': 'beauty', 'price': 14, 'stock': 70, 'description': 'Moisturizing body lotion', 'img': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'},
    {'name': 'Hair Conditioner', 'category': 'beauty', 'price': 13, 'stock': 75, 'description': 'Deep conditioning hair conditioner', 'img': 'https://images.unsplash.com/photo-1585751119414-ef2636f8aede?w=400'},
    {'name': 'Eyeliner Pencil', 'category': 'beauty', 'price': 10, 'stock': 80, 'description': 'Waterproof black eyeliner pencil', 'img': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400'},
    {'name': 'Face Serum', 'category': 'beauty', 'price': 25, 'stock': 45, 'description': 'Vitamin C brightening face serum', 'img': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'},
    # More Home & Kitchen
    {'name': 'Knife Set 5pc', 'category': 'home', 'price': 28, 'stock': 30, 'description': 'Stainless steel kitchen knife set', 'img': 'https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400'},
    {'name': 'Electric Kettle 1.5L', 'category': 'home', 'price': 32, 'stock': 25, 'description': '1.5L fast boil electric kettle', 'img': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400'},
    {'name': 'Wall Clock', 'category': 'home', 'price': 18, 'stock': 35, 'description': 'Modern silent wall clock', 'img': 'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400'},
    {'name': 'Pillow Set 2pc', 'category': 'home', 'price': 19, 'stock': 50, 'description': 'Soft cotton pillow set 2 pieces', 'img': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400'},
    {'name': 'Curtains Pair', 'category': 'home', 'price': 22, 'stock': 30, 'description': 'Blackout curtains pair', 'img': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400'},
    {'name': 'Toaster 2 Slice', 'category': 'home', 'price': 25, 'stock': 20, 'description': '2 slice pop-up toaster', 'img': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400'},
    # More Medical & Fitness
    {'name': 'Pulse Oximeter', 'category': 'sports', 'price': 15, 'stock': 50, 'description': 'Fingertip pulse oximeter', 'img': 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400'},
    {'name': 'Knee Support Belt', 'category': 'sports', 'price': 12, 'stock': 60, 'description': 'Elastic knee support belt', 'img': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400'},
    {'name': 'Dumbbell Set 10kg', 'category': 'sports', 'price': 55, 'stock': 20, 'description': 'Pair of 10kg rubber dumbbells', 'img': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400'},
    {'name': 'Ab Roller Wheel', 'category': 'sports', 'price': 18, 'stock': 40, 'description': 'Core ab roller exercise wheel', 'img': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400'},
    {'name': 'Foam Roller', 'category': 'sports', 'price': 20, 'stock': 35, 'description': 'Muscle recovery foam roller', 'img': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400'},
    {'name': 'Sports Water Bottle', 'category': 'sports', 'price': 13, 'stock': 80, 'description': '1L BPA free sports water bottle', 'img': 'https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=400'},
]


class Command(BaseCommand):
    help = 'Fix images and add new products'

    def handle(self, *args, **kwargs):
        # Fix missing images
        self.stdout.write("--- Fixing missing images ---")
        for p in FIX_IMAGES:
            try:
                product = Product.objects.get(name=p['name'])
                if not product.image:
                    resp = requests.get(p['img'], timeout=10)
                    if resp.status_code == 200:
                        fname = p['name'].replace(' ', '_') + '.jpg'
                        product.image.save(fname, ContentFile(resp.content), save=True)
                        self.stdout.write(f"Fixed: {p['name']}")
            except Product.DoesNotExist:
                pass
            except Exception as e:
                self.stdout.write(f"Error: {p['name']}")

        # Add new products
        self.stdout.write("--- Adding new products ---")
        ok, skip = 0, 0
        for p in NEW_PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': p['category'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'description': p['description'],
                }
            )
            if created:
                try:
                    resp = requests.get(p['img'], timeout=10)
                    if resp.status_code == 200:
                        fname = p['name'].replace(' ', '_').replace('(', '').replace(')', '') + '.jpg'
                        product.image.save(fname, ContentFile(resp.content), save=True)
                        ok += 1
                        self.stdout.write(f"Added: {p['name']}")
                except Exception as e:
                    ok += 1
                    self.stdout.write(f"Added (no img): {p['name']}")
            else:
                skip += 1

        self.stdout.write(self.style.SUCCESS(f"\nNew added: {ok} | Already existed: {skip}"))
        self.stdout.write(self.style.SUCCESS(f"Total products: {Product.objects.count()}"))
