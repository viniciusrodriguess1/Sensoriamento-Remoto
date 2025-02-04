int ph_pin = A0; 
void setup() {
  Serial.begin(9600);
  Serial.println("    Projeto agua em ação");
  }
void loop() {
  int measure = analogRead(ph_pin);
  Serial.print("Measure: ");
  Serial.print(measure);

  double voltage = 5 / 1024.0 * measure; 
  Serial.print("\tVoltage: ");
  Serial.print(voltage, 3);

  float Po = 7 + ((2.5 - voltage) / 0.18);
  Serial.print("\tPH: ");
  Serial.print(Po, 3);

  Serial.println("");
  delay(2000);
}