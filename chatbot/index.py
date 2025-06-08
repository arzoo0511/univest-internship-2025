from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

app = Flask(__name__)

bot = ChatBot("univestbot", read_only=False,
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "Sorry, I don’t have an answer. Please reach out at univest@gmail.in for a response from our people.",
            "maximum_similarity_threshold": 0.6
        }
    ])

if not os.path.exists("db.sqlite3"):
    list_to_train3 = [{
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
    "ICICI Bank": {
        "about": "ICICI Bank is the second-largest private sector bank in India offering a diversified portfolio of financial products and services to retail, SME and corporate customers. The Bank has an extensive network of branches, ATMs and other touch-points.The ICICI group has presence in businesses like life and general insurance, housing finance, primary dealership, etc, through its subsidiaries and associates.",
        "pros": "Good profit growth of 39.8% CAGR over last 5 years",
        "cons": "trading at 3.24 times its book value Company has low interest coverage ratio.Contingent liabilities of Rs.58,58,608 Cr.Earnings include an other income of Rs.1,08,255 Cr",
        "financials": {
            "revenue": "2.94 lakh crore",
            "PE": "20.0",
            "ROE": "18.0%",
            "market_cap": "₹10.18 lakh crore"
        }
    },
    "Axis Bank": {
        "about": "Incorporated in December 1993, Axis Bank Limited is a private sector bank.It has the third-largest network of branches among private sector banks and an international presence through branches in DIFC (Dubai) and Singapore along with representative offices in Abu Dhabi, Sharjah, Dhaka and Dubai and an offshore banking unit in GIFT City.",
        "pros": "Good profit growth of 39.8% CAGR over last 5 years",
        "cons": "trading at 3.24 times its book value Company has low interest coverage ratio.Contingent liabilities of Rs.58,58,608 Cr.Earnings include an other income of Rs.1,08,255 Cr",
        "financials": {
            "revenue": "3.63 lakh crore",
            "PE": "13.0",
            "ROE": "16.4%",
            "market_cap": "₹1.47 lakh crore"
        }
    },
    "ITC": {
        "about": "Established in 1910, ITC is the largest cigarette manufacturer and seller in the country. ITC operates in four business segments at present — FMCG Cigarettes, FMCG Others, Paperboards, Paper and Packaging, and Agri Business.",
        "pros": "Almost debt free,good dividend yield of 3.43%,good return on equity (ROE) track record: 3 Years ROE 28.3%,Maintaining a healthy dividend payout of 78.6%",
        "cons": "trading at 7.42 times its book value ,poor sales growth of 8.81% over past five years,Earnings include an other income of Rs.17,656 Cr,Working capital days have increased from 60.7 days to 125 days",
        "financials": {
            "revenue": "0.81 lakh crore",
            "PE": "26.3",
            "ROE": "27.5%",
            "market_cap": "₹5.23 lakh crore"
        }
    },
    "Bharti Airtel": {
        "about": "Bharti Airtel Ltd is one of the world’s leading providers of telecommunication services with presence in 18 countries representing India, Sri Lanka, 14 countries in Africa.",
        "pros": "Company has delivered good profit growth of 30.6% CAGR over last 5 years ,maintaining a healthy dividend payout of 38.8%",
        "cons": "Trading at 9.39 times its book value Promoter holding has decreased over last quarter: -0.69% Tax rate seems low",
        "financials": {
            "revenue": "1.72 lakh crore",
            "PE": "40.6",
            "ROE": "28.3%",
            "market_cap": "₹11.26 lakh crore"
        }
    },
    "Kotak Mahindra": {
        "about": "diversified financial services group providing a wide range of banking and financial services including Retail Banking, Treasury and Corporate Banking, Investment Banking, Stock Broking, Vehicle Finance, Advisory services, Asset Management, Life Insurance and General Insurance.",
        "pros": "not very well defined pros discovered ",
        "cons": "Trading at 2.60 times its book value,low interest coverage ratio,Contingent liabilities of Rs.7,77,539 Cr ,Earnings include an other income of Rs.41,211 Cr.",
        "financials": {
            "revenue": "94.27 lakh crore",
            "PE": "21.1",
            "ROE": "13.4%",
            "market_cap": "₹0.406 lakh crore"
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
    "Sun Pharmaceutical": {
        "about": "Sun Pharmaceutical Industries Ltd is engaged in the business of manufacturing, developing and marketing a wide range of branded and generic formulations and Active Pharma Ingredients (APIs). The company and its subsidiaries has various manufacturing facilities spread across the world with trading and other incidental and related activities extending to global market.",
        "pros": "Reduced debt ,almost debt free,delivered good profit growth of 23.8% CAGR over last 5 years,been maintaining a healthy dividend payout of 33.8%",
        "cons": "Delivered a poor sales growth of 9.87% over past five years ,Working capital days have increased from 115 days to 174 days",
        "financials": {
            "revenue": "0.52 lakh crore",
            "PE": "34.8",
            "ROE": "16.9%",
            "market_cap": "₹3.99 lakh crore"
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
    "Titan Company": {
        "about": "Titan Company Ltd is among India’s most respected lifestyle companies. It has established leadership positions in the Watches, Jewellery and Eyewear categories led by its trusted brands and differentiated customer experience. It was founded in 1984 as a joint-venture between TATA Group and Tamilnadu Industrial Development Corporation",
        "pros": "Good return on equity (ROE) track record: 3 Years ROE 31.8% ,maintaining a healthy dividend payout of 28.2%",
        "cons": "Trading at 26.7 times its book value,might be capitalizing the interest cost",
        "financials": {
            "revenue": "0.14 lakh crore",
            "PE": "93.2",
            "ROE": "31.8%",
            "market_cap": "₹3.107 lakh crore"
        }
    },
    "Oil & Natural Gas Corp": {
        "about": "ONGC is the largest crude oil and natural gas Company in India, contributing around 71 per cent to Indian domestic production",
        "pros": "Trading at 0.87 times its book value,providing a good dividend yield of 5.20%,maintaining a healthy dividend payout of 37.9%",
        "cons": "Delivered a poor sales growth of 10.8% over past five years,low return on equity of 13.6% over last 3 years.",
        "financials": {
            "revenue": "1.70 lakh crore",
            "PE": "8.20",
            "ROE": "10.7%",
            "market_cap": "₹2.99 lakh crore"
        }
    },
    "Adani Enterprises": {
        "about": "Adani Enterprises Ltd has business interests in various economic areas such as mining, integrated resources management (IRM), infrastructure such as airports, roads, rail/ metro, water, data centres, solar manufacturing, agro and defence.",
        "pros": "Company has delivered good profit growth of 38.6% CAGR over last 5 years",
        "cons": "Trading at 5.66 times its book value,low return on equity of 9.75% over last 3 years,Earnings include an other income of Rs.6,403 Cr.",
        "financials": {
            "revenue": "1.003 lakh crore",
            "PE": "65.4",
            "ROE": "9.82%",
            "market_cap": "₹2.86 lakh crore"
        }
    }
}

     ]  

    trainer = ListTrainer(bot)
    trainer.train(list_to_train3)


#@app.route('/')
#def home():
 #   return render_template('index.html') 

#@app.route('/get_response', methods=['POST'])
#def get_bot_response():
 #   data = request.get_json()
  #  user_input = data.get("message", "")
   # response = str(bot.get_response(user_input))
    #return jsonify({'response': response})

#if __name__ == '__main__':
 #   app.run(debug=True)
