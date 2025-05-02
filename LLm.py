from google import genai
import json
import re
from PIL import Image

with open("config.json") as f:
    config = json.load(f)

client = genai.Client(api_key=config["api_key"])

def parse_llm_response(raw_text: str):
    try:
        cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_text.strip())
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            "response": "Sorry, I couldn't understand the assistant's reply.",
            "is_recommendation_request": False
        }

def getFromGemini(prompt, image_path=None):
    if image_path:
        image = Image.open(image_path)
        model = "gemini-1.5-flash"
        content = [image, prompt]
    else:
        content = [prompt]
        model = "gemini-2.0-flash"

    response = client.models.generate_content(
        model=model,
        contents=content
    )
    return response.text

def analyze_text(user_input, history_prompt):
    analyzeprompt = f"""
    You are a smart shopping assistant AI helping users find products in an online store.

    Your job is to analyze the user's message and recent conversation, and return a JSON object with the following fields:

    1. "categories": a list of possible relevant categories from the following options (select one or more as appropriate):
       ["Food", "Electronics", "Daily Essential", "Beverages"]
    2. "semantic_query": a short, descriptive phrase summarizing what kind of item the user wants. This will be used for semantic matching with product descriptions.

    Be specific and use natural language understanding to choose the most relevant categories and write a clear, searchable semantic query.

    Here is the recent chat history:
    {history_prompt}

    Now the user says:
    "{user_input}"

    Respond ONLY with valid JSON. No markdown.
    """.strip()
    response = getFromGemini(analyzeprompt)

    parsed = parse_llm_response(response)
    return parsed

def analyze_image(image_path):
    prompt = f"""
    You are a smart AI assistant that analyzes product images to determine what type of item it is.

    Your task is to return the most relevant product category (or categories) the image may belong to.

    Choose one or more from the following options:
    ["Food", "Electronics", "Daily Essential", "Beverages"]

    Return ONLY valid JSON in the following format:
    {{
        "categories": ["Category1", "Category2"]
    }}

    Do NOT include any explanations or markdown.
    """.strip()

    response = getFromGemini(prompt, image_path)
    parsed = parse_llm_response(response)
    return parsed


def getResponse(user_input, history_prompt):

    chatprompt = f"""
    You are a helpful shopping assistant for an online commerce platform.

    Your job is to do two things:
    1. Respond naturally to the user's current message.
    2. Determine whether the user is requesting a product recommendation or just chatting casually.

    Guidelines:
    - If the user is only greeting you or making small talk (e.g., "hi", "how are you?"), set "is_recommendation_request" to false and respond like a polite assistant.
    - If the user is asking for product help, shopping advice, or suggestions, set "is_recommendation_request" to true and reply as if you are about to recommend products (e.g., "Sure! Here are some recommendations.") — do NOT ask further questions.

    Your response must be a JSON object with exactly two fields:
    - "response": a short, friendly sentence
    - "is_recommendation_request": true or false

    Here is the recent chat history:
    {history_prompt}

    Now the user says:
    "{user_input}"
    """.strip()

    response = getFromGemini(chatprompt)

    parsed = parse_llm_response(response)
    return parsed

def double_check(recommendation_list, user_request_text, image_path):
    items_block = ""
    for i, info in enumerate(recommendation_list):
        items_block += f"""
    Item {i}:
    Name: {info['name']}
    Description: {info['description']}
            """.strip() + "\n"

    prompt_text = f"""
    You are a helpful shopping assistant.

    The user's request is:
    "{user_request_text}"

    You are given a list of product recommendations. For each, compare its description with the user's request and decide whether it is a reasonable match.

    Then return a JSON object with two fields:

    1. "valid_indices": a list of indices (e.g., [0, 2])
    2. "reply_text": a short and friendly message to the user. 
   - If no products are a good match, let the user know politely. 
   - If there are matching products, provide a natural-sounding sentence introducing the suggestions (e.g., “Here are a few items that might interest you.” or similar)

    Recommended items:
    {items_block}

    Respond with JSON only. No markdown, no explanation.
        """.strip()

    prompt_image = f"""
    You are a visual assistant that validates product recommendations based on an uploaded image.

    Your task is to compare the uploaded image with the descriptions of the recommended items, and decide which ones match the image content.

    Return a JSON object with:
    1. "valid_indices": a list of matching indices (e.g., [1, 3])
    2. "reply_text": a short, polite, and friendly message to the user. 
       - If some items match, give a helpful and natural response suggesting those products.
       - If nothing matches well, gently inform the user that no suitable items were found based on the image.

    Recommended items:
    {items_block}

    Respond ONLY in JSON. Do not include any markdown or explanations.
        """.strip()
    if image_path:
        response = getFromGemini(prompt_image, image_path)
    else:
        response = getFromGemini(prompt_text)

    return parse_llm_response(response)


if __name__ == "__main__":

    recommendations = [
        {
            "name": "Coca-Cola Classic Can",
            "description": "A refreshing cold beverage perfect for summer days. Enjoy the fizzy sweetness of this iconic soft drink.",
            "image_path": "images/cola.jpg",
            "link": "https://example.com/product/cola"
        },
        {
            "name": "Logitech MX Mechanical Keyboard",
            "description": "A quiet, wireless mechanical keyboard suitable for office or gaming, with backlit keys and long battery life.",
            "image_path": "images/keyboard.jpg",
            "link": "https://example.com/product/keyboard"
        },
        {
            "name": "Red Bull Energy Drink",
            "description": "Boost your energy with this powerful drink. Great for studying, driving, or workouts. Keep cool and productive.",
            "image_path": "images/red_bull.jpg",
            "link": "https://example.com/product/redbull"
        }
    ]

    user_request = "I need something refreshing to drink"

    print("🧪 Testing with text input only...")
    reply_text, filtered = double_check(recommendations, user_request=user_request, image_path=None)
    print("🤖 Reply:", reply_text)
    print("✅ Filtered recommendations:")
    for item in filtered:
        print("-", item["name"])

    print("\\n🧪 Testing with image input only...")
    reply_text_img, filtered_img = double_check(recommendations, user_request=None, image_path="img.png",
                                               )
    print("🤖 Reply:", reply_text_img)
    print("✅ Filtered recommendations:")
    for item in filtered_img:
        print("-", item["name"])
