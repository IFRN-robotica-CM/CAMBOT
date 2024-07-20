import cv2
import numpy as np

def detectar_circulos(imagem_path):
    # Carregar a imagem
    img = cv2.imread(imagem_path, cv2.IMREAD_COLOR)
    
    # Converter a imagem para escala de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar um desfoque para reduzir ruídos
    img_blur = cv2.medianBlur(img_gray, 5)

    # Detectar círculos usando a Transformada de Hough
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=60, param2=35, minRadius=0, maxRadius=0)

    # Verificar se algum círculo foi encontrado
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # Coordenadas do centro e raio do círculo
            x, y, radius = i[0], i[1], i[2]

            # Calcular a cor média dentro do círculo
            avg_color = np.mean(img[y-radius:y+radius, x-radius:x+radius], axis=(0, 1))

            # Verificar se a cor média é próxima de preto
            if np.all(avg_color < 50):
                # Desenhar o círculo encontrado
                cv2.circle(img, (x, y), radius, (0, 255, 0), 2)
                # # Desenhar o centro do círculo
                # cv2.circle(img, (x, y), 2, (0, 0, 255), 3)

            else:
                # Desenhar o círculo encontrado
                cv2.circle(img, (x, y), radius, (0, 0, 255), 2)

    # Exibir a imagem resultante
    cv2.imshow('Circulos detectados', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def detectar_circulos_video(video_path):
    # Abrir o vídeo
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        # Ler um quadro do vídeo
        ret, frame = cap.read()
        if not ret:
            break

        # Converter o quadro para escala de cinza
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Aplicar um desfoque para reduzir ruídos
        img_blur = cv2.medianBlur(img_gray, 5)

        # Detectar círculos usando a Transformada de Hough
        circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                                   param1=60, param2=35, minRadius=0, maxRadius=0)

        # Verificar se algum círculo foi encontrado
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # Coordenadas do centro e raio do círculo
                x, y, radius = i[0], i[1], i[2]

                # Calcular a cor média dentro do círculo
                avg_color = np.mean(frame[y-radius:y+radius, x-radius:x+radius], axis=(0, 1))

                # Verificar se a cor média é próxima de preto
                if np.all(avg_color < 50):
                    # Desenhar o círculo encontrado
                    cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
                    # # Desenhar o centro do círculo
                    # cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)

                else:
                    # Desenhar o círculo encontrado
                    cv2.circle(frame, (x, y), radius, (0, 0, 255), 2)

        # Exibir o quadro resultante
        cv2.imshow('Circulos detectados', frame)

        # Sair do loop se a tecla 'q' for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar o objeto de captura e fechar todas as janelas OpenCV
    cap.release()
    cv2.destroyAllWindows()

# Exemplo de uso
# detectar_circulos_video('videotest2.mp4')

# Exemplo de uso
detectar_circulos('cinza_preta.jpg')