import random
import statistics
import matplotlib.pyplot as plt
import numpy as np

class FoodDeliveryAnalyzer:
    def __init__(self, data):
        self.data = data
        self.min_price = min(item['price'] for item in data)
        self.max_price = max(item['price'] for item in data)
        self.min_delivery_time = min(item['delivery_time_minutes'] for item in data)
        self.max_delivery_time = max(item['delivery_time_minutes'] for item in data)

    def _normalize_value(self, value, min_val, max_val, invert=False):
        if max_val == min_val:
            return 0.5 if not invert else 0.5
        normalized = (value - min_val) / (max_val - min_val)
        return 1 - normalized if invert else normalized

    def _get_quantity_score(self, quantity_description):
        quantity_map = {
            'Very Small': 1, 'Small': 2, 'Standard': 3, 'Generous': 4, 'Very Generous': 5
        }
        return quantity_map.get(quantity_description, 3)

    def _get_review_sentiment_score(self, reviews):
        positive_keywords = ['good', 'great', 'delicious', 'tasty', 'amazing', 'excellent', 'fast', 'hot', 'fresh', 'satisfied', 'love', 'worth', 'hygienic']
        negative_keywords = ['bad', 'poor', 'soggy', 'cold', 'late', 'disappointed', 'awful', 'terrible', 'small portion', 'expensive', 'unhygienic', 'spicy (too much)']
        neutral_keywords = ['okay', 'average', 'standard', 'decent', 'nothing special']

        total_score = 0
        num_reviews = len(reviews)
        if not num_reviews:
            return 0.5

        for review in reviews:
            review_lower = review.lower()
            sentiment_found = False
            if any(keyword in review_lower for keyword in positive_keywords):
                total_score += 1
                sentiment_found = True
            if any(keyword in review_lower for keyword in negative_keywords):
                total_score -= 1
                sentiment_found = True
            if not sentiment_found and any(keyword in review_lower for keyword in neutral_keywords):
                pass

        min_possible = -num_reviews
        max_possible = num_reviews
        return self._normalize_value(total_score, min_possible, max_possible)

    def _calculate_overall_score(self, item):
        weights = {
            'price': 0.25, 'rating': 0.20, 'delivery_time': 0.15,
            'quantity': 0.15, 'quality': 0.15, 'reviews_sentiment': 0.10
        }

        normalized_price = self._normalize_value(item['price'], self.min_price, self.max_price, invert=True)
        normalized_rating = self._normalize_value(item['rating'], 1.0, 5.0)
        normalized_delivery_time = self._normalize_value(item['delivery_time_minutes'], self.min_delivery_time, self.max_delivery_time, invert=True)
        normalized_quantity = self._normalize_value(self._get_quantity_score(item['quantity_description']), 1, 5)
        normalized_quality = self._normalize_value(item['quality_score'], 1, 5)
        normalized_reviews_sentiment = self._get_review_sentiment_score(item['reviews'])

        overall_score = (
            normalized_price * weights['price'] +
            normalized_rating * weights['rating'] +
            normalized_delivery_time * weights['delivery_time'] +
            normalized_quantity * weights['quantity'] +
            normalized_quality * weights['quality'] +
            normalized_reviews_sentiment * weights['reviews_sentiment']
        )
        return overall_score

    def analyze_food_item(self, food_item_name):
        matching_items = [
            item for item in self.data
            if food_item_name.lower() in item['food_item'].lower()
        ]

        if not matching_items:
            print(f"No results found for '{food_item_name}'.")
            return None

        for item in matching_items:
            item['overall_score'] = self._calculate_overall_score(item)

        sorted_items = sorted(matching_items, key=lambda x: x['overall_score'], reverse=True)

        return {
            'best_option': sorted_items[0] if sorted_items else None,
            'all_options_sorted': sorted_items
        }

def generate_synthetic_data(num_entries=1000):
    platforms = ['Swiggy', 'Blinkit', 'Zomato', 'Deliveroo', 'Domino\'s']
    indian_food_items = [
        'Hyderabadi Biryani', 'Chicken Biryani', 'Veg Biryani', 'Dosa', 'Idli', 'Vada',
        'Pulihora', 'Chapati', 'Paneer Butter Masala', 'Chicken 65', 'Fish Fry',
        'Gongura Chicken', 'Mirchi Bajji', 'Double Ka Meetha', 'Qubani Ka Meetha',
        'Pizza (Indian Style)', 'Burger (Local)', 'Pasta (Fusion)', 'Samosa', 'Vada Pav',
        'Tea', 'Coffee', 'Fresh Juice'
    ]
    restaurants_indian = [
        'Paradise Biryani', 'Bawarchi', 'Pista House', 'Sarvi', 'Hotel Nayaab',
        'Minerva Coffee Shop', 'Chutneys', 'Ulavacharu',
        'Rayalaseema Ruchulu', 'Ohri\'s', 'Simply South',
        'Amaravathi Restaurant', 'Grand Bawarchi', 'RR Durbar',
        'Domino\'s Pizza', 'Pizza Hut', 'McDonald\'s', 'KFC',
        'Local Tiffin Centre', 'Street Spice', 'The Grand Kitchen'
    ]
    quantity_descriptions = ['Very Small', 'Small', 'Standard', 'Generous', 'Very Generous']

    positive_reviews = [
        "Absolutely delicious, the Biryani was authentic!", "Great taste and good portion size, worth the money.",
        "Delivered super fast, food was hot and fresh.", "Customer service from Swiggy was excellent, a delightful experience.",
        "Fresh ingredients and perfectly cooked, felt hygienic.", "Value for money is amazing, will order from Zomato again.",
        "The Dosa was crispy and chutney was perfect.", "Paneer Butter Masala was rich and creamy.",
        "Timely delivery by Deliveroo, highly satisfied."
    ]
    negative_reviews = [
        "Food was cold and late, very disappointed with Blinkit delivery.", "Portion size was disappointingly small for the price.",
        "Not worth the price, taste was bland and unauthentic.", "Mistake in the order, and took too long to resolve.",
        "Ingredients didn't seem fresh, felt a bit unhygienic.", "Packaging was damaged when it arrived, a mess.",
        "Too much oil/spice, couldn't finish it.", "The pizza from Domino's arrived squashed.", "Delivery rider was rude."
    ]
    neutral_reviews = [
        "It was okay, nothing special, standard delivery experience.", "Decent food, but a bit pricey for what it offers.",
        "Arrived as expected, no complaints.", "Could be better, but acceptable.", "Average meal, nothing to write home about.",
        "Just a regular order, nothing stood out."
    ]

    data = []
    for i in range(num_entries):
        platform = random.choice(platforms)
        food_item = random.choice(indian_food_items)
        restaurant = random.choice(restaurants_indian)

        if platform == 'Domino\'s':
            food_item = random.choice(['Pizza', 'Garlic Bread', 'Choco Lava Cake'])
            restaurant = 'Domino\'s Pizza'
            price = round(random.uniform(250.0, 800.0), 2)
            delivery_time_minutes = random.randint(20, 45)
        elif platform == 'Blinkit':
            food_item = random.choice(['Samosa', 'Tea', 'Coffee', 'Fresh Juice', random.choice(indian_food_items)])
            price = round(random.uniform(50.0, 400.0), 2)
            delivery_time_minutes = random.randint(15, 35)
        else:
            price = round(random.uniform(100.0, 1200.0), 2)
            delivery_time_minutes = random.randint(25, 75)

        rating = round(random.uniform(3.0, 5.0), 1)
        quantity_description = random.choice(quantity_descriptions)
        quality_score = random.randint(1, 5)

        reviews = []
        num_reviews = random.randint(1, 3)
        for _ in range(num_reviews):
            review_type = random.choices(['positive', 'negative', 'neutral'], weights=[0.65, 0.20, 0.15], k=1)[0]
            if review_type == 'positive':
                reviews.append(random.choice(positive_reviews))
            elif review_type == 'negative':
                reviews.append(random.choice(negative_reviews))
            else:
                reviews.append(random.choice(neutral_reviews))

        data.append({
            'id': i + 1, 'platform': platform, 'food_item': food_item, 'restaurant': restaurant,
            'price': price, 'rating': rating, 'delivery_time_minutes': delivery_time_minutes,
            'quantity_description': quantity_description, 'quality_score': quality_score, 'reviews': reviews
        })
    return data

def display_platform_comparison_graphs(food_item_name, all_options_sorted):
    if not all_options_sorted:
        print("No data available to generate graphs.")
        return

    platform_data = {}
    for item in all_options_sorted:
        platform = item['platform']
        if platform not in platform_data:
            platform_data[platform] = {'prices': [], 'ratings': [], 'delivery_times': [], 'overall_scores': []}
        platform_data[platform]['prices'].append(item['price'])
        platform_data[platform]['ratings'].append(item['rating'])
        platform_data[platform]['delivery_times'].append(item['delivery_time_minutes'])
        platform_data[platform]['overall_scores'].append(item['overall_score'])

    platforms = sorted(list(platform_data.keys()))
    avg_prices = [np.mean(platform_data[p]['prices']) for p in platforms]
    avg_ratings = [np.mean(platform_data[p]['ratings']) for p in platforms]
    avg_delivery_times = [np.mean(platform_data[p]['delivery_times']) for p in platforms]
    avg_overall_scores = [np.mean(platform_data[p]['overall_scores']) for p in platforms]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Platform Comparison for "{food_item_name}"', fontsize=16)

    axes[0, 0].bar(platforms, avg_prices, color='skyblue')
    axes[0, 0].set_title('Average Price (₹)')
    axes[0, 0].set_ylabel('Price (₹)')
    axes[0, 0].tick_params(axis='x', rotation=45)
    axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)

    axes[0, 1].bar(platforms, avg_ratings, color='lightgreen')
    axes[0, 1].set_title('Average Customer Rating (1-5)')
    axes[0, 1].set_ylabel('Rating')
    axes[0, 1].set_ylim(3.0, 5.0)
    axes[0, 1].tick_params(axis='x', rotation=45)
    axes[0, 1].grid(axis='y', linestyle='--', alpha=0.7)

    axes[1, 0].bar(platforms, avg_delivery_times, color='salmon')
    axes[1, 0].set_title('Average Delivery Time (minutes)')
    axes[1, 0].set_ylabel('Time (mins)')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(axis='y', linestyle='--', alpha=0.7)

    axes[1, 1].bar(platforms, avg_overall_scores, color='gold')
    axes[1, 1].set_title('Average Overall Value Score (Higher is Better)')
    axes[1, 1].set_ylabel('Score')
    axes[1, 1].tick_params(axis='x', rotation=45)
    axes[1, 1].grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    plt.show()

if __name__ == "__main__":
    synthetic_data = generate_synthetic_data(num_entries=1500)
    analyzer = FoodDeliveryAnalyzer(synthetic_data)

    while True:
        food_item_search = input("\nEnter the food item you want to analyze (e.g., Biryani, Pizza, Dosa) or 'quit' to exit: ").strip()
        if food_item_search.lower() == 'quit':
            break

        results = analyzer.analyze_food_item(food_item_search)

        if results:
            best_option = results['best_option']
            all_options_sorted = results['all_options_sorted']

            if best_option:
                print("\n--- Best Overall Value Found ---")
                print(f"Food Item: {best_option['food_item']}")
                print(f"Platform: {best_option['platform']}")
                print(f"Restaurant: {best_option['restaurant']}")
                print(f"Price: ₹{best_option['price']:.2f}")
                print(f"Rating: {best_option['rating']}/5.0")
                print(f"Delivery Time: {best_option['delivery_time_minutes']} mins")
                print(f"Quantity: {best_option['quantity_description']}")
                print(f"Quality: {best_option['quality_score']}/5 (Higher is better)")
                print(f"Reviews: {'; '.join(best_option['reviews'])}")
                print(f"Overall Score: {best_option['overall_score']:.2f}")

            print("\n--- Top 30 Options (Sorted by Overall Score, Best First) ---")
            print(f"{'#':<3} | {'Platform':<10} | {'Restaurant':<25} | {'Food Item':<20} | {'Price':<8} | {'Rating':<7} | {'Time':<5} | {'Qty':<9} | {'Qual':<5} | {'Score':<6}")
            print("-" * 115)

            for i, item in enumerate(all_options_sorted[:30]):
                print(f"{i+1:<3} | {item['platform']:<10} | {item['restaurant']:<25} | {item['food_item']:<20} | ₹{item['price']:<6.2f} | {item['rating']:.1f}/5.0 | {item['delivery_time_minutes']:<5} | {item['quantity_description'][0]:<9} | {item['quality_score']}/5 | {item['overall_score']:.2f}")

            if all_options_sorted:
                display_platform_comparison_graphs(food_item_search, all_options_sorted)
        print("\n" + "=" * 115 + "\n")
    print("Thank you for using the Food Delivery Analysis System!")
