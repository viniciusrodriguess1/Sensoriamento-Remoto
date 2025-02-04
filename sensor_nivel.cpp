#define SensorBoia 10 
#define LedVermelho 11 
#define LedVerde 12 

int leiturasensor ; 

void setup() {
  Serial.begin(9600); 
  pinMode(SensorBoia, INPUT); 
  pinMode(LedVermelho, OUTPUT); 
  pinMode(LedVerde, OUTPUT); 
}

void loop() {
  leiturasensor = digitalRead(SensorBoia); 
  Serial.print("Leitura do sensor: ");
  Serial.println(leiturasensor);

  if (leiturasensor == HIGH) { 
    Serial.println("Nível de água alto");
    digitalWrite(LedVermelho, LOW);
    digitalWrite(LedVerde, HIGH);
  }
  else {
    Serial.println("Nível de água baixo");
    digitalWrite(LedVermelho, HIGH);
    digitalWrite(LedVerde, LOW);
  }
  delay(300);
}