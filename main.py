import cv2
import numpy as np
import json
import serial
import time

def detectar_circulos_video(video):
    data_balls = {"n":3, "b": []}

    # Ler um quadro do vídeo
    ret, frame = video.read()
    
    if not ret:
        print("Erro ao ler o vídeo.")
        cap.release()
        return

    # Converter o quadro para escala de cinza
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar um desfoque para reduzir ruídos
    img_blur = cv2.medianBlur(img_gray, 5)

    # Detectar círculos usando a Transformada de Hough
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=70,
                               param1=60, param2=35, minRadius=10, maxRadius=0)

    # Verificar se algum círculo foi encontrado
    if circles is not None:
        circles = np.uint16(np.around(circles))
        
        num_circles = 1
        for i in circles[0, :]:
            # Criar uma nova instância de dicionário para cada círculo
            data = {"id": num_circles, "xy": {"x": 0, "y": 0}, "t": " "}
            num_circles += 1
            
            # Coordenadas do centro e raio do círculo
            x, y, radius = i[0], i[1], i[2]
            
            data["xy"]["x"] = int(x)
            data["xy"]["y"] = int(y)
            
            # Garantir que o círculo esteja dentro dos limites da imagem
            x1, x2 = max(0, x-radius), min(frame.shape[1], x+radius)
            y1, y2 = max(0, y-radius), min(frame.shape[0], y+radius)
            
            # Calcular a cor média dentro do círculo
            avg_color = np.mean(frame[y1:y2, x1:x2], axis=(0, 1))
            
            # Desenhar o círculo encontrado
            cv2.circle(frame, (x, y), 2, (255, 0, 0), 3)
            
            # Verificar se a cor média é próxima de preto
            if np.all(avg_color < 60):
                cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)
                data["t"] = "dead"
            else:
                cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
                data["t"] = "alive"
            
            # Adicionar o dicionário à lista
            data_balls["b"].append(data)
   
    
    # Converter para JSON
    data_json = json.dumps(data_balls)
    return data_json


cap = cv2.VideoCapture(0)

#cordenadas = detectar_circulos_video(cap)
#print(cordenadas)
#cap.release()
ser = serial.Serial('/dev/ttyACM1',115200)
time.sleep(2)

while True:
    message = ser.readline().decode('utf-8').strip()
    
    if message == 'GET_COORDS':
        
        
        cordenadas = detectar_circulos_video(cap)
        ser.write(cordenadas.encode('utf-8'))
        
        print('raspi enviou isso:')
        print(cordenadas)
    else:
        print(message)

cap.release()
        
