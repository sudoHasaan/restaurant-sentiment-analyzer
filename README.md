# Restaurant Sentiment Analysis Dashboard

A web-based sentiment analysis tool for restaurant reviews that scrapes OpenTable reviews, categorizes feedback using Claude AI, and provides visual competitor analysis.

## 🌟 Features

- **Web Scraping**: Automatically scrapes restaurant reviews from OpenTable
- **AI-Powered Categorization**: Uses Anthropic's Claude AI to categorize reviews into:
  - Food Quality feedback
  - Staff/Service feedback
- **Interactive Dashboard**: Flask-based web interface with:
  - Searchable reviews with highlighted categories
  - Pagination support
  - Dark-themed responsive UI
- **Competitor Analysis**: Compare your restaurant's ratings with competitors over time using visual graphs

## 🛠️ Technologies Used

- **Python 3.x**
- **Flask**: Web framework
- **Selenium & WebDriver Manager**: Web scraping
- **Anthropic Claude API**: AI-powered text categorization
- **Pandas**: Data manipulation
- **Matplotlib**: Data visualization

## 📋 Prerequisites

- Python 3.8 or higher
- Chrome browser (for Selenium)
- Anthropic API key ([Get one here](https://console.anthropic.com/settings/keys))

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/restaurant-sentiment-analysis.git
   cd restaurant-sentiment-analysis
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the project root
   # Add your Anthropic API key
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## 📊 Usage

### Option 1: Quick Start (Using Provided Scripts)

**Step 1: Scrape Reviews**
```bash
python scraper.py
```
This creates `restaurant_reviews_content.csv` with scraped reviews from OpenTable.

**Step 2: Categorize Reviews with AI**
```bash
# Set your API key first
set ANTHROPIC_API_KEY=your_api_key_here

# Run categorization
python categorizer.py
```
This creates `categorized_reviews.json` with AI-analyzed reviews.

**Step 3: Run the Dashboard**
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

### Option 2: Interactive Workflow (Using Jupyter Notebook)

```bash
jupyter notebook project.ipynb
```
Run the cells in order to:
1. Scrape reviews from OpenTable
2. Categorize them using Claude AI
3. Launch the Flask dashboard

## 🎯 Features Walkthrough

### Main Dashboard
- View all categorized reviews
- **Green highlights**: Food quality comments
- **Red highlights**: Staff/service comments
- Search for specific keywords (e.g., "food", "staff", "delicious")

### Competitor Analysis
1. Navigate to "Competitor Analysis"
2. Paste a competitor's OpenTable URL
3. View rating trends comparison graph

## 📁 Project Structure

```
restaurant-sentiment-analysis/
│
├── app.py                          # Flask web application
├── scraper.py                      # OpenTable web scraping module
├── categorizer.py                  # AI categorization module
├── project.ipynb                   # Jupyter notebook (full workflow)
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── .gitignore                      # Git ignore rules
│
├── static/
│   └── style.css                   # Dashboard styling
│
├── templates/
│   ├── base.html                   # Base HTML template
│   ├── index.html                  # Main dashboard
│   └── competitor_analysis.html    # Competitor analysis page
│
├── restaurant_reviews_content.csv  # Scraped reviews (not in repo)
└── categorized_reviews.json        # AI-categorized reviews (not in repo)
```

## 🔒 Security Notes

- **Never commit your API key** to the repository
- The `.gitignore` file excludes sensitive files
- Use environment variables for configuration

## ⚠️ Important Notes

- **Rate Limiting**: Be mindful of API rate limits when categorizing large datasets
- **Web Scraping**: Ensure compliance with OpenTable's Terms of Service
- **Data Privacy**: Remove personal information from scraped reviews before sharing

## 🙏 Acknowledgments

- Built with [Anthropic's Claude API](https://www.anthropic.com/)
- Restaurant data from OpenTable
