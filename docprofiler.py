import asyncio
from timeit import default_timer
import requests
from aiohttp import ClientSession
import re
import time


json_data = {}

total_asynchronous_time = 0.0
total_synchronous_time = [0]

time_by_sifrank = [0]
time_by_flairner = [0] 
time_by_tagme = [0]
time_by_textrank = [0]

def demo_async(urls):
    """Fetch list of web pages asynchronously."""
    loop = asyncio.get_event_loop() # event loop
    future = asyncio.ensure_future(fetch_all(urls,time_by_sifrank,time_by_flairner,time_by_tagme,time_by_textrank,total_asynchronous_time,total_synchronous_time)) # tasks to do
    loop.run_until_complete(future) # loop until done
    
async def fetch_all(urls,time_by_sifrank,time_by_flairner,time_by_tagme,time_by_textrank,total_asynchronous_time,total_synchronous_time):
    """Launch requests for all web pages."""
    tasks = []
    fetch.start_time = dict() # dictionary of start times for each url
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session,time_by_sifrank,time_by_flairner,time_by_tagme,time_by_textrank))
            tasks.append(task) # create list of tasks
        r = await asyncio.gather(*tasks) # gather task responses
        print(r)
        text_sum=entities_tagme=GPE=ORG=PERSON=EVENT=DATE=MONEY=NORP=LOC=ADDITIONAL = ""
        keyphrases = []
        for i in r:
            import json
            i = json.loads(i.decode('utf-8')) 
            for k,v in i.items():
                if k == "Summary":
                    text_sum = v
                elif k == "Entities":
                    entities_tagme = v
                elif k == "Kephrases":
                    kp = [x[0] for x in v]
                    kp = list(set(kp))
                    keyphrases = kp
                elif k == "GPE":
                    GPE = v
                elif k == "ORG":
                    ORG = v
                elif k == "PERSON":
                    PERSON = v
                elif k == "EVENT":
                    EVENT = v
                elif k == "DATE":
                    DATE = v
                elif k == "MONEY":
                    MONEY = v
                elif k == "NORP":
                    NORP = v
                elif k == "LOC":
                    LOC = v
                elif k == "ADDITIONAL":
                    ADDITIONAL = v
        global json_data
        json_data = {
            'Entities': entities_tagme,
            'Keyphrases': keyphrases,
            'Summary': text_sum.strip().replace("\n", " ").replace("\r", " ").replace("\t", " "),
            'GPE' : GPE,
            'ORG' : ORG,
            'PERSON': PERSON,
            'LOC': LOC,
            'NORP': NORP,
            'EVENT' : EVENT,
            'DATE': DATE,
            'MONEY': MONEY,
            'ADDITIONAL' : ADDITIONAL

        } 
        #print(json_data)

async def fetch(url, session,time_by_sifrank,time_by_flairner,time_by_tagme,time_by_textrank):
    """Fetch a url, using specified ClientSession."""
    fetch.start_time[url] = default_timer()
    
    async with session.post(url,json = {"text":data,"no_of_keyphrases":number_of_keyphrases,"sifrank_algo":sifrank_algo,"summary_words":summary_words,"summary_ratio":summary_ratio,"tagme_score":tagme_score,"tagme_token_api":tagme_token_api}) as response:
        resp = await response.read()
        
        elapsed = default_timer() - fetch.start_time[url]
        if 'getKeyphrases' in url:
            time_by_sifrank.append(elapsed)
        elif 'flairner' in url:
            time_by_flairner.append(elapsed)
        elif 'tagme' in url:
            time_by_tagme.append(elapsed)
        elif 'getSummaryByRatio' in url:
            time_by_textrank.append(elapsed)
        return resp

def generate_profile(textdata,URL_LIST,no_of_keyphrases,sifrankalgo,summarywords,summaryratio,tagmescore,tagmetokenapi):
    #asyncio.set_event_loop(asyncio.new_event_loop())
    global data 
    global number_of_keyphrases
    global sifrank_algo
    global summary_words
    global summary_ratio
    global tagme_score
    global tagme_token_api
    number_of_keyphrases = no_of_keyphrases
    data = textdata
    sifrank_algo = sifrankalgo
    summary_words = summarywords
    summary_ratio =summaryratio
    tagme_score =tagmescore
    tagme_token_api = tagmetokenapi
    print(URL_LIST)
    start_time = default_timer()
    demo_async(URL_LIST)
    tot_elapsed = default_timer() - start_time
    return json_data,tot_elapsed
    
#s,tt = generate_profile(data_a,URL_LIST = ['http://127.0.0.1:5002/tagme','http://127.0.0.1:5003/textrank'],no_of_keyphrases=10)
#print(s)
#print(tt)

#text = "THREE WEEKS ago, Phil Morgan, head of the financial-services initiative at the Welsh Development Agency, took an exhibition to Bristol, to 'sell' to that city's business community the attractions of relocating in south-east Wales. Although the day-long event was one of a series that will shortly go to Reading and then to places along the M25 corridor around London, the Bristol visit touched a raw nerve. Relations have never been good between Bristol and South Wales, and the English city resented what it saw as the seduction of one of its own growth industries. The move illustrates the aggressive policy that is being followed in order to attract financial-services companies to South Wales. Cardiff, as the main centre for the sector in south-east Wales, has never had a particularly strong indigenous financial industry. Before Mr Peter Walker, then secretary of state for Wales, launched his financial services initiative to build the city's financial nexus three years ago, effectively all that the Welsh capital had to offer was: the Bank of Wales, set up in the 1972; one medium-sized building society, the Principality, 28th in the societies' pecking order; the venture capital group, 3i; and one major incomer, Chemical Bank. Mr Walker's initiative had immediate results. NM Rothschild has been the five-star name to arrive, but others - including National Provident Institution, Banque Nationale de Paris, Axa, the French insurance giant, Willis Wrightson (also in insurance), and stockbrokers Bell, Lawrie, White - have strengthened the sector. While this financial muscle has greatly added to the city's commercial depth, it has not yet turned Cardiff into an important financial centre. 'You still have to look at Cardiff as an emerging financial city,' says Peter Davies, Rothschild's director of corporate finance in Wales. 'It is not possible to get institutional support for a major issue, and if a growing business wants to raise equity capital, it has really only one choice - 3i.' Rothschild's own venture fund is based in London, and of two attempts by the WDA to set up funds, the Cardiff Consortium came to nothing and the Welsh Venture Capital Fund was eventually closed. That situation is about to change. Meirion Thomas, an executive director of the WDA, says that a new fund, Venture Link, is raising Pounds 5m from Welsh institutions, such as the local-authority pension funds, and expects to be in business within the next few months. Venture Link, which has two other funds in Britain, has opened an office in Cardiff, and will gear its lending to the bottom end of the market, offering capital between Pounds 25,000 and Pounds 150,000. 'The signs are that people within Wales are looking much more to institutions within the country for their needs,' says Mr Thomas. 'The Bank of Wales, for instance, is getting more into the risk-capital business, and that is encouraging.' Venture Link is not the only one interested in Cardiff. Credit Lyonnais, the French bank, having already opened a dozen regional centres in Britain, is considering an office in Cardiff, which it currently serves from Bristol through a former WDA official. Other entrants are in the pipeline, according to Mr Morgan. At 3i, Nigel Guy, the Cardiff director, says there is plenty of money for lending, but that the city lacks a large corporate base, such as that of the West Midlands, to sustain a major financial sector. Last year, 3i completed Pounds 18m of business in 50 investments, but the 12 months to March 1991 'was not so good. The position in Cardiff reflected what is happening in the rest of the UK economy.' Even so, Mr Guy says there is considerable interest in management buy-outs, boosted by companies drawing back into their core activities and seeking to sell what they see as peripheral businesses. 'There has been an upsurge in interest in this sector in the past four months,' he says, 'including a couple of seven-figure deals, such as that at British Rotatherm, which was bought from its Scandinavian parents.' This activity encourages Mr Morgan at the financial services initiative, who says that the 'temperature is still good, despite the recession. The downturn in the City of London provides us in Cardiff with an opportunity to attract firms to a location that provides them with a better cost base. Both wage and salary levels, and property prices, are much more attractive here than in the south east of England.' Mr Morgan has been aiming particularly at the insurance companies, such as Axa, believing that, as the continental concerns grow increasingly larger in preparation for the single market in 1992, they will want to have national networks of offices. 'We want them to look at Cardiff and the rest of south-east Wales as a potential location,' he says, offering the example of DAS, a German concern, which late last year opened an office in Bedwas, between Cardiff and Newport. 'A number of overseas banks, such as Credit Agricole and Paribas, of France, and the Canadian Imperial Bank of Commerce, have already financed deals in Wales. 'The electronics-based Gooding Group has Japan's C Itoh and the American Citibank among its major shareholders; and with this level of interest, I am convinced we shall be seeing major banks of their standing actually opening offices in Cardiff before long."
#data,final_time = generate_profile(text, URL_LIST=['http://3.236.47.53:5001/flairner','http://127.0.0.1:5030/textrank','http://127.0.0.1:5020/tagme','http://3.236.47.53:5000/sifrank'],no_of_keyphrases=10)
#print(data)
#text = "THREE WEEKS ago, Phil Morgan, head of the financial-services initiative at the Welsh Development Agency, took an exhibition to Bristol, to 'sell' to that city's business community the attractions of relocating in south-east Wales. Although the day-long event was one of a series that will shortly go to Reading and then to places along the M25 corridor around London, the Bristol visit touched a raw nerve. Relations have never been good between Bristol and South Wales, and the English city resented what it saw as the seduction of one of its own growth industries. The move illustrates the aggressive policy that is being followed in order to attract financial-services companies to South Wales. Cardiff, as the main centre for the sector in south-east Wales, has never had a particularly strong indigenous financial industry. Before Mr Peter Walker, then secretary of state for Wales, launched his financial services initiative to build the city's financial nexus three years ago, effectively all that the Welsh capital had to offer was: the Bank of Wales, set up in the 1972; one medium-sized building society, the Principality, 28th in the societies' pecking order; the venture capital group, 3i; and one major incomer, Chemical Bank. Mr Walker's initiative had immediate results. NM Rothschild has been the five-star name to arrive, but others - including National Provident Institution, Banque Nationale de Paris, Axa, the French insurance giant, Willis Wrightson (also in insurance), and stockbrokers Bell, Lawrie, White - have strengthened the sector. While this financial muscle has greatly added to the city's commercial depth, it has not yet turned Cardiff into an important financial centre. 'You still have to look at Cardiff as an emerging financial city,' says Peter Davies, Rothschild's director of corporate finance in Wales. 'It is not possible to get institutional support for a major issue, and if a growing business wants to raise equity capital, it has really only one choice - 3i.' Rothschild's own venture fund is based in London, and of two attempts by the WDA to set up funds, the Cardiff Consortium came to nothing and the Welsh Venture Capital Fund was eventually closed. That situation is about to change. Meirion Thomas, an executive director of the WDA, says that a new fund, Venture Link, is raising Pounds 5m from Welsh institutions, such as the local-authority pension funds, and expects to be in business within the next few months. Venture Link, which has two other funds in Britain, has opened an office in Cardiff, and will gear its lending to the bottom end of the market, offering capital between Pounds 25,000 and Pounds 150,000. 'The signs are that people within Wales are looking much more to institutions within the country for their needs,' says Mr Thomas. 'The Bank of Wales, for instance, is getting more into the risk-capital business, and that is encouraging.' Venture Link is not the only one interested in Cardiff. Credit Lyonnais, the French bank, having already opened a dozen regional centres in Britain, is considering an office in Cardiff, which it currently serves from Bristol through a former WDA official. Other entrants are in the pipeline, according to Mr Morgan. At 3i, Nigel Guy, the Cardiff director, says there is plenty of money for lending, but that the city lacks a large corporate base, such as that of the West Midlands, to sustain a major financial sector. Last year, 3i completed Pounds 18m of business in 50 investments, but the 12 months to March 1991 'was not so good. The position in Cardiff reflected what is happening in the rest of the UK economy.' Even so, Mr Guy says there is considerable interest in management buy-outs, boosted by companies drawing back into their core activities and seeking to sell what they see as peripheral businesses. 'There has been an upsurge in interest in this sector in the past four months,' he says, 'including a couple of seven-figure deals, such as that at British Rotatherm, which was bought from its Scandinavian parents.' This activity encourages Mr Morgan at the financial services initiative, who says that the 'temperature is still good, despite the recession. The downturn in the City of London provides us in Cardiff with an opportunity to attract firms to a location that provides them with a better cost base. Both wage and salary levels, and property prices, are much more attractive here than in the south east of England.' Mr Morgan has been aiming particularly at the insurance companies, such as Axa, believing that, as the continental concerns grow increasingly larger in preparation for the single market in 1992, they will want to have national networks of offices. 'We want them to look at Cardiff and the rest of south-east Wales as a potential location,' he says, offering the example of DAS, a German concern, which late last year opened an office in Bedwas, between Cardiff and Newport. 'A number of overseas banks, such as Credit Agricole and Paribas, of France, and the Canadian Imperial Bank of Commerce, have already financed deals in Wales. 'The electronics-based Gooding Group has Japan's C Itoh and the American Citibank among its major shareholders; and with this level of interest, I am convinced we shall be seeing major banks of their standing actually opening offices in Cardiff before long."
#data,final_time = generate_profile(text, URL_LIST=['http://34.211.28.139:5001/flairner', 'http://34.211.28.139:5000/sifrank', 'http://34.211.28.139:5003/textrank', 'http://localhost:5005/dbpedia'],no_of_keyphrases=10,entity_linking_dbpedia_sc=0.6,dbped_host_url="http://34.211.28.139:8080/rest/candidates")
#print(data)