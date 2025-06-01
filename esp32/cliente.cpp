#include <WiFi.h>

// Substitua com sua rede Wi-Fi
const char* ssid = "DIGITAL-GABRIEL";
const char* password = "07102017";

// IP e porta do servidor TCP (ajuste conforme necessário)
const char* server_ip = "192.168.0.100"; // IP do seu servidor (por exemplo, computador local)
const uint16_t server_port = 5001;

WiFiClient client;

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
}

void loop() {
  if (client.connect(server_ip, server_port)) {
    String message = "Mensagem do ESP32: " + String(random(1000,9000));
    client.println(message);
    Serial.println("Mensagem enviada: " + message);
    client.stop();
  } else {
    Serial.println("Falha ao conectar ao servidor.");
  }

  delay(5000); // Envia uma mensagem a cada 5 segundos
}