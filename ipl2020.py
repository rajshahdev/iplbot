import csv
# from pymongo import MongoClient
from flask import Flask,request
from twilio.twiml.messaging_response import MessagingResponse
# import urllib
from twilio.rest import Client
from pycricbuzz import Cricbuzz
import json
import os


apbot=Flask(__name__)

twilio_account = "ACb1aff114e44dc432f3dc0a2689d8772d"
twilio_token = "4e347796d5400b8729a0da9f61864ed7"
ACCOUNT_ID = twilio_account
TWILIO_id = twilio_token
client = Client(ACCOUNT_ID,TWILIO_id)

TWILIO_NUMBER = 'whatsapp:+14155238886'

@apbot.route("/sms",methods=["GET","POST"])
def reply():
    msg_text=request.form.get("Body")
    # x=collection.find_one({"NUMBER":num})
    # try:
    #     status=x["status"]
    # except:
    #     pass
    # if (bool(num)==False):
        # collection.insert_one({"NUMBER":num,"status":"first"})
    msg=MessagingResponse()
    resp=msg.message("""Hello & welcome ,myself IPL BOT ,a bot for knowing live score updates for ipl matches.
please read and select from the below options:
enter *1* to get live score for an ongoing match,
enter *2* to get sull score updates for an ongoing match,
enter *3* to get complete match information for an ongoing match.
""")
    return (str(msg))


    # if(status=="first"):
    #     msg=msg=MessagingResponse()
    if(msg_text=="1"):
        c=Cricbuzz()
        matches=c.matches()
        match_data=[]
        for match in matches:
            if match["srs"]=="Indian Premier League 2020" and not(match["mchstate"]=="preview"):
                match_data.append(match)
        if (len(match_data)==1):
            match_id=match_data[0]["id"]
        livescore=c.livescore(mid=match_id)
        batting_team=livescore["batting"]["team"]
        batting_inn=livescore["batting"]["score"][0]["inning_num"]
        batting_score=livescore["batting"]["score"][0]["runs"]
        battig_overs=livescore["batting"]["score"][0]["overs"]
        batting_wickets=livescore["batting"]["score"][0]["wickets"]
        livescore=f"""Currently innings no {batting_inn} is going on , {batting_team} is doing the batting.
Cuurent score is {batting_score} runs  at the end of {battig_overs} overs with the loss of {batting_wickets} wickets."""
        resp=msg.message(livescore)
        return (str(msg))
    elif(msg_text=="2"):
        c=Cricbuzz()
        matches=c.matches()
        match_data=[]
        for match in matches:
            if match["srs"]=="Indian Premier League 2020" and not(match["mchstate"]=="preview"):
                match_data.append(match)
        if (len(match_data)==1):
            match_id=match_data[0]["id"]
        fullscore=c.scorecard(mid=match_id)
        resp=msg.message(fullscore)
        return (str(msg))

    elif(msg_text=="3"):
        c=Cricbuzz()
        matches=c.matches()
        match_data=[]
        for match in matches:
            if match["srs"]=="Indian Premier League 2020" and not(match["mchstate"]=="preview"):
                match_data.append(match)
        if (len(match_data)==1):
            match_id=match_data[0]["id"]
        info=c.matchinfo(mid=match_id)
        info=json.dumps(info)
        resp=msg.message(info)
        return (str(msg))
    else:
        resp=msg.message("""Sorry you have entered invalid option.
please read and select from the below options:
enter *1* to get live score for an ongoing match,
enter *2* to get sull score updates for an ongoing match,
enter *3* to get complete match information for an ongoing match.
""")
        return (str(msg))
        

if __name__=="__main__":
    apbot.run()