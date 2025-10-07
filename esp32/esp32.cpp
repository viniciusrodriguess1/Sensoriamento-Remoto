#include <WiFi.h>
#include <HTTPClient.h>

// --- Configurações de Rede ---
// Dados da rede Wi-Fi
const char* ssid = "DIGITAL-João"; // Substitua pelo seu SSID, se necessário
const char* password = "29102002"; // Substitua pela sua senha, se necessário

// IP e porta do computador onde está rodando o FastAPI (Endpoint completo)
// Usar 'http://' é crucial para o HTTPClient
const char* serverName = "http://192.168.1.103:8001/api/v1/estados-luz";

// --- Configurações de Hardware ---
#define LED_PIN 2           // Pino do LED (Normalmente o LED_BUILTIN no ESP32 é o pino 2)
bool estadoLED = false;     // Variável para rastrear o estado atual do LED

// --- Configurações de Temporização ---
const unsigned long INTERVALO_ENVIO = 10000; // Intervalo de envio em milissegundos (10 segundos)
unsigned long ultimoEnvio = 0;              // Variável para armazenar o tempo do último envio

// ------------------------------------
// Função para tentar reconectar ao Wi-Fi
// ------------------------------------
void conectarWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    return; // Já está conectado
  }

  Serial.println("\nTentando conectar ao Wi-Fi...");
  WiFi.begin(ssid, password);
  
  // Tenta conectar por no máximo 30 segundos (60 iterações de 500ms)
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 60) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWi-Fi conectado!");
    Serial.print("Endereço IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFalha na conexão Wi-Fi. Tentando novamente no loop.");
  }
}

// ------------------------------------
// SETUP
// ------------------------------------
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, estadoLED ? HIGH : LOW); // Garante que o LED comece no estado inicial

  conectarWiFi(); // Tenta conectar no início
}

// ------------------------------------
// LOOP
// ------------------------------------
void loop() {
  // Chamamos a função de conexão a cada loop para garantir que ele tente reconectar
  // se a conexão cair após o setup
  conectarWiFi(); 

  // Utiliza a técnica "millis()" para não bloquear o código com "delay()"
  // Isso permite que outras tarefas (futuras) sejam executadas
  if (millis() - ultimoEnvio >= INTERVALO_ENVIO) {
    ultimoEnvio = millis(); // Atualiza o tempo do último envio

    // 1. ALTERNA O ESTADO DO LED
    estadoLED = !estadoLED;
    digitalWrite(LED_PIN, estadoLED ? HIGH : LOW);

    // 2. ENVIA O ESTADO POR HTTP
    if (WiFi.status() == WL_CONNECTED) {
      // Cria uma instância de HTTPClient localmente
      HTTPClient http;
      
      // Inicia a conexão HTTP
      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      // Monta o JSON
      String estadoStr = estadoLED ? "ligado" : "desligado";
      String jsonData = "{\"estado\":\"" + estadoStr + "\"}";

      Serial.println("\n----------------------------------");
      Serial.println("Enviando dados para o servidor:");
      Serial.println(jsonData);

      // Faz a requisição POST
      int httpResponseCode = http.POST(jsonData);

      if (httpResponseCode > 0) {
        // HTTP 200 (OK), 201 (Created), etc.
        Serial.print("Código de resposta HTTP: ");
        Serial.println(httpResponseCode);
        Serial.print("Resposta do servidor: ");
        Serial.println(http.getString());
      } else {
        // Códigos negativos indicam erro de conexão ou protocolo
        Serial.print("Erro na requisição HTTP (Código): ");
        Serial.println(httpResponseCode);
        Serial.print("Detalhe do Erro: ");
        Serial.println(http.errorToString(httpResponseCode));
      }

      // Fecha a conexão HTTP
      http.end();
    } else {
      Serial.println("Erro: Wi-Fi desconectado. Não foi possível enviar.");
    }
    Serial.println("----------------------------------");
  }
}