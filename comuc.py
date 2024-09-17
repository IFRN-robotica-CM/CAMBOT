import serial
import time

def get_user_input():
    while True:
        choice = input("Deseja ligar ou desligar o LED? (L/D): ").strip().lower()
        if choice in ['l', 'd']:
            return 'ON' if choice == 'l' else 'OFF'
            break
        else:
            print("Escolha inválida. Por favor, digite 'Ligar' ou 'Desligar'.")
            break

def comunicarArduino(posicao):
    # Configura a porta serial (ajuste /dev/ttyUSB0 se necessário)
    ser = serial.Serial('/dev/ttyACM0', 9600) 

    time.sleep(2)  # Aguarda a inicialização do Arduino

    while True:
        
        message = ser.readline().decode().strip()
        if message == "BUTTON_PRESSED":
            print("Botão pressionado no Arduino.")
            user_command = posicao
            ser.write(user_command.encode())
            print(f"Comando enviado para o Arduino: {user_command}")
