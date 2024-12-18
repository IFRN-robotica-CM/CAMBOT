#impotação de bibliotecas de visão computacional, json e serial
import cv2
import numpy as np
import json
import serial
import time

#definição das funções de detecção e envio dos círculos
def detectarCirculosImagem(video):
    #Inicializa a lista de circulos encontrados
    circulos = []

    #Lê um quadro do vídeo
    ret, frame = video.read()
    
    #Se o vídeo não for encontado mostra mensagem de erro
    if not ret:
        print("Erro ao ler o vídeo.")
        cap.release()
        return

    #Converte o quadro para escalas de cinza
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Aplica um desfoque para reduzir ruídos que possam existir
    img_blur = cv2.medianBlur(img_gray, 5)

    # Detectar círculos usando a Transformada de Hough
    circles = cv2.HoughCircles(img_blur, 
                               cv2.HOUGH_GRADIENT, 
                               dp=1, 
                               minDist=70, 
                               param1=70, 
                               param2=35, 
                               minRadius=10, 
                               maxRadius=0)

    # Verificar se algum círculo foi encontrado
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        num_circles = 1
        for i in circles[0, :]:
            #Criar um dicionário para cada círculo
            data = {"id": num_circles, "xy": {"x": 0, "y": 0}, "s": " "}
            num_circles += 1
            
            #Coordenadas do centro e raio do círculo e adiciona no dicionário
            x, y, radius = i[0], i[1], i[2]
            x = int(x)
            
            data["xy"]["x"] = ((x- 320)*5)/16
            data["xy"]["y"] = int(y)
            
            #Garante que o círculo esteja dentro dos limites da imagem
            x1, x2 = max(0, x-radius), min(frame.shape[1], x+radius)
            y1, y2 = max(0, y-radius), min(frame.shape[0], y+radius)
            
            #Calcula a cor média dentro do círculo
            avg_color = np.mean(frame[y1:y2, x1:x2], axis=(0, 1))
            
            #Verifica se a cor média é próxima de preto
            if np.all(avg_color < 60):
                cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)
                #Adiciona o status da vítima como morta
                data["s"] = "dead"

            #Se não for preto
            else:
                cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
                #Adiciona o status da vítima como viva
                data["s"] = "alive"
            
            # Adicionar o dicionário do circulo à lista de circulos encontrados
            circulos.append(data)
   
    #Retorna uma lista de todos os dicionarios com as bolas
    return circulos


def EnviarCirculos(circulos, serial):
    #Envia a quantidade de círculos a serem enviados 
    qtd = len(circulos)
    temp = json.dumps({"numCirculos":qtd})
    serial.write(temp.encode("utf-8"))
    
    #Para ca circulo encontrado
    for circulo in circulos:
        #espera o Arduino dizer que está pronto para receber
        message = ser.readline().decode('utf-8').strip()
        print(message)

        #Enquanto ele não pedir as cordenadas espere ele pedir
        while not(message == 'GET'):
            message = ser.readline().decode('utf-8').strip()
            print(message)
            print('waiting ...')

        #Se o Arduino está pronto para receber os dados do círculo 

        #Serializa para o formato json
        circle = json.dumps(circulo)
        #Envia pela serial
        serial.write(circle.encode('utf-8'))

        #Mostra mensagem de recebimento do Arduino
        message = ser.readline().decode('utf-8').strip()
        print(message)        

#Execução do script

#Inicializa a camera
cap = cv2.VideoCapture(0)

try:
    #Inicializa a serial para comunicação com o Arduino
    ser = serial.Serial('/dev/ttyUSB0',9600)
    time.sleep(2)
except:
    ser = serial.Serial('/dev/ttyUSB1',9600)
    time.sleep(2)
#Inicia como "escravo" esperando o Arduino pedir os dados
while True:
    message = ser.readline().decode('utf-8').strip()
    print(message)
    
    if message == 'GET_COORDS':
        
        cordenadas = detectarCirculosImagem(cap)
        EnviarCirculos(cordenadas, ser)
        
cap.release()
        
