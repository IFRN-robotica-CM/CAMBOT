# Importação de bibliotecas necessárias
import cv2
import numpy as np

# Função para detectar círculos na imagem capturada em tempo real
def detectarCirculosImagem(video):
    # Lê um quadro do vídeo
    ret, frame = video.read()
    
    # Verifica se o vídeo foi lido corretamente
    if not ret:
        print("Erro ao ler o vídeo.")
        return [], None

    # Converte o quadro para escala de cinza
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplica desfoque para reduzir ruídos
    img_blur = cv2.medianBlur(img_gray, 5)

    # Detecta círculos usando a Transformada de Hough
    circles = cv2.HoughCircles(img_blur, 
                               cv2.HOUGH_GRADIENT, 
                               dp=1, 
                               minDist=70, 
                               param1=70, 
                               param2=35, 
                               minRadius=10, 
                               maxRadius=0)

    # Lista para armazenar as coordenadas dos círculos detectados
    circulos_detectados = []

    # Verifica se algum círculo foi detectado
    if circles is not None:
        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            # Extrai as coordenadas do centro e o raio do círculo
            x, y, radius = i[0], i[1], i[2]
            
            # Desenha o círculo na imagem para visualização
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)  # Marca o centro
            
            # Adiciona as coordenadas do centro à lista
            circulos_detectados.append({"x": int(x), "y": int(y)})

    # Retorna as coordenadas dos círculos detectados e o quadro
    return circulos_detectados, frame


# Execução do script

# Inicializa a câmera
cap = cv2.VideoCapture(0)

# Inicializa um contador de quadros para reduzir a frequência de exibição
frame_count = 0

# Loop principal para processar o vídeo em tempo real
while True:
    # Detecta os círculos na imagem capturada
    circulos, frame = detectarCirculosImagem(cap)

    # Exibe as coordenadas dos círculos detectados
    if circulos:
        print(f"Círculos detectados: {circulos}")
    
    # Exibe a janela somente a cada 10 quadros
    frame_count += 1
    if frame_count % 10 == 0 and frame is not None:
        cv2.imshow('Detecção de Círculos', frame)

    # Verifica se a tecla 'q' foi pressionada para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera os recursos da câmera e fecha as janelas
cap.release()
cv2.destroyAllWindows()
