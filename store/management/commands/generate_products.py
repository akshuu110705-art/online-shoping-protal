import requests
import random
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Product

# Unsplash image pools per category
IMAGES = {
    'clothing': [
        'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
        'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400',
        'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=400',
        'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400',
        'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=400',
        'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400',
        'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=400',
        'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400',
        'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
        'https://images.unsplash.com/photo-1556821840-3a63f15732ce?w=400',
    ],
    'electronics': [
        'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400',
        'https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46?w=400',
        'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=400',
        'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400',
        'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400',
        'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400',
        'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400',
        'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400',
    ],
    'books': [
        'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
        'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400',
        'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400',
        'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400',
        'https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=400',
        'https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=400',
    ],
    'beauty': [
        'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400',
        'https://images.unsplash.com/photo-1586495777744-4e6232bf2f9a?w=400',
        'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400',
        'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=400',
        'https://images.unsplash.com/photo-1541643600914-78b084683702?w=400',
        'https://images.unsplash.com/photo-1585751119414-ef2636f8aede?w=400',
    ],
    'home': [
        'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400',
        'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400',
        'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=400',
        'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400',
        'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400',
        'https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=400',
    ],
    'sports': [
        'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
        'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400',
        'https://images.unsplash.com/photo-1575361204480-aadea25e6e68?w=400',
        'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400',
        'https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=400',
        'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=400',
    ],
}

PRODUCTS_DATA = {
    'clothing': {
        'men': [
            'Slim Fit Shirt', 'Regular Fit Jeans', 'Polo T-Shirt', 'Cargo Pants',
            'Formal Blazer', 'Casual Hoodie', 'Track Suit', 'Linen Shirt',
            'Denim Jacket', 'Chino Pants', 'Graphic Tee', 'Sweatshirt',
            'Bomber Jacket', 'Kurta', 'Dhoti', 'Vest', 'Shorts', 'Joggers',
            'Raincoat', 'Overcoat', 'Tuxedo Shirt', 'Henley Shirt',
        ],
        'women': [
            'Floral Kurti', 'Silk Saree', 'Anarkali Dress', 'Palazzo Pants',
            'Crop Top', 'Maxi Dress', 'Lehenga', 'Churidar', 'Salwar Suit',
            'Wrap Dress', 'Pencil Skirt', 'A-Line Skirt', 'Blouse',
            'Cardigan', 'Tunic Top', 'Jumpsuit', 'Co-ord Set', 'Shrug',
            'Ethnic Gown', 'Party Dress', 'Casual Kurti', 'Printed Dress',
        ],
        'kids': [
            'Kids Frock', 'Kids T-Shirt', 'Kids Jeans', 'School Uniform',
            'Kids Kurta', 'Baby Onesie', 'Kids Shorts', 'Kids Hoodie',
            'Kids Pajama', 'Kids Raincoat', 'Kids Tracksuit', 'Kids Dress',
            'Kids Leggings', 'Kids Dungaree', 'Kids Sweatshirt', 'Kids Jacket',
        ],
    },
    'electronics': [
        'Smartphone', 'Laptop', 'Tablet', 'Smartwatch', 'Wireless Earbuds',
        'Bluetooth Speaker', 'Power Bank', 'USB Hub', 'Webcam', 'Keyboard',
        'Mouse', 'Monitor', 'Headphones', 'Gaming Controller', 'Drone',
        'Action Camera', 'Smart TV', 'LED Strip', 'Router', 'Hard Drive',
        'SSD Drive', 'RAM Module', 'Graphics Card', 'CPU Cooler', 'Microphone',
        'Ring Light', 'Tripod', 'Memory Card', 'Charging Cable', 'Adapter',
    ],
    'books': [
        'Self Help Book', 'Fiction Novel', 'Science Book', 'History Book',
        'Biography', 'Cookbook', 'Travel Guide', 'Art Book', 'Poetry Book',
        'Philosophy Book', 'Psychology Book', 'Business Book', 'Tech Book',
        'Children Story', 'Comic Book', 'Manga', 'Dictionary', 'Encyclopedia',
        'Language Guide', 'Math Textbook', 'Physics Book', 'Chemistry Book',
        'Medical Book', 'Law Book', 'Economics Book', 'Political Book',
    ],
    'beauty': [
        'Lipstick', 'Foundation', 'Mascara', 'Eyeshadow', 'Blush',
        'Highlighter', 'Concealer', 'Primer', 'Setting Spray', 'Bronzer',
        'Lip Liner', 'Eyeliner', 'Eyebrow Pencil', 'Nail Polish', 'Lip Gloss',
        'Face Serum', 'Moisturizer', 'Sunscreen', 'Face Wash', 'Toner',
        'Sheet Mask', 'Eye Cream', 'Body Lotion', 'Scrub', 'Hair Mask',
        'Shampoo', 'Conditioner', 'Hair Oil', 'Perfume', 'Deodorant',
        'Body Wash', 'Soap', 'Talcum Powder', 'Lip Balm', 'BB Cream',
    ],
    'home': [
        'Sofa', 'Dining Table', 'Bed Frame', 'Wardrobe', 'Bookshelf',
        'Coffee Table', 'TV Stand', 'Study Desk', 'Chair', 'Stool',
        'Curtains', 'Bed Sheet', 'Pillow', 'Blanket', 'Towel Set',
        'Frying Pan', 'Pressure Cooker', 'Knife Set', 'Cutting Board',
        'Mixing Bowl', 'Dinner Set', 'Glass Set', 'Mug', 'Kettle',
        'Toaster', 'Blender', 'Rice Cooker', 'Air Fryer', 'Microwave',
        'Wall Clock', 'Photo Frame', 'Vase', 'Candle', 'Lamp',
        'Dustbin', 'Storage Box', 'Hanger Set', 'Door Mat', 'Bath Mat',
    ],
    'sports': [
        'Cricket Bat', 'Football', 'Basketball', 'Tennis Racket', 'Badminton Racket',
        'Volleyball', 'Table Tennis Bat', 'Hockey Stick', 'Golf Club', 'Baseball Bat',
        'Yoga Mat', 'Dumbbell', 'Barbell', 'Resistance Band', 'Pull Up Bar',
        'Skipping Rope', 'Gym Gloves', 'Knee Support', 'Ankle Support', 'Protein Shaker',
        'Running Shoes', 'Sports Socks', 'Gym Bag', 'Water Bottle', 'Foam Roller',
        'Ab Roller', 'Push Up Bar', 'Treadmill', 'Cycle', 'Rowing Machine',
        'Thermometer', 'BP Monitor', 'Pulse Oximeter', 'First Aid Kit', 'Bandage',
        'Sanitizer', 'Face Mask', 'Gloves', 'Stethoscope', 'Weighing Scale',
    ],
}

COLORS = ['Red', 'Blue', 'Black', 'White', 'Green', 'Yellow', 'Pink', 'Purple',
          'Orange', 'Brown', 'Grey', 'Navy', 'Maroon', 'Teal', 'Beige', 'Cream']
SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
BRANDS = ['StyleX', 'FashionHub', 'TrendSet', 'ClassicWear', 'UrbanStyle',
          'ElegantChoice', 'ModernFit', 'PremiumLine', 'BasicEssentials', 'LuxeWear']


def get_image(category, cache={}):
    if category not in cache:
        urls = IMAGES.get(category, IMAGES['clothing'])
        url = random.choice(urls)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                cache[category] = resp.content
            else:
                cache[category] = None
        except:
            cache[category] = None
    return cache[category]


class Command(BaseCommand):
    help = 'Generate 1000+ products'

    def handle(self, *args, **kwargs):
        count = 0
        existing = set(Product.objects.values_list('name', flat=True))

        # Clothing - Men
        for item in PRODUCTS_DATA['clothing']['men']:
            for color in COLORS[:8]:
                name = f"Men {color} {item}"
                if name not in existing:
                    p = Product.objects.create(
                        name=name, category='clothing', gender='men',
                        price=round(random.uniform(15, 120), 2),
                        stock=random.randint(10, 100),
                        description=f"Premium quality men {color.lower()} {item.lower()}. Comfortable and stylish.",
                    )
                    img = get_image('clothing')
                    if img:
                        p.image.save(f"{name.replace(' ','_')}.jpg", ContentFile(img), save=True)
                    count += 1
                    if count % 50 == 0:
                        self.stdout.write(f"Added {count} products...")

        # Clothing - Women
        for item in PRODUCTS_DATA['clothing']['women']:
            for color in COLORS[:8]:
                name = f"Women {color} {item}"
                if name not in existing:
                    p = Product.objects.create(
                        name=name, category='clothing', gender='women',
                        price=round(random.uniform(15, 150), 2),
                        stock=random.randint(10, 80),
                        description=f"Beautiful women {color.lower()} {item.lower()}. Trendy and elegant.",
                    )
                    img = get_image('clothing')
                    if img:
                        p.image.save(f"{name.replace(' ','_')}.jpg", ContentFile(img), save=True)
                    count += 1
                    if count % 50 == 0:
                        self.stdout.write(f"Added {count} products...")

        # Clothing - Kids
        for item in PRODUCTS_DATA['clothing']['kids']:
            for color in COLORS[:6]:
                name = f"Kids {color} {item}"
                if name not in existing:
                    p = Product.objects.create(
                        name=name, category='clothing', gender='kids',
                        price=round(random.uniform(8, 50), 2),
                        stock=random.randint(15, 60),
                        description=f"Cute kids {color.lower()} {item.lower()}. Soft and comfortable.",
                    )
                    img = get_image('clothing')
                    if img:
                        p.image.save(f"{name.replace(' ','_')}.jpg", ContentFile(img), save=True)
                    count += 1
                    if count % 50 == 0:
                        self.stdout.write(f"Added {count} products...")

        # Other categories
        for category, items in PRODUCTS_DATA.items():
            if category == 'clothing':
                continue
            for item in items:
                for brand in BRANDS[:4]:
                    name = f"{brand} {item}"
                    if name not in existing:
                        p = Product.objects.create(
                            name=name, category=category,
                            price=round(random.uniform(5, 500), 2),
                            stock=random.randint(5, 100),
                            description=f"{brand} {item}. High quality product with great features and durability.",
                        )
                        img = get_image(category)
                        if img:
                            p.image.save(f"{name.replace(' ','_')}.jpg", ContentFile(img), save=True)
                        count += 1
                        if count % 50 == 0:
                            self.stdout.write(f"Added {count} products...")

        total = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(f"\nNew products added: {count}"))
        self.stdout.write(self.style.SUCCESS(f"Total products in DB: {total}"))
