"""
Flask Web Application for Restaurant Sentiment Analysis Dashboard
Provides interactive dashboard with search, pagination, and competitor analysis
"""

from flask import Flask, render_template, request
from datetime import datetime, timedelta
import json
import re
from math import ceil
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd

# Import custom modules
from scraper import scrape_competitor_reviews

app = Flask(__name__)

# Load reviews data
with open('categorized_reviews.json', 'r', encoding='utf-8') as file:
    reviews_data = json.load(file)


def preprocess_reviews(reviews_data):
    """
    Preprocesses reviews by highlighting food and staff/service comments
    """
    for review in reviews_data:
        original_review = re.sub(r'\s+', ' ', review['Original Review'].strip())
        food_quality = re.sub(r'\s+', ' ', review['Analysis'].get('Food Quality', '').strip())
        staff_service = re.sub(r'\s+', ' ', review['Analysis'].get('Staff/Service', '').strip())

        # Highlight food quality sentences
        for sentence in re.split(r'[.!?]', food_quality):
            sentence = sentence.strip()
            if sentence and sentence in original_review:
                original_review = original_review.replace(
                    sentence, f'<span class="food">{sentence}</span>'
                )

        # Highlight staff/service sentences
        for sentence in re.split(r'[.!?]', staff_service):
            sentence = sentence.strip()
            if sentence and sentence in original_review:
                original_review = original_review.replace(
                    sentence, f'<span class="staff">{sentence}</span>'
                )

        # Label the review based on categories
        if food_quality and staff_service:
            review['Label'] = 'both' 
        elif food_quality:
            review['Label'] = 'food'  
        elif staff_service:
            review['Label'] = 'staff'  
        else:
            review['Label'] = 'none'  

        review['Original Review'] = original_review
    return reviews_data


# Preprocess reviews on startup
reviews_data = preprocess_reviews(reviews_data)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main dashboard route with search and pagination
    """
    search_query = request.form.get('search_query', '').strip().lower()
    page = int(request.args.get('page', 1)) 
    reviews_per_page = 10  
    filtered_reviews = []

    # Filter reviews based on search query
    if search_query:
        for review in reviews_data:
            label = review['Label']

            if search_query == 'food' and label in ['food', 'both']:
                filtered_reviews.append(review)
            elif search_query in ['staff', 'service', 'services'] and label in ['staff', 'both']:
                filtered_reviews.append(review)
            elif search_query in review['Original Review'].lower():
                filtered_reviews.append(review)
    else:
        filtered_reviews = reviews_data

    # Pagination logic
    total_reviews = len(filtered_reviews)
    total_pages = ceil(total_reviews / reviews_per_page)
    start = (page - 1) * reviews_per_page
    end = start + reviews_per_page
    paginated_reviews = filtered_reviews[start:end]

    pagination = {
        "current_page": page,
        "total_pages": total_pages,
        "prev_page": page - 1 if page > 1 else None,
        "next_page": page + 1 if page < total_pages else None,
        "pages": list(range(1, total_pages + 1))
    }

    return render_template('index.html', reviews=paginated_reviews, pagination=pagination)


def parse_date(date_string):
    """
    Parse date strings from reviews
    """
    if "Dined on" in date_string:
        return datetime.strptime(date_string.replace("Dined on ", "").strip(), "%B %d, %Y")
    elif "days ago" in date_string:
        days_ago = int(date_string.split()[1])
        return datetime.now() - timedelta(days=days_ago)
    else:
        return None


@app.route('/competitor-analysis', methods=["GET", "POST"])
def competitor_analysis():
    """
    Competitor analysis route - scrapes competitor data and generates comparison plot
    """
    if request.method == "POST":
        competitor_url = request.form["competitor_url"]
        print(f"Analyzing competitor: {competitor_url}")

        # Scrape competitor reviews
        competitor_file = scrape_competitor_reviews(competitor_url, output_file='competitor_reviews.csv')

        # Load competitor data
        competitor_df = pd.read_csv(competitor_file, lineterminator='\n')
        competitor_df.columns = competitor_df.columns.str.strip()

        # Load main restaurant data
        main_df = pd.read_csv('restaurant_reviews_content.csv')
        main_df.columns = main_df.columns.str.strip()

        # Process main restaurant ratings
        main_ratings = [int(rating[0]) for rating in main_df['Rating']]
        main_df['Rating'] = main_ratings
        main_df['Date'] = main_df['Date'].apply(parse_date)

        # Process competitor ratings
        competitor_ratings = [int(rating[0]) for rating in competitor_df['Rating']]
        
        # Align lengths
        max_len = max(len(main_df), len(competitor_df))
        if len(competitor_ratings) < max_len:
            competitor_ratings.extend([None] * (max_len - len(competitor_ratings)))
        else:
            competitor_ratings = competitor_ratings[:max_len]

        competitor_df_aligned = pd.DataFrame({
            'Rating': competitor_ratings[:len(competitor_df)],
            'Date': competitor_df['Date'].apply(parse_date)
        })

        # Calculate monthly averages
        main_monthly = main_df.groupby(main_df['Date'].dt.to_period('M'))['Rating'].mean()
        competitor_monthly = competitor_df_aligned.groupby(
            competitor_df_aligned['Date'].dt.to_period('M')
        )['Rating'].mean()

        comparison_df = pd.DataFrame({
            'Your Restaurant': main_monthly,
            'Competitor': competitor_monthly
        })
        comparison_df.fillna(0, inplace=True)

        # Generate comparison plot
        plt.figure(figsize=(10, 6))
        plt.plot(comparison_df.index.astype(str), comparison_df['Your Restaurant'], 
                label="Your Restaurant", marker='o', linewidth=2)
        plt.plot(comparison_df.index.astype(str), comparison_df['Competitor'], 
                label="Competitor Restaurant", marker='s', linewidth=2)

        plt.xlabel('Month', fontsize=12)
        plt.ylabel('Average Rating', fontsize=12)
        plt.title('Competitor Analysis: Rating Comparison Over Time', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save plot
        plot_file = 'static/comparison_plot.png'
        plt.savefig(plot_file, dpi=150, bbox_inches='tight')
        plt.close()

        return render_template("competitor_analysis.html", plot_url=plot_file)

    return render_template("competitor_analysis.html")


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
