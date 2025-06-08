from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request, jsonify
import json

with open("companies.json", "r") as f:
    companies = json.load(f)

training_data = []
for company, data in companies.items():
    a=[
        f"What is {company}?", data["about"],
        f"Tell me about {company}", data["about"],
        f"What are the pros of investing in {company}?", data["pros"],
        f"What are the cons of investing in {company}?", data["cons"],
        f"What are the financials of {company}?",
        f"Market Cap: {data['financials']['market_cap']}, ROE: {data['financials']['ROE']}, PE: {data['financials']['PE']}, Revenue: {data['financials']['revenue']}",
        f"What is {company}'s ROE?", f"{data['financials']['ROE']}",
        f"What is {company}'s PE ratio?", f"{data['financials']['PE']}",
        f"What is {company}'s market cap?", f"{data['financials']['market_cap']}",
        f"What is {company}'s revenue?", f"{data['financials']['revenue']}",
    ]
    print(a)
    training_data.extend(a)

bot = ChatBot(
    "univestbot",
    read_only=False,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Sorry, I don’t have an answer. Please reach out at univest@gmail.in for a response from our people.",
            "maximum_similarity_threshold": 1
        }
    ]
)
print(bot)

trainer = ListTrainer(bot)
trainer.train(training_data)

app = Flask(__name__)

def find_matching_company(user_input):
    user_input = user_input.lower()
    matched_companies = []

    for company in companies:
        company_lower = company.lower()

        if company_lower in user_input:
            matched_companies.append(company)

   
    if matched_companies:
        best_match = max(matched_companies, key=len)
        return best_match

    return None

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message", "").lower()
    company = find_matching_company(user_input)


    bot_response = str(bot.get_response(user_input))
    print(bot_response)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
