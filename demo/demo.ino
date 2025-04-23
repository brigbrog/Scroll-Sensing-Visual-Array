void setup() {
  Serial.begin(9600);
  //pinMode(5, OUTPUT);
}

void loop() {
  float gloveVal;

  gloveVal = analogRead(A0);

  Serial.println(gloveVal);
  delay(100);
}
