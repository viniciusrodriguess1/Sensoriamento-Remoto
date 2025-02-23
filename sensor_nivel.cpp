#define SensorBoia 10 
#define LedVermelho 11 
#define LedVerde 12 

int leiturasensor; 
int ultimoEstado = -1;  // Variável para armazenar o último estado (inicia com um valor inválido)

void setup() {
  Serial.begin(9600); 
  pinMode(SensorBoia, INPUT); 
  pinMode(LedVermelho, OUTPUT); 
  pinMode(LedVerde, OUTPUT); 
}

void loop() {
  leiturasensor = digitalRead(SensorBoia);  // Lê o sensor

  if (leiturasensor != ultimoEstado) {  // Verifica se houve mudança no estado
    // Define o status com base no valor lido
    String status = (leiturasensor == HIGH) ? "ALTO" : "BAIXO";
    
    // Envia o status e o valor da leitura para o PC
    String mensagem = "{\"leitura\": " + String(leiturasensor) + ", \"status\": \"" + status + "\"}";
    Serial.println(mensagem);

    // Atualiza o último estado
    ultimoEstado = leiturasensor;

    // Controle dos LEDs
    if (leiturasensor == HIGH) { 
      digitalWrite(LedVermelho, LOW);
      digitalWrite(LedVerde, HIGH);
    }
    else {
      digitalWrite(LedVermelho, HIGH);
      digitalWrite(LedVerde, LOW);
    }
  }
  delay(300);  // Pequena pausa para evitar leituras excessivas
}