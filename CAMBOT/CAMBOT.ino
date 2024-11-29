#include <ArduinoJson.h>
#include <robo_hardware2.h> 
#include <Servo.h>

float X;

void setup() {
  Serial.begin(9600); 
  robo.configurar();
}

void loop() {
  //Envia o pedido das coordenadas
  Serial.println("GET_COORDS");
  
  //Espera receber a quantidade de círculos a serem enviados
  while(!Serial.available()){
  }

  //Lê o json com a quantidade de círculos
  String json = Serial.readString();
  
  //Inicializa o buffer do json
  DynamicJsonDocument doc(1024);

  //Desemcapsula o json
  DeserializationError error = deserializeJson(doc, json);
  
  //Tratamento de erro pra deserialização
  if (error) {
      Serial.print(F("Falha ao deserializar JSON: "));
      Serial.println(error.f_str());
      return;
  }
  
  //Pega o valor da quantidade de círculos
  int QTDcirculos = doc["numCirculos"];

  //Para cada círculo a ser enviado
  for (int i = 1; i <= QTDcirculos; i++ ){
    //Envia informando que está pronto para receber o círculo
    Serial.println("GET");
    
    //Lê o json com os circulos
    String Circulo = Serial.readString();

    Serial.print("Arduino :");
    Serial.println(Circulo);

    if (QTDcirculos == 1){
        DynamicJsonDocument docCirculo(1024);

        //Desemcapsula o json
        DeserializationError error = deserializeJson(docCirculo, Circulo);
        
        if (error) {
            Serial.print(F("Falha ao deserializar JSON: "));
            Serial.println(error.f_str());
            return;

        }
        
        X = docCirculo["xy"]["x"];

        Serial.print("Arduino Cord:");
        Serial.println(X);

        if(X<30 && X>-30){
          robo.acionarMotores(0,0);
          delay(100);
        }
        else if (X<0){
          robo.acionarMotores(100, 0);
          delay(100);
        }
        else if (X>0){
          robo.acionarMotores(0, 100);
          delay(100);
        }
        
        else{
          robo.acionarMotores(0,0);
        }

        robo.acionarMotores(0,0);
    }
    
    
  }

  //Espera 5 minutos para o próximo pedido
  // delay(100);
}
