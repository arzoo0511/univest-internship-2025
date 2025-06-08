from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
bot=ChatBot("calculators",logic_adapters=['chatterbot.logic.MathematicalEvaluation'])
list_to_train=[

]
list_trainer=ListTrainer(bot)
list_trainer.train(list_to_train)
while True:
    user_response=input("User: ")
    print("Chatbot: "+str(bot.get_response(user_response)))