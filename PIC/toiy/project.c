#include <24FJ48GA002.h>
#include "BL_Support.h"

#PIN_SELECT OC1 = PIN_B2  // Pin DX02
#PIN_SELECT OC2 = PIN_B3  // Pin DX03
#PIN_SELECT OC3 = PIN_B4  // Pin DXI0  (PWM)
#PIN_SELECT INT1 = PIN_B5 // Pin DXI1  (Encoder)
// #PIN_SELECT INT2 = PIN_B6

long count = 0; //set count = 0
float timer = 0; 
float volt = 0; //set volt = 0 
int x;

#INT_EXT1
void INT_EXT_INPUT1(void) {
  if (input(PIN_B6)==0) {
    count++;
  } else {
    count--;
  }
}

float chirpSine(float time) {
  float signal = sin(time * time) * 12;
  return signal;
}
int convertToDuty(float voltage) {
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
	timer += 0.01;
	printf("%d ", (int)(timer*1000));
 	printf(",");
 	printf(" %d ", count);
	printf(",");
 	printf(" %d", (int)(volt * 1000));
	printf("\r\n");
// Send time , voltage in milli for resolution
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
  volt = chirpSine(timer);
  int duty = convertToDuty(volt);
  int dir = getDirection(volt);
  flip(dir, duty);
  timer += 0.0001;
}

void motorDrive() {
  setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200); // Set frequency at 10 KHz
  enable_interrupts(INT_TIMER3);
  setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
}

void main() {
  disable_interrupts(GLOBAL);
  motorDrive();
  Init_Timer2();
  Init_Interrupts();
  enable_interrupts(GLOBAL);

  while (TRUE) {
  }
}