import spacy
from spacy.training.example import Example
from spacy.util import minibatch
import random
import os

TRAIN_DATA = [{
    "TCS": {
        "about": "TCS is a global IT service provider under the Tata Group.",
        "pros": "Strong brand, high ROE, consistent growth.",
        "cons": "Valuation concerns, dependency on US/Europe markets.",
        "financials": {
            "revenue": "₹2.25 lakh crore",
            "PE": "30.5",
            "ROE": "35%",
            "market_cap": "₹12 lakh crore"
        }
    },
    "Reliance": {
        "about": "Reliance Industries is a major Indian conglomerate with business in oil, telecom, and retail.",
        "pros": "Diversified business, strong retail and telecom presence.",
        "cons": "Debt from expansions, oil price exposure.",
        "financials": {
            "revenue": "₹2.25 lakh crore",
            "PE": "24.3",
            "ROE": "8.5%",
            "market_cap": "₹19 lakh crore"
        }
    },
    "Infosys": {
        "about": "Infosys Ltd provides consulting, technology, outsourcing and next-generation digital services to enable clients to execute strategies for their digital transformation.It is the 2nd largest Information Technology company in India behind TCS.",
        "pros": "almost debt free,good return on equity track record: 3 Years ROE 30.7%,healthy dividend payout of 65.9%",
        "cons": "Promoter holding is low: 14.6%",
        "financials": {
            "revenue": "1.607 lakh crore",
            "PE": "24.3",
            "ROE": "28.8%",
            "market_cap": "₹6.44 lakh crore"
        }
    },
    "HDFC Bank": {
        "about": "HDFC Bank Limited is an Indian banking and financial services company headquartered in Mumbai. It is India's largest private sector bank by assets and the world's tenth-largest bank by market capitalization as of May 2024.As of April 2024, HDFC Bank has a market capitalization of $145 billion, making it the third-largest company on the Indian stock exchanges.",
        "pros": "almost debt free,good return on equity track record: 3 Years ROE 30.7%,healthy dividend payout of 65.9%",
        "cons": "Promoter holding is low: 14.6%",
        "financials": {
            "revenue": "1.08 lakh crore",
            "PE": "21.0",
            "ROE": "14.5%",
            "market_cap": "₹14.86 lakh crore"
        }
    },
    "HUL": {
        "about": "Hindustan Unilever is in the FMCG business comprising primarily of Home Care, Beauty & Personal Care and Foods & Refreshment segments. The Company has manufacturing facilities across the country and sells primarily in India.",
        "pros": "almost debt free,good return on equity track record: 3 Years ROE 30.7%,healthy dividend payout of 65.9%",
        "cons": "Promoter holding is low: 14.6%",
        "financials": {
            "revenue": "0.62 lakh crore",
            "PE": "53.0",
            "ROE": "20.7%",
            "market_cap": "₹5.52 lakh crore"
        }
    },
    "State Bank of India": {
        "about": "State Bank of India is a Fortune 500 company. It is an Indian Multinational, Public Sector banking and financial services statutory body headquartered in Mumbai. It is the largest and oldest bank in India with over 200 years of history.",
        "pros": "Delivered good profit growth of 36.3% CAGR over last 5 years,maintains a healthy dividend payout of 18.2%",
        "cons": "Low interest coverage ratio ,Contingent liabilities of Rs.27,42,584 Cr ,Earnings include an other income of Rs.1,72,406 Cr.",
        "financials": {
            "revenue": "0.709 lakh crore",
            "PE": "9.42",
            "ROE": "17.2%",
            "market_cap": "₹0.71 lakh crore"
        }
    },
    "Bajaj finance": {
        "about": "Bajaj Finance is mainly engaged in the business of lending. BFL has a diversified lending portfolio across retail, SME and commercial customers with a significant presence in urban and rural India. It also accepts public and corporate deposits and offers variety of financial services products to its customers.",
        "pros": "Delivered good profit growth of 25.9% CAGR over last 5 years ,maintaining a healthy dividend payout of 17.4%,Company's median sales growth is 30.9% of last 10 years",
        "cons": "Trading at 5.78 times its book value,low interest coverage ratio.",
        "financials": {
            "revenue": "0.18 lakh crore",
            "PE": "33.6",
            "ROE": "19.2%",
            "market_cap": "₹5.58 lakh crore"
        }
    },
    "Larsen & Turbo": {
        "about": "Larsen & Toubro Ltd is a multinational conglomerate which is primarily engaged in providing engineering, procurement and construction (EPC) solutions in key sectors such as Infrastructure, Hydrocarbon, Power, Process Industries and Defence, Information Technology and Financial Services in domestic and international markets.",
        "pros": "Delivered good profit growth of 25.9% CAGR over last 5 years ,maintaining a healthy dividend payout of 17.4%,Company's median sales growth is 30.9% of last 10 years",
        "cons": "Trading at 5.78 times its book value,low interest coverage ratio.",
        "financials": {
            "revenue": "2.55 lakh crore",
            "PE": "32.8",
            "ROE": "16.6%",
            "market_cap": "₹4.98 lakh crore"
        }
    },
    "HCL": {
        "about": "HCL Tech is a leading global IT services company, which is ranked amongst the top five Indian IT services companies in terms of revenues. Since its inception into the global landscape after its IPO in 1999, HCL Tech has focused on transformational outsourcing, and offers an integrated portfolio of services including software-led IT solutions, remote infrastructure management, engineering and R&D services and BPO. The company leverages its extensive global offshore infrastructure and network of offices in 46 countries to provide multi-service delivery in key industry verticals.",
        "pros": "Almost debt free,providing a good dividend yield of 3.30% ,maintaining a healthy dividend payout of 90.4%,Debtor days have improved from 79.1 to 60.9 days.",
        "cons": "The company has delivered a poor sales growth of 10.6% over past five years.",
        "financials": {
            "revenue": "0.30 lakh crore",
            "PE": "25.3",
            "ROE": "25.2%",
            "market_cap": "₹4.40 lakh crore"
        }
    },

    "Maruti Suzuki": {
        "about": "The Company was established in 1981. A joint venture agreement was signed between the Government of India and Suzuki Motor Corporation (SMC), Japan in 1982. The Company became a subsidiary of SMC in 2002.It is the market leader in passenger vehicle segment in India. In terms of production volume and sales, the Company is now SMC’s largest subsidiary. SMC currently holds 56.28% of its equity stake.",
        "pros": "Reduced debt,almost debt free,delivered good profit growth of 34.8% CAGR over last 5 years,been maintaining a healthy dividend payout of 30.9%",
        "cons": " no found as such",
        "financials": {
            "revenue": "1.45 lakh crore",
            "PE": "26.4",
            "ROE": "16.0%",
            "market_cap": "₹3.82 lakh crore"
        }
    },
    "UltraTech Cement": {
        "about": "UltraTech Cement is engaged in the manufacturing and sale of Cement and Cement related product primarily across globe.",
        "pros": "Reduced debt,almost debt free,delivered good profit growth of 34.8% CAGR over last 5 years,been maintaining a healthy dividend payout of 30.9%",
        "cons": " no found as such",
        "financials": {
            "revenue": "0.75 lakh crore",
            "PE": "53.1",
            "ROE": "9.34%",
            "market_cap": "₹3.25 lakh crore"
        }
    },
}


]

nlp = spacy.blank("en") 

if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

optimizer = nlp.begin_training()
for i in range(20):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = minibatch(TRAIN_DATA, size=2)
    for batch in batches:
        for text, annotations in batch:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], drop=0.3, losses=losses)
    print(f"Losses at iteration {i}: {losses}")
output_dir = "ner_model"
nlp.to_disk(output_dir)
print("Saved trained model to", output_dir)
