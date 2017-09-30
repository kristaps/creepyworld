// Command format
// CHxxRxxxZ

String command = "";

void rotateHead(int head, int angle) {
  if (angle > 180) {
    Serial.println("Switching high");
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    Serial.println("Switching low");
    digitalWrite(LED_BUILTIN, LOW);
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
}

void loop() {
  // Wait for command
//  Serial.println("waiting for command");
  command = Serial.readStringUntil('Z');
  if (command == NULL) {
    return;
  }

  if (command.length() != 8 || command[0] != 'C') {
//    Serial.println("Discarding malformed command " + command);
    return;
  }
//  Serial.println("COMMAND:" + command);

  // Parse command
  int head = command.substring(2, 4).toInt();
  int angle = command.substring(5, 8).toInt();
//  Serial.println("HEAD:" + String(head));
//  Serial.println("ANGLE:" + String(angle));

  // Do ya thing, heads!
  rotateHead(head, angle);
}

