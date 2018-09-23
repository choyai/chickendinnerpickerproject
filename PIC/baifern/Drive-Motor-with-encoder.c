#include <24FJ48GA002.h>
#include "BL_Support.h"
#include "math.h"
#use delay(internal = 8 MHz, clock = 32000000)
#PIN_SELECT U1TX = PIN_B13
#PIN_SELECT U1RX = PIN_B12

#use rs232(UART1, baud = 115200, xmit = PIN_B13, rcv = PIN_B12)

#PIN_SELECT OC1 = PIN_B2  // Pin output is connected to DX02
#PIN_SELECT OC2 = PIN_B3  // Pin output is connected to DX03
#PIN_SELECT OC3 = PIN_B4  // Pin output is connected to DXI0  (PWM)
#PIN_SELECT INT1 = PIN_B5 // Pin output is connected to DXI1  (Encoder)
// #PIN_SELECT INT2 = PIN_B6			// Pin output is connected to DXI2
// (Stop motor)

long countPulse;
float timer3time = 0;
float volt = 0;
int x;

#INT_EXT1
void INT_EXT_INPUT1(void) {
  if (input(PIN_B6) == 0) {
    countPulse++;
  } else {
    countPulse--;
  }
}

float chirpSine(float time) {
  float sig = sin(time * time) * 12;
  return sig;
}
int convertToDUTY(float voltage) {
  int duty = abs(voltage) * 100 / 12;
  return duty;
}

int getDirection(float voltage) {
  int direction;
  if (voltage > 0) {
    direction = 0;
  } else if (voltage < 0) {
    direction = 1;
  } else {
    direction = 2;
  }
  return direction;
}

void Init_Interrupts() {
  enable_interrupts(INT_EXT1);
  ext_int_edge(1, L_TO_H); // Rising Edge
}

#INT_TIMER2
void TIMER2_isr() {
  timer3time += 0.01;

  printf("%d", (int)(timer3time*1000));
  printf(",");
  printf("%d", countPulse);
	printf(",");
  printf("%d", (int)(volt * 1000));
	printf("\n");
}

void init_Timer2() {
  setup_timer2(TMR_INTERNAL | TMR_DIV_BY_256, 625);
  enable_interrupts(INT_TIMER2);
}

void flip(int direction, int PWM) {
  if (direction == 0) { // turn right
    x = 1;
    output_bit(PIN_B2, 1);
    output_bit(PIN_B3, 0);
  } else if (direction == 1) { // turn left
    x = 0;
    output_bit(PIN_B2, 0);
    output_bit(PIN_B3, 1);
  } else if (direction == 2) {
    output_bit(PIN_B2, 1);
    output_bit(PIN_B3, 1);
  }
  set_pwm_duty(3, 200 * PWM / 100);
}

#INT_TIMER3
void TIMER3_ist() {
	// if(timer3time <= 20){
  volt = chirpSine(timer3time);
  int duty = convertToDUTY(volt);
  int dir = getDirection(volt);
  flip(dir, duty);
	// }
	// else{
		// set_pwm_duty(3, 0);
	// }
  timer3time += 0.0001;
}

void Drivemotor() {
  setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200); // Set frequency at 10 KHz
  enable_interrupts(INT_TIMER3);
  setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
}

void main() {
  countPulse = 0;
  timer3time = 0;
  disable_interrupts(GLOBAL);
  Drivemotor();
  Init_Timer2();
  Init_Interrupts();
  enable_interrupts(GLOBAL);

  while (TRUE) {
  }
}
