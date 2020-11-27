import discord
import webbrowser
from termcolor import colored
import datetime
import logging
import os
#import Google_Search
import time
from datetime import datetime
from pytz import timezone
from lomond import WebSocket
from unidecode import unidecode
import colorama
import requests
import json
import re
from bs4 import BeautifulSoup
from dhooks import Webhook, Embed
import aniso8601

webhook_url="https://discordapp.com/api/webhooks/773373593521225779/wGC2a6K73R6btbRqLrxqioePAvg4wonN9oZhlDAUDz1D3SQWWGBvE4K8trGWWHYFmJQs"

we="https://discordapp.com/api/webhooks/756387515774140496/Uv0eKVWQR15HaO6wf4t05D8SYJJ9xjQQp8sc7afQVCzQ9yGI2XG7LVqBuhw4ilOo6OIx"




try:
    hook = Webhook(webhook_url)
except:
    print("Invalid WebHook Url!")


try:
    hq = Webhook(we)
except:
    print("Invalid WebHook Url!")
    

def show_not_on():
    colorama.init()
    # Set up logging
    logging.basicConfig(filename="data.log", level=logging.INFO, filemode="w")

    # Read in bearer token and user ID
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            BEARER_TOKEN = settings[0].split("=")[1]
        except IndexError as e:
            logging.fatal(f"Settings read error: {settings}")
            raise e

    print("getting")
    main_url = f"https://api-quiz.hype.space/shows/now?type="
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}",
               "x-hq-client": "Android/1.3.0"}
    # "x-hq-stk": "MQ==",
    # "Connection": "Keep-Alive",
    # "User-Agent": "okhttp/3.8.0"}

    try:
        response_data = requests.get(main_url).json()
    except:
        print("Server response not JSON, retrying...")
        time.sleep(1)

    logging.info(response_data)

    if "broadcast" not in response_data or response_data["broadcast"] is None:
        if "error" in response_data and response_data["error"] == "Auth not valid":
            raise RuntimeError("Connection settings invalid")
        else:
            print("Show not on.")
            tim = (response_data["nextShowTime"])
            tm = aniso8601.parse_datetime(tim)
            x =  tm.strftime("%H:%M:%S [%d/%m/%Y] ")
            x_ind = tm.astimezone(timezone("Asia/Kolkata"))
            x_in = x_ind.strftime("%H:%M:%S [%d/%m/%Y] ")
    
            prize = (response_data["nextShowPrize"])
            time.sleep(5)
            print(x_in)
            print(prize)
            hq.send(f"**Show is Not Live**")
            #hook.send(f"**Next Show Prize ---{NextShowPrize} **")



def show_active():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()
    return response_data['active']


def get_socket_url():
    main_url = 'https://api-quiz.hype.space/shows/now'
    response_data = requests.get(main_url).json()

    socket_url = response_data['broadcast']['socketUrl'].replace('https', 'wss')
    return socket_url


def connect_websocket(socket_url, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}",
               "x-hq-client": "iPhone8,2"}


    websocket = WebSocket(socket_url)

    for header, value in headers.items():
        websocket.add_header(str.encode(header), str.encode(value))

    for msg in websocket.connect(ping_rate=5):
        if msg.name == "text":
            message = msg.text
            message = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", message)
            message_data = json.loads(message)
           # print(message_data)

            if message_data['type'] == 'question':
                question = message_data['question']
                qcnt = message_data['questionNumber']
                Fullcnt = message_data['questionCount']

                print(f"\nQuestion number {qcnt} out of {Fullcnt}\n{question}")
                #hook.send(f"**\nQuestion number {qcnt} out of {Fullcnt}\n{question}**")
                #open_browser(question)
                answers = [unidecode(ans["text"]) for ans in message_data["answers"]]
                print(f"\n{answers[0]}\n{answers[1]}\n{answers[2]}\n")
                real_question = str(question).replace(" ","+")
                google_query = "https://google.com/search?q="+real_question             
                embed=discord.Embed(title=question,url=google_query,description="",color=0xffff00)
                embed.set_author(name = f"Question {qcnt} out of {Fullcnt}")
                hook.send(embed=embed)
                #hook.send("+hq")
                option1=f"{answers[0]}"
                option2=f"{answers[1]}"
                option3=f"{answers[2]}"
                #r = requests.get("http://google.com/search?q=" + question)
#                soup = BeautifulSoup(r.text, 'html.parser')
#                response = soup.find_all("span", class_="st")
#                res = str(r.text)
#                countoption1 = res.count(option1)
#                countoption2 = res.count(option2)
#                countoption3 = res.count(option3)
#                maxcount = max(countoption1, countoption2, countoption3)
#                sumcount = countoption1+countoption2+countoption3
#                print("/n")
#                p = requests.get("http://google.com/search?q=" + question + option1 + option2 + option3 )
#                soup2 = BeautifulSoup(p.text, 'html.parser')
#                response2 = soup2.find_all("span", class_="st")
#                res2 = str(p.text)
#                countoption4 = res2.count(option1)
#                countoption5 = res2.count(option2)
#                countoption6 = res2.count(option3)
                
                #fix = question.replace(" ", "+")
                #fix1 = option1.replace(" ", "+")
                #fix2 = option2.replace(" ", "+")
                #fix3 = option3.replace(" ", "+")
                #url = f"https://www.google.com/search?q={fix}" 
                #req = requests.get(url)
                #sor = BeautifulSoup(req.text, "html.parser")
                #text = sor.text
                
                #abc = option1.split(" ")
                #option1Counts = ""
                #option1Total = 0
                #for x in abc:
                #    countop = text.count(x)
                #    option1Counts+= f"({countop}) {x} "
                #    option1Total+= countop
                #print(option1Counts)
                #print("Total:", option1Total)


                #abc2 = option2.split(" ")
                #for x in abc2:
                #	countop=text.count(x)
                #	hook.send(f"{countop} {x}")


                #abc3 = option3.split(" ")
                #for x in abc3:
                #	countop=text.count(x)
                #	hook.send(f"{countop} {x}")

                stopwords = ['what', 'is', 'a', 'at', 'is', 'he','not','who','never','?','has','will','could']
                querywords = question.split()
                resultwords  = [word for word in querywords if word.lower() not in stopwords]
                result = ' '.join(resultwords)

                quesoroption = result + "(" + option1 + " or " + option2 + " or " + option3 + ")"
                #quesoroption = result + option1 + " " + option2 + " " + option3 
                fix = quesoroption.replace(" ", "+")
                url = f"https://www.google.com/search?q={fix}" 
                req = requests.get(url)
                sor = BeautifulSoup(req.text, "html.parser")
                text = sor.text
                abc = option1.split(" ")
                option1Counts = ""
                option1Total = 0
                for x in abc:
                    countop = text.count(x)
                    option1Counts+= f"({countop}) {x} "
                    option1Total+= countop
                #print(option1Counts)
                #print("Total:", option1Total)
                
                    
                abc2 = option2.split(" ")
                option2Counts = ""
                option2Total = 0
                for x in abc2:
                    countop = text.count(x)
                    option2Counts+= f"({countop}) {x} "
                    option2Total+= countop
                #print(option2Counts)
                #print("Total:", option2Total)

                abc3 = option3.split(" ")
                option3Counts = ""
                option3Total = 0
                for x in abc3:
                    countop = text.count(x)
                    option3Counts+= f"({countop}) {x} "
                    option3Total+= countop
                #print(option3Counts)
                #print("Total:", option3Total)



                
                maxcount = max(option1Total, option2Total, option3Total)              
                if option1Total == maxcount:
                    embed2=discord.Embed(title=f"QHvia Result : (A)",description=f"{answers[0]}: **{option1Counts}**\nTotal - **{option1Total}** \n\n{answers[1]}: **{option2Counts}**\nTotal - **{option2Total}** \n\n{answers[2]}: **{option3Counts}**\nTotal - **{option3Total}** \n\n",color = 0xff00ff)
                    embed2.set_footer(text="❰ Mℜ. M✪D̷丂❱ | Trivia Evil Cats")
                    hook.send(embed=embed2)
                    
                elif option2Total == maxcount:
                    embed2=discord.Embed(title=f"QHvia Result : (B)",description=f"{answers[0]}: **{option1Counts}**\nTotal - **{option1Total}** \n\n{answers[1]}: **{option2Counts}**\nTotal - **{option2Total}** \n\n{answers[2]}: **{option3Counts}**\nTotal - **{option3Total}** \n\n",color = 0x0000ff)
                    embed2.set_footer(text="❰ Mℜ. M✪D̷丂❱ | Trivia Evil Cats")
                    hook.send(embed=embed2)
                    
                elif option3Total == maxcount:
                    embed2=discord.Embed(title=f"QHvia Result : (C)",description=f"{answers[0]}: **{option1Counts}**\nTotal - **{option1Total}** \n\n{answers[1]}: **{option2Counts}**\nTotal - **{option2Total}** \n\n{answers[2]}: **{option3Counts}**\nTotal - **{option3Total}** \n\n",color = 0xff00ff)
                    embed2.set_footer(text="❰ Mℜ. M✪D̷丂❱ | Trivia Evil Cats")
                    hook.send(embed=embed2)
                else :
                    embed2=discord.Embed(title=f"QHvia Result : (Same Result)",description=f"{answers[0]}: **{option1Counts}**\nTotal - **{option1Total}** \n\n{answers[1]}: **{option2Counts}**\nTotal - **{option2Total}** \n\n{answers[2]}: **{option3Counts}**\nTotal - **{option3Total}** \n\n",color = 0x00ffff)   
                    embed2.set_footer(text="❰ Mℜ. M✪D̷丂❱ | Trivia Evil Cats")
                    hook.send(embed=embed2)

            elif message_data["type"] == "questionSummary":

                answer_counts = {}
                correct = ""
                for answer in message_data["answerCounts"]:
                    ans_str = unidecode(answer["answer"])

                    if answer["correct"]:
                        correct = ans_str
                advancing = message_data['advancingPlayersCount']
                eliminated = message_data['eliminatedPlayersCount']
               # nextcheck = message_data['nextCheckpointIn']
                stats = f"Correct : {correct} \nCorrect Users : {advancing} \nWrong Users: : {eliminated}"
                hook.send(stats)
            


"""
def open_browser(question):

    main_url = "https://www.google.co.in/search?q=" + question
    webbrowser.open_new(main_url)
"""

def get_auth_token():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "BTOKEN.txt"), "r") as conn_settings:
        settings = conn_settings.read().splitlines()
        settings = [line for line in settings if line != "" and line != " "]

        try:
            auth_token = settings[0].split("=")[1]
        except IndexError:
            print('No Key is given!')
            return 'NONE'

        return auth_token

while True:
    if show_active():
        url = get_socket_url()
        #print('Connecting to Socket : {}'.format(url))
        #hook.send('Connecting to Socket : {}'.format(url))

        token = get_auth_token()
        if token == 'NONE':
            print('Please enter a valid auth token.')
        else:
            connect_websocket(url, token)

    else:
        show_not_on()
        time.sleep(300)
