import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product

PRODUCTS = [
    # WOMEN
    {'name': 'Women Red Saree', 'category': 'clothing', 'gender': 'women', 'price': 45, 'stock': 30, 'description': 'Beautiful red silk saree for women', 'img': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400'},
    {'name': 'Women Kurti Blue', 'category': 'clothing', 'gender': 'women', 'price': 22, 'stock': 40, 'description': 'Comfortable blue cotton kurti', 'img': 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400'},
    {'name': 'Women Kurti Pink', 'category': 'clothing', 'gender': 'women', 'price': 22, 'stock': 40, 'description': 'Stylish pink cotton kurti', 'img': 'https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?w=400'},
    {'name': 'Women Leggings Black', 'category': 'clothing', 'gender': 'women', 'price': 14, 'stock': 80, 'description': 'Stretchable black leggings', 'img': 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400'},
    {'name': 'Women Leggings Navy', 'category': 'clothing', 'gender': 'women', 'price': 14, 'stock': 70, 'description': 'Comfortable navy blue leggings', 'img': 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=400'},
    {'name': 'Women Floral Dress', 'category': 'clothing', 'gender': 'women', 'price': 35, 'stock': 25, 'description': 'Pretty floral summer dress', 'img': 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400'},
    {'name': 'Women Black Dress', 'category': 'clothing', 'gender': 'women', 'price': 55, 'stock': 20, 'description': 'Elegant black evening dress', 'img': 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400'},
    {'name': 'Women Handbag Brown', 'category': 'clothing', 'gender': 'women', 'price': 39, 'stock': 25, 'description': 'Stylish brown leather handbag', 'img': 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400'},
    {'name': 'Women Heels Pink', 'category': 'clothing', 'gender': 'women', 'price': 49, 'stock': 20, 'description': 'Elegant pink high heels', 'img': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=400'},
    {'name': 'Women Scarf Red', 'category': 'clothing', 'gender': 'women', 'price': 12, 'stock': 60, 'description': 'Soft red cotton scarf', 'img': 'https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=400'},

    # MEN
    {'name': 'Men Formal Suit Black', 'category': 'clothing', 'gender': 'men', 'price': 120, 'stock': 15, 'description': 'Classic black formal suit for men', 'img': 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400'},
    {'name': 'Men Polo Shirt White', 'category': 'clothing', 'gender': 'men', 'price': 25, 'stock': 50, 'description': 'Classic white polo shirt for men', 'img': 'https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400'},
    {'name': 'Men Polo Shirt Navy', 'category': 'clothing', 'gender': 'men', 'price': 25, 'stock': 50, 'description': 'Navy blue polo shirt for men', 'img': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400'},
    {'name': 'Men Cargo Pants', 'category': 'clothing', 'gender': 'men', 'price': 38, 'stock': 35, 'description': 'Durable cargo pants with pockets', 'img': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
    {'name': 'Men Track Pants', 'category': 'clothing', 'gender': 'men', 'price': 22, 'stock': 55, 'description': 'Comfortable track pants for men', 'img': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400'},
    {'name': 'Men Hoodie Grey', 'category': 'clothing', 'gender': 'men', 'price': 35, 'stock': 40, 'description': 'Warm grey hoodie for men', 'img': 'https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400'},
    {'name': 'Men Hoodie Black', 'category': 'clothing', 'gender': 'men', 'price': 35, 'stock': 40, 'description': 'Stylish black hoodie for men', 'img': 'https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400'},
    {'name': 'Men Leather Belt', 'category': 'clothing', 'gender': 'men', 'price': 18, 'stock': 60, 'description': 'Genuine leather belt for men', 'img': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'},
    {'name': 'Men Wallet Black', 'category': 'clothing', 'gender': 'men', 'price': 22, 'stock': 50, 'description': 'Slim black leather wallet', 'img': 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400'},
    {'name': 'Men Cap Blue', 'category': 'clothing', 'gender': 'men', 'price': 12, 'stock': 70, 'description': 'Casual blue baseball cap', 'img': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=400'},

    # KIDS
    {'name': 'Kids Red Frock', 'category': 'clothing', 'gender': 'kids', 'price': 18, 'stock': 35, 'description': 'Cute red frock for little girls', 'img': 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400'},
    {'name': 'Kids Blue Frock', 'category': 'clothing', 'gender': 'kids', 'price': 18, 'stock': 35, 'description': 'Pretty blue frock for girls', 'img': 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400'},
    {'name': 'Kids T-Shirt Yellow', 'category': 'clothing', 'gender': 'kids', 'price': 10, 'stock': 60, 'description': 'Bright yellow kids t-shirt', 'img': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'},
    {'name': 'Kids T-Shirt Red', 'category': 'clothing', 'gender': 'kids', 'price': 10, 'stock': 60, 'description': 'Fun red kids t-shirt', 'img': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'},
    {'name': 'Kids Jeans Blue', 'category': 'clothing', 'gender': 'kids', 'price': 22, 'stock': 40, 'description': 'Comfortable blue jeans for kids', 'img': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'},
    {'name': 'Kids School Shoes', 'category': 'clothing', 'gender': 'kids', 'price': 28, 'stock': 30, 'description': 'Durable black school shoes for kids', 'img': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'},
    {'name': 'Kids Sports Shoes', 'category': 'clothing', 'gender': 'kids', 'price': 25, 'stock': 35, 'description': 'Colorful sports shoes for kids', 'img': 'https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=400'},
    {'name': 'Kids Raincoat Yellow', 'category': 'clothing', 'gender': 'kids', 'price': 20, 'stock': 25, 'description': 'Waterproof yellow raincoat for kids', 'img': 'https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=400'},
    {'name': 'Kids Pajama Set', 'category': 'clothing', 'gender': 'kids', 'price': 15, 'stock': 50, 'description': 'Soft cotton pajama set for kids', 'img': 'https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400'},
    {'name': 'Kids Backpack Blue', 'category': 'clothing', 'gender': 'kids', 'price': 19, 'stock': 40, 'description': 'Colorful school backpack for kids', 'img': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'},
]


class Command(BaseCommand):
    help = 'Add women men kids clothing products'

    def handle(self, *args, **kwargs):
        ok, skip = 0, 0
        for p in PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': p['category'],
                    'gender': p['gender'],
                    'price': p['price'],
                    'stock': p['stock'],
                    'description': p['description'],
                }
            )
            if created:
                try:
                    resp = requests.get(p['img'], timeout=10)
                    if resp.status_code == 200:
                        fname = p['name'].replace(' ', '_') + '.jpg'
                        product.image.save(fname, ContentFile(resp.content), save=True)
                    ok += 1
                    self.stdout.write(f"Added: {p['name']}")
                except Exception as e:
                    ok += 1
            else:
                skip += 1
        self.stdout.write(self.style.SUCCESS(f"\nAdded: {ok} | Skipped: {skip} | Total: {Product.objects.count()}"))
