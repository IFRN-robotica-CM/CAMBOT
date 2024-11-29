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

  //Lê o json com o circulo
  String Circulo = Serial.readString();

  Serial.print("Arduino :");
  Serial.println(Circulo);

  //   if (QTDcirculos == 1){
  //       DynamicJsonDocument docCirculo(1024);

  //       //Desemcapsula o json
  //       DeserializationError error = deserializeJson(docCirculo, Circulo);
        
  //       if (error) {
  //           Serial.print(F("Falha ao deserializar JSON: "));
  //           Serial.println(error.f_str());
  //           return;

  //       }
        
  //       X = docCirculo["xy"]["x"];

  //       Serial.print("Arduino Cord:");
  //       Serial.println(X);

  //       if(X<30 && X>-30){
  //         robo.acionarMotores(0,0);
  //         delay(100);
  //       }
  //       else if (X<0){
  //         robo.acionarMotores(100, 0);
  //         delay(100);
  //       }
  //       else if (X>0){
  //         robo.acionarMotores(0, 100);
  //         delay(100);
  //       }
        
  //       else{
  //         robo.acionarMotores(0,0);
  //       }

  //       robo.acionarMotores(0,0);
  //   }
    
    
  // }

  //Espera 5 minutos para o próximo pedido
  // delay(100);
}
