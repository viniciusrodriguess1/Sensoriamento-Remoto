#include <WiFi.h>

// Definições de pinos 
#define SensorBoia 32
#define LedVermelho 2
#define LedVerde 4
#define ph_pin 34

// Rede Wi-Fi
const char* ssid = "wifi";
const char* password = "senha";

// Servidor
const char* server_ip = "192.168.1.102";
const uint16_t server_port = 8081;

WiFiClient client;

int ultimoEstadoBoia = -1;
bool pH_fora_faixa = false;

void setup() {
  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi conectado!");
  Serial.print("IP local: ");
  Serial.println(WiFi.localIP());

  pinMode(SensorBoia, INPUT);
  pinMode(LedVermelho, OUTPUT);
  pinMode(LedVerde, OUTPUT);
}

void loop() {
  int leituraPH = analogRead(ph_pin);
  double voltage = 3.3 / 4095.0 * leituraPH;  // ESP32: 3.3V, 12 bits
  float Po = 7 + ((2.5 - voltage) / 0.18);

  int leituraBoia = digitalRead(SensorBoia);
  String statusBoia = (leituraBoia == HIGH) ? "ALTO" : "BAIXO";

  if ((Po > 9 || Po < 3) && !pH_fora_faixa) {
    Serial.println("ALERTA: pH fora da faixa segura!");
    Serial.print("Valor do pH: ");
    Serial.println(Po, 2);
    pH_fora_faixa = true;
  }

  if ((Po >= 3 && Po <= 9) && pH_fora_faixa) {
    Serial.println("O pH voltou à faixa segura.");
    Serial.print("Valor do pH: ");
    Serial.println(Po, 2);
    pH_fora_faixa = false;
  }

  if (leituraBoia != ultimoEstadoBoia) {
    String mensagem = "{\"ph\": " + String(Po, 2) +
                      ", \"voltagem\": " + String(voltage, 3) +
                      ", \"boia\": " + String(leituraBoia) +
                      ", \"status\": \"" + statusBoia + "\"" +
                      ", \"dispositivo_id\": 2}";

    Serial.println("Enviando: " + mensagem);

    if (client.connect(server_ip, server_port)) {
      client.println(mensagem);
      client.stop();
    } else {
      Serial.println("Falha ao conectar ao servidor.");
    }

    ultimoEstadoBoia = leituraBoia;

    digitalWrite(LedVerde, leituraBoia == HIGH ? HIGH : LOW);
    digitalWrite(LedVermelho, leituraBoia == HIGH ? LOW : HIGH);
  }

  delay(2000);
}