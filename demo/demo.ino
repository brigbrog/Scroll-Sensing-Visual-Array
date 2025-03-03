void setup() {
  Serial.begin(9600);
}

void loop() {
  float cur = analogRead(A0);
  Serial.println(cur);
}