import sqlite3

products = [
    {
        'name': 'Chips Ahoy! Original Chocolate Chip Cookies, Party Size',
        'description': "Chips Ahoy! delivers the sweet, classic taste of chocolate chip cookies with a delicious crunch. Perfect for sharing at parties, keeping in lunchboxes, or enjoying with milk at home. This party-sized pack ensures you'll always have a treat on hand. Made with real chocolate chips and baked to perfection.",
        'image_path': 'images/cookies.jpg',
        'category': 'Food',
        'link': 'https://www.example.com/product/chips-ahoy-cookies'
    },
    {
        'name': 'Nestle Mini Chocolate Bars Variety Pack (50 Count)',
        'description': 'An assortment of your favorite mini chocolate bars including Kit Kat, Coffee Crisp, Smarties, and Aero. Ideal for sharing, parties, Halloween treats, or quick indulgent snacks. Proudly made in Canada and peanut-free, suitable for school-safe environments.',
        'image_path': 'images/chocolate.jpg',
        'category': 'Food',
        'link': 'https://www.example.com/product/nestle-mini-chocolate-pack'
    },
    {
        'name': 'Starbucks Doubleshot Energy Coffee Drink, Mocha, 12-Pack',
        'description': 'A perfect energy boost combining Starbucks coffee with enhanced energy ingredients. Smooth mocha flavor with 135mg of caffeine per can. Ideal for mornings, busy workdays, or pre-workout pick-me-ups. Best served chilled or over ice.',
        'image_path': 'images/coffee.jpg',
        'category': 'Beverages',
        'link': 'https://www.example.com/product/starbucks-doubleshot-mocha'
    },
    {
        'name': 'Coca-Cola Classic Soft Drink, 24 Cans',
        'description': 'Enjoy the refreshing and original taste of Coca-Cola in a convenient 24-pack. Ideal for family gatherings, barbecues, picnics, or stocking your fridge. Each can offers the same crisp cola flavor people have loved for over a century.',
        'image_path': 'images/cola.jpg',
        'category': 'Beverages',
        'link': 'https://www.example.com/product/coca-cola-24-pack'
    },
    {
        'name': 'Quaker Oat Bran Hot Cereal, 625g',
        'description': 'A hearty, creamy hot cereal made from high-fiber oat bran. Excellent for baking muffins or enjoying as a warm breakfast. Supports heart health and digestion. Serve with fruit, honey, or milk for a nutritious and filling meal.',
        'image_path': 'images/oatmeal.jpg',
        'category': 'Food',
        'link': 'https://www.example.com/product/quaker-oat-bran'
    },
    {
        'name': 'Mr. Noodles Spicy Chicken Instant Cup Noodles, 64g',
        'description': 'Mr. Noodles spicy chicken flavor provides a quick, convenient meal in a microwavable cup. Great for students, late-night snacks, or busy days. Just add water and microwave. Bold flavor and satisfying noodles in one cup.',
        'image_path': 'images/noodle.jpg',
        'category': 'Food',
        'link': 'https://www.example.com/product/mr-noodles-spicy-chicken'
    },
    {
        'name': 'Liguori Farfalle Pasta, 454g',
        'description': 'Premium bow-tie pasta crafted from durum wheat semolina in Italy. Slow dried for superior taste and texture. Perfect for creamy sauces, pasta salads, and traditional Italian dishes. Imported quality for gourmet home cooking.',
        'image_path': 'images/pasta.jpg',
        'category': 'Food',
        'link': 'https://www.example.com/product/liguori-farfalle'
    },
    {
        'name': 'Red Bull Energy Drink, 12 x 250ml',
        'description': 'Red Bull provides wings with its iconic blend of caffeine, taurine, B-vitamins, and sugars. Designed to improve focus and energy. Perfect for athletes, students, or long work sessions. Enjoy chilled for best taste.',
        'image_path': 'images/red_bull.jpg',
        'category': 'Beverages',
        'link': 'https://www.example.com/product/red-bull-energy-drink'
    },
    {
        'name': 'Nestle Pure Life Purified Water, 24 Bottles',
        'description': 'Nestle Pure Life provides crisp, refreshing purified water with added minerals for taste. Comes in a convenient 24-pack of half-liter bottles. Ideal for families, offices, events, or staying hydrated on the go.',
        'image_path': 'images/water.jpg',
        'category': 'Beverages',
        'link': 'https://www.example.com/product/nestle-pure-life-water'
    },
    {
        'name': 'Brisk Lemon Iced Tea, 12 x 355ml Cans',
        'description': "Brisk's lemon iced tea is a bold, tangy, and refreshing drink served cold. Perfect for summer gatherings, road trips, or quenching thirst. Comes in a 12-pack of convenient cans. Made with real tea and natural lemon flavor.",
        'image_path': 'images/ice_tea.jpg',
        'category': 'Beverages',
        'link': 'https://www.example.com/product/brisk-lemon-iced-tea'
    },
    {
        'name': 'BERIBES Over-Ear Wireless Bluetooth Headphones with Deep Bass',
        'description': 'Experience immersive sound with BERIBES over-ear Bluetooth headphones, designed for comfort and clarity. Ideal for music, gaming, or calls with up to 65 hours of playtime. Foldable, lightweight, and perfect for travel, work, or home use. Includes built-in mic and multi-device connectivity.',
        'image_path': 'images/headphone.jpg',
        'category': 'Electronics',
        'link': 'https://www.example.com/product/beribes-wireless-headphones'
    },
    {
        'name': 'Amazon Basics 7-Inch Table Fan - Black',
        'description': 'Compact and powerful, this Amazon Basics table fan is perfect for bedrooms, desktops, dorms, or small offices. With adjustable tilt and quiet operation, it ensures optimal airflow without noise distraction. Energy-efficient and easy to use.',
        'image_path': 'images/fans.jpg',
        'category': 'Electronics',
        'link': 'https://www.example.com/product/amazon-basics-desk-fan'
    },
    {
        'name': 'Glad Small Garbage Bags, 100 Count with Febreze Fresh Clean Scent',
        'description': 'Glad small garbage bags combine strength and freshness. Perfect for bathrooms, offices, and bedrooms. Includes 100 25L bags with Febreze odor control to keep spaces smelling clean. Guaranteed strong with secure drawstring closure.',
        'image_path': 'images/garbage_bag.jpg',
        'category': 'Daily Essential',
        'link': 'https://www.example.com/product/glad-small-trash-bags'
    },
    {
        'name': 'Conair 1600W Compact Hair Dryer with Folding Handle, White',
        'description': 'This lightweight and portable hair dryer from Conair features 2 heat/speed settings and a folding handle, making it ideal for travel and small storage. Efficient 1600W drying power ensures quick styling on the go.',
        'image_path': 'images/hair dryer.jpg',
        'category': 'Daily Essential',
        'link': 'https://www.example.com/product/conair-compact-hair-dryer'
    },
    {
        'name': 'WAV Modern LED Desk Lamp with Touch Control and 5 Brightness Levels',
        'description': 'WAV’s ultra-slim LED desk lamp offers 5 brightness modes with touch-sensitive controls. Great for work, reading, or bedtime use. Energy-saving and flicker-free lighting with adjustable angle design and modern black finish.',
        'image_path': 'images/lampjpg.jpg',
        'category': 'Electronics',
        'link': 'https://www.example.com/product/wav-led-touch-lamp'
    },
    {
        'name': 'Chefman Electric Glass Kettle with LED Indicator, 1.8L',
        'description': 'Boil water quickly with this sleek electric glass kettle from Chefman. 1.8L capacity with auto shut-off and boil-dry protection. Blue LED indicator lights up during heating. Perfect for tea, coffee, or instant meals.',
        'image_path': 'images/kettle.jpg',
        'category': 'Daily Essential',
        'link': 'https://www.example.com/product/chefman-electric-kettle'
    },
    {
        'name': 'Mechanical RGB Gaming Keyboard with Backlit Keys',
        'description': 'Enhance your gaming or work setup with this RGB mechanical keyboard. Customizable lighting effects, durable key switches, and anti-ghosting make it a must-have for gamers and typists. Compatible with Windows and Mac systems.',
        'image_path': 'images/keyboard.jpg',
        'category': 'Electronics',
        'link': 'https://www.example.com/product/rgb-gaming-keyboard'
    },
    {
        'name': 'Tide PODS Spring Meadow 3-in-1 Laundry Detergent, 76 Count',
        'description': 'Tide PODS 3-in-1 combine detergent, stain remover, and color protector. Suitable for all machines and water conditions. Simple to use and perfect for families or shared laundry spaces. Spring Meadow scent leaves clothes fresh and clean.',
        'image_path': 'images/laundry_pods.jpg',
        'category': 'Daily Essential',
        'link': 'https://www.example.com/product/tide-pods-spring-meadow'
    },
    {
        'name': 'Bonterra Facial Tissues, 3 Mega Boxes',
        'description': 'Bonterra tissues offer softness and strength with 3 mega boxes in each pack. Sustainable and recyclable packaging. Ideal for daily use at home, in classrooms, or at the office. Hypoallergenic and gentle on skin.',
        'image_path': 'images/tissue.jpg',
        'category': 'Daily Essential',
        'link': 'https://www.example.com/product/bonterra-facial-tissues'
    },
    {
        'name': 'Scotch-Brite Non-Scratch Scrub Sponges, 3 Count',
        'description': 'Designed for everyday cleaning jobs, these Scotch-Brite sponges are safe for non-stick cookware, showers, countertops, and more. Durable, long-lasting and gentle on surfaces but tough on messes. Ideal for kitchens and bathrooms.',
        'image_path': 'images/sponge.jpg',
        'category': 'Daily Essential',
        'link': 'https://www.example.com/product/scotch-brite-non-scratch-sponges'
    },
]

def create_product_db(db_path='products.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        image_path TEXT,
        category TEXT,
        link TEXT
    )
    ''')
    cursor.execute("DELETE FROM products")
    conn.commit()

    cursor.execute("VACUUM")

    for item in products:
        cursor.execute(
            "INSERT INTO products (name, description, image_path, category, link) VALUES (?, ?, ?, ?, ?)",
            (item["name"], item["description"], item["image_path"], item["category"], item["link"])
        )

    conn.commit()
    conn.close()
    print(f"✅ Successfully created and populated '{db_path}'")

if __name__ == '__main__':
    create_product_db()
