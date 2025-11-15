"""
AI-Powered Review Categorizer using Anthropic's Claude API
Categorizes restaurant reviews into Food Quality and Staff/Service feedback
"""

import anthropic
import pandas as pd
import json
import time
import os


def categorize_single_review(review_text, client):
    """
    Categorize a single review into Food Quality and Staff/Service categories
    
    Args:
        review_text (str): The review text to categorize
        client: Anthropic client instance
    
    Returns:
        dict: Dictionary with 'Food Quality' and 'Staff/Service' keys
    """
    prompt = (
        "Analyze and categorize the following review from the customer\n"
        "Strictly categorize the review into two categories: 1) Comments about food quality, 2) Comments about staff/service. "
        "Ensure the extracted comments are accurate.\n"
        "Ensure no hallucinations occur and no data irrelevant to the category is added "
        "(e.g. no staff related data should be present in the food information and vice versa).\n"
        "Exclude any personal information (PI) of the reviewers. Separate the feedback clearly into two categories: "
        "'Food Quality' and 'Staff/Service'. Avoid giving any additional information or clarity or note from your side, "
        "just work on review and give categorized response. If any one or both of the categories are not present then "
        "do not provide that category in response only provide that category that is present. "
        "The categories should contain the exact text as present in Original review. Do not complete the sentences on your own, "
        "do not correct the grammar. Just use exact same text as in original review.\n"
        f"Following is the Review Text: {review_text}\n\n"
        "Provide the response in JSON format like this:\n"
        "{\n"
        "  'Food Quality': 'comments about food',\n"
        "  'Staff/Service': 'comments about staff'\n"
        "}\n"
        "strictly follow all the instructions.\n"
    )
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0,
            system="You are an expert assistant specialized in text analysis and categorization that has never been wrong. "
                   "Provide 100 percent accurate responses as asked in the prompts by the user.",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        
        if message:
            response_text = message.content[0].text.strip()
            analysis = json.loads(response_text)
            return analysis
        else:
            return {"Food Quality": "", "Staff/Service": ""}
    
    except Exception as e:
        print(f"Error processing review: {e}")
        return {"Food Quality": "", "Staff/Service": ""}


def categorize_reviews_from_csv(input_csv='restaurant_reviews_content.csv', 
                                 output_json='categorized_reviews.json',
                                 api_key="your_api_key_here",
                                 delay=2):
    """
    Categorize all reviews from a CSV file using Claude AI
    
    Args:
        input_csv (str): Path to input CSV file with reviews
        output_json (str): Path to output JSON file for categorized reviews
        api_key (str): Anthropic API key - REPLACE 'your_api_key_here' with your actual key
        delay (int): Delay in seconds between API calls to avoid rate limiting
    
    Returns:
        str: Path to output JSON file
    """
    # Initialize Anthropic client
    if api_key and api_key != "your_api_key_here":
        client = anthropic.Anthropic(api_key=api_key)
    else:
        # Try to get from environment variable
        client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY from environment
    
    # Read CSV file
    df = pd.read_csv(input_csv, lineterminator='\n')
    df.columns = df.columns.str.strip()
    
    categorized_reviews = []
    total_reviews = len(df)
    
    print(f"Starting categorization of {total_reviews} reviews...")
    
    for index, row in df.iterrows():
        print(f"Processing review {index + 1}/{total_reviews}...")
        
        review_text = row["Review Text"]
        
        # Categorize the review
        analysis = categorize_single_review(review_text, client)
        
        categorized_reviews.append({
            "Reviewer Name": row["Reviewer Name"],
            "Rating": row["Rating"],
            "Date": row["Date"],
            "Original Review": review_text,
            "Analysis": analysis
        })
        
        # Delay to avoid rate limiting
        time.sleep(delay)
    
    # Save to JSON
    with open(output_json, 'w', encoding='utf-8') as file:
        json.dump(categorized_reviews, file, indent=4)
    
    print(f"\nCategorization complete! {len(categorized_reviews)} reviews saved to '{output_json}'")
    return output_json


if __name__ == "__main__":
    # Example usage
    # Make sure ANTHROPIC_API_KEY is set in your environment variables
    categorize_reviews_from_csv(
        input_csv='restaurant_reviews_content.csv',
        output_json='categorized_reviews.json'
    )
