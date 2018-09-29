#include <24FJ48GA002.h>
#include "BL_Support.h"
#include "math.h"
#use delay(internal = 8 MHz, clock = 32000000)
#PIN_SELECT U1TX = PIN_B13
#PIN_SELECT U1RX = PIN_B12

#use rs232(UART1, baud = 115200, xmit = PIN_B13, rcv = PIN_B12)

#PIN_SELECT OC1 = PIN_B2  //DX02
#PIN_SELECT OC2 = PIN_B3  //DX03
#PIN_SELECT OC3 = PIN_B4  //DXI0  (PWM)
#PIN_SELECT INT1 = PIN_B5 //DXI1  (Encoder)
// #PIN_SELECT INT2 = PIN_B6			// Pin output is connected to DXI2

#define PERCENT_DUTY 10

long countPulse;
float timer3time = 0;
float volt = 0;
int x;

#INT_EXT1
void INT_EXT_INPUT1(void) {
  if (input(PIN_B6) == 0) {
    countPulse--;
  } else {
    countPulse++;
  }
}

int convertToDUTY(float voltage) {
  int duty = abs(voltage) * 100 / 12;
  return duty;
}

int dutyPercentInput(int duty_percent){
  int duty = abs(duty_percent);
  if(duty > 100){
    duty = 100;
  }
  return duty;
}

int getDirection(int duty_percent) {
  int direction;
  if (duty_percent > 0) {
    direction = 0;
  } else if (duty_percent < 0) {
    direction = 1;
  }
  else{
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
	// Send time and voltage in milli for resolution's sake
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

void directional_drive(int direction, int duty) {
  if (direction == 0) { // turn right
    output_bit(PIN_B2, 1);
    output_bit(PIN_B3, 0);
  } else if (direction == 1) { // turn left
    output_bit(PIN_B2, 0);
    output_bit(PIN_B3, 1);
  } else if (direction == 2) {//stop
    output_bit(PIN_B2, 1);
    output_bit(PIN_B3, 1);
  }
  set_pwm_duty(3, 200 * duty / 100);
}

#INT_TIMER3
void TIMER3_ist() {
  // volt = chirpSine(timer3time);

  int duty = dutyPercentInput(10);
  int dir = getDirection(duty);
  directional_drive(dir, duty);
  // timer3time += 0.0001;
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
