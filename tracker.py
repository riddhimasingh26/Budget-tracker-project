import requests
import re

# ---------- Google Search Setup ----------
API_KEY = "AIzaSyBRLcD8QCNo-VISEv8rHDw_Kx8-UPkylRY"   # <-- your Google API key
SEARCH_ENGINE_ID = "550d9871ba32940db"  # <-- your custom search engine CX


# ---------- Helper: Extract Price from Snippet ----------
def extract_price(text):
    if not text:
        return None
    match = re.search(r"₹\s?[\d,]+", text)   # looks for ₹ followed by numbers
    if match:
        return int(match.group(0).replace("₹", "").replace(",", "").strip())
    return None


# ---------- Function: Search for alternatives & compare ----------
def search_alternative(product):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": f'"{product}" buy online site:amazon.in OR site:flipkart.com OR site:myntra.com',
        "num": 10   # get top 10 results
    }

    response = requests.get(url, params=params).json()

    if "items" not in response:
        print(f"No exact results found for {product}.")
        return

    results = []
    for item in response["items"]:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        price = extract_price(snippet)
        results.append({"title": title, "link": link, "price": price})

    # Filter out results without price
    results_with_price = [r for r in results if r["price"] is not None]

    if not results_with_price:
        print(f"No prices found for {product}, but here are some links:\n")
        for r in results:
            print(f"- {r['title']}\n  {r['link']}\n")
        return

    # Find cheapest option
    cheapest = min(results_with_price, key=lambda x: x["price"])

    print(f"\n💰 Cheapest option for {product}:")
    print(f"- {cheapest['title']}")
    print(f"  Price: ₹{cheapest['price']}")
    print(f"  Link: {cheapest['link']}\n")


# ---------- Budget Tracker ----------
transactions = []

def add_transaction(item, amount):
    transactions.append({"item": item, "amount": amount})

def analyze_spending():
    if not transactions:
        print("No transactions yet.")
        return None
    
    # Find item with maximum spending
    spend_by_item = {}
    for t in transactions:
        spend_by_item[t["item"]] = spend_by_item.get(t["item"], 0) + t["amount"]

    top_item = max(spend_by_item, key=spend_by_item.get)
    print(f"\n📊 You spend the most on: {top_item} (₹{spend_by_item[top_item]})")
    return top_item


# ---------- Main Program ----------
while True:
    print("\n--- Budget Tracker ---")
    print("1. Add Transaction")
    print("2. Analyze Spending & Suggest Cheapest Alternative")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        item = input("Enter item name: ")
        amount = float(input("Enter amount spent: "))
        add_transaction(item, amount)
        print("✅ Transaction added.")

    elif choice == "2":
        top_item = analyze_spending()
        if top_item:
            search_alternative(top_item)

    elif choice == "3":
        print("Exiting... Goodbye 👋")
        break
    else:
        print("Invalid choice! Try again.")