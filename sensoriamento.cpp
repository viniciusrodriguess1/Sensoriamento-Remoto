#define SensorBoia 10 
#define LedVermelho 11 
#define LedVerde 12 
#define ph_pin A0 

int ultimoEstadoBoia = -1;  // Armazena o último estado do sensor de boia
bool pH_fora_faixa = false; // Flag para verificar se o pH estava fora da faixa

void setup() {
  Serial.begin(9600);
  Serial.println("    Projeto Agua em Ação");

  pinMode(SensorBoia, INPUT);
  pinMode(LedVermelho, OUTPUT);
  pinMode(LedVerde, OUTPUT);
}

void loop() {
  // Leitura do sensor de pH
  int leituraPH = analogRead(ph_pin);
  double voltage = 5.0 / 1024.0 * leituraPH; 
  float Po = 7 + ((2.5 - voltage) / 0.18);  // Cálculo do pH

  // Leitura do sensor de boia
  int leituraBoia = digitalRead(SensorBoia);
  String statusBoia = (leituraBoia == HIGH) ? "ALTO" : "BAIXO";

  // Verifica se o pH saiu da faixa segura (apenas avisa uma vez)
  if ((Po > 9 || Po < 3) && !pH_fora_faixa) {
    Serial.println("⚠️ ALERTA: pH fora da faixa segura!");
    Serial.print("Valor do pH: ");
    Serial.println(Po, 2);
    pH_fora_faixa = true;  // Atualiza o estado
  }

  // Verifica se o pH voltou à faixa segura (apenas avisa uma vez)
  if ((Po >= 3 && Po <= 9) && pH_fora_faixa) {
    Serial.println("✅ O pH voltou à faixa segura.");
    Serial.print("Valor do pH: ");
    Serial.println(Po, 2);
    pH_fora_faixa = false;  // Atualiza o estado
  }

  // Envia os dados apenas se houver mudança no sensor de boia
  if (leituraBoia != ultimoEstadoBoia) {
    String mensagem = "{\"ph\": " + String(Po, 2) + 
                      ", \"voltagem\": " + String(voltage, 3) + 
                      ", \"boia\": " + String(leituraBoia) + 
                      ", \"status\": \"" + statusBoia + "\"}";
    Serial.println(mensagem);

    // Atualiza o último estado
    ultimoEstadoBoia = leituraBoia;

    // Controle dos LEDs
    if (leituraBoia == HIGH) { 
      digitalWrite(LedVermelho, LOW);
      digitalWrite(LedVerde, HIGH);
    } else {
      digitalWrite(LedVermelho, HIGH);
      digitalWrite(LedVerde, LOW);
    }
  }

  delay(2000);  // Ajuste no tempo de leitura
}
