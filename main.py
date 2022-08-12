import json
import numpy
import websocket
import talib
SOCKET="wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
SlowEma_Period=28
FastEma_Period=9

TradeSymbol='ETHUSDT'
TradeQuantity=0.02
TradeQuantityRisk=0.01

closes = [] #kapanış değerlerini tutuyor
lowes = [] #en düşük değerlerini tutuyor
highes = [] #en yüksek değerlerini tutuyor

in_position= False
cuzdan = 1000
alimSayisi = 0
satimSayisi = 0
toplamCoin = 0
komisyon=75/10000
verilenKomisyon=0

def buy_or_sell(FastEma,SlowEma,stotastic):
    global in_position
    global cuzdan
    global alimSayisi
    global satimSayisi
    global toplamCoin
    global komisyon
    global verilenKomisyon

    if FastEma[-1] > SlowEma[-1] and in_position == False:
        if FastEma[-2] < SlowEma[-2]:
            print("### GOLDEN CROSS ###")
            if stotastic.values[-14][0] > stotastic.values[-14][1]:
                if stotastic.values[-14][0] > 39 and stotastic.values[-14][0] < 65:
                    print(" ")
                    print("*** Alış ***")
                    in_position = True
                    print(f"cüzdan : {cuzdan}")
                    print(cuzdan/closes[-1], " adet ETH alındı. ETH alış fiyatı : ", closes[-1])
                    satimSayisi +=1
                    cuzdan -= komisyon*cuzdan
                    toplamCoin = cuzdan/closes[-1]
                    verilenKomisyon+= komisyon*cuzdan

                    '''tahtaya for(2,50,2) 
                    toplamCoin*0.02 
                    closes[-1]^1.02 şeklinde yazdır'''
                if stotastic.values[-14][0] > 64 and stotastic.values[-14][0] < 80:
                    print(" ")
                    print("*** Alış Stoctastic yuksek***")
                    in_position = True
                    print(f"cüzdan : {cuzdan}")
                    print(cuzdan / closes[-1], " adet ETH alındı. ETH alış fiyatı : ", closes[-1])
                    satimSayisi += 1
                    cuzdan -= komisyon * cuzdan
                    toplamCoin = cuzdan / closes[-1]
                    verilenKomisyon += komisyon * cuzdan

                    '''tahtaya for(2,50,2) 
                    toplamCoin*0.02 
                    closes[-1]^1.02 şeklinde yazdır'''
                elif stotastic.values[-14][0]>79:
                    print("Stotastic çok yuksek alım yapılamaz")
                else:
                    print("Stotastic çok düşük alım yapılamaz")
            else:
                print("Stotastic alıma uygun değil")

    if in_position==True:
        if FastEma[-1]<SlowEma[-1] and FastEma[-2]>SlowEma[-2]:
            print("*** Satış ***")
            print("Ema satış verdi.")
            print("Tüm emirler iptal edildi")
            satimSayisi+=1
            cuzdan= closes[-1]*toplamCoin
            toplamCoin=0
            verilenKomisyon+=komisyon*cuzdan
            print(f"işlemler sonunda toplam cüzdan : {cuzdan}")
            print("#############################################")




def on_open(ws):
    print("baglantı saglandi")

def on_close(ws):
    print("baglantı koptu")

def on_message(ws,message):
    json_message=json.loads(message)
    candle=json_message['k']
    candle_Close=candle['c']
    candle_Open=candle['o']
    candle_High=candle['h']
    candle_Low=candle['l']

    is_candle_closed=candle['x']

    if is_candle_closed:
        print("is_candle_closed :" , candle_Close)


        closes.append(float(candle_Close))
        highes.append(float(candle_High))
        lowes.append(float(candle_Low))
        print(closes)
        if len(closes)<28:
            np_closes=numpy.array(closes)
            np_lowes=numpy.array(lowes)
            np_highes=numpy.array(highes)

            FastEmaList = talib.EMA(np_closes, FastEma_Period)
            FastEma = FastEmaList[-1]
            SlowEmaList = talib.EMA(np_closes, SlowEma_Period)
            SlowEma = SlowEmaList[-1]
            StotasticList=numpy.STOCH(np_highes,np_lowes,np_closes,smooth_k=3,k=14)
            Stotastic_A=StotasticList[-14][0]
            Stotastic_B=StotasticList[-14][1]
            print("Stotastic_A",Stotastic_A)
            print("Stotastic_B",Stotastic_B)


        buy_or_sell(FastEma,SlowEma)#,SlowEma,stotastic)





ws=websocket.WebSocketApp(SOCKET,on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()
