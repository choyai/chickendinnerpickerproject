#include <24FJ48GA002.h>
#include "BL_Support.h"
#include "math.h"
#use delay(internal = 8 MHz, clock = 32MHz)

#PIN_SELECT U1RX = PIN_B12 // PIN_B14 //
#PIN_SELECT U1TX = PIN_B13 // PIN_B15 //
#use rs232(UART1, BAUD = 9600, XMIT = PIN_B13, RCV = PIN_B12)

#define DEVICE_ID 2
#define limitSw_x PIN_B8 //
#define limitSw_y PIN_A2 //
#define limitSw_z PIN_A4 //
#define Motor_Bp PIN_B10 // Pin output is connected to DXI0  (PWM)
#define Motor_Br PIN_B2  // Pin output is connected to DX02
#define Motor_Bl PIN_B3  // Pin output is connected to DX03
#define Motor_Ap PIN_B4  // Pin output is connected to DX03
#define Motor_Ar PIN_A1  // Pin output is connected to DX03
#define Motor_Al PIN_A0  // Pin output is connected to DX03
#define Motor_Zp PIN_B14 // Pin output is connected to DX03
#define Motor_Zr PIN_B15 // Pin output is connected to DX03
#define Motor_Zl PIN_B9  // Pin output is connected to DX03
#define Encode_A PIN_B7  // Pin output is connected to DX03
#define Encode_B PIN_B6  // Pin output is connected to DX03
#define Encode_Z PIN_B5  // Pin output is connected to DX03
#define servo_r PIN_B0   // servo 270
#define servo_l PIN_B1   // servo 180

#PIN_SELECT OC1 = Motor_Bp
#PIN_SELECT OC2 = Motor_Ap
#PIN_SELECT OC3 = Motor_Zp
#PIN_SELECT OC4 = servo_r
#PIN_SELECT OC5 = servo_l
#PIN_SELECT INT1 = Encode_B
#PIN_SELECT INT2 = Encode_Z

// long count = 0;
long count_a = 0;
long count_b = 0;
long count_z = 0;
// long posi = 0;
int u_a;
int *a_u = &u_a;
int u_b;
int *b_u = &u_b;
int u_z;
int *z_u = &u_z;

int s_a = 0;
int *a_s = &s_a;
int s_b = 0;
int *b_s = &s_b;
int s_z = 0;
int *z_s = &s_z;
int p_a = 0;
int *a_p = &p_a;
int p_b = 0;
int *b_p = &p_b;
int p_z = 0;
int *z_p = &p_z;

int tolerance_a = 30;
int tolerance_b = 30;
int tolerance_z = 20;

float K_Pz = 0.6;
float K_Iz = 0.0015;
float K_Dz = 0.002;
float K_Pa = 0.6;
float K_Ia = 0.001;
float K_Da = 0.0025;
float K_Pb = 0.6;
float K_Ib = 0.001;
float K_Db = 0.0025;

int direction_z = 0;
int direction_a = 0;
int direction_b = 0;
char array[20] = {};
char SM_id = 0;
int getPackage = 0;
char command_ID;
// char* print_float(float data){
//    long intDist = data / 1;
//     long dotDist = (((intDist>>31)*-2)+1) * ((data * 1000.0f) - (intDist *
//     1000));
//     char stringFloat[20];
//     sprintf(stringFloat, "%d.%d", intDist, dotDist);
//     return stringFloat;
// }
// void print_float(char* stringResult, float data){
//    long intDist = data / 1;
//     long dotDist = (((intDist>>31)*-2)+1) * ((data * 1000.0f) - (intDist *
//     1000));
//     sprintf(stringResult, "%d.%d", intDist, dotDist);
// }

// Encoder Interrupts
#INT_EXT0
void INT_EXT_INPUT0(void) {
  if (direction_a == 0) {
    count_a++;
  } else {
    count_a--;
  }
}

#INT_EXT1
void INT_EXT_INPUT1(void) {
  if (direction_b == 0) {
    count_b++;
  } else {
    count_b--;
  }
}

#INT_EXT2
void INT_EXT_INPUT2(void) {
  if (direction_z == 0) {
    count_z++;
  } else {
    count_z--;
  }
}

void Init_Interrupts() {
  enable_interrupts(INT_EXT0);
  ext_int_edge(0, L_TO_H); // Rising Edge
  enable_interrupts(INT_EXT1);
  ext_int_edge(1, L_TO_H); // Rising Edge
  enable_interrupts(INT_EXT2);
  ext_int_edge(2, L_TO_H); // Rising Edge
}

//

// Communication Routines

void SM_RxD(int c) {
  if (getPackage == 0) {
    if (SM_id < 2) {
      if (c == 255) {
        array[SM_id] = c;
        SM_id++;
      } else {
        SM_id = 0;
      }
    } else if (SM_id == 2) {
      array[SM_id] = c;
      command_ID = c;
      SM_id++;
    } else if (SM_id > 2) {
      array[SM_id] = c;
      if (SM_id >= 9) {
        getPackage = 1;
        SM_id = 0;
      } else {
        SM_id++;
      }
    }
  }
}

#INT_RDA
void UART1_Isr() {
  int c = getc();
  // putc(c);
  SM_RxD(c);
}
//

// Motor
void Motor_z(int u) {
  if (u > 100)
    u = 100;
  if (u < -100)
    u = -100;
  if (u > 0) {
    output_bit(Motor_Zr, 0);
    output_bit(Motor_Zl, 1);
    direction_z = 0;
    set_pwm_duty(3, (int)(2 * u));
  } else if (u < 0) {
    output_bit(Motor_Zr, 1);
    output_bit(Motor_Zl, 0);
    direction_z = 1;
    set_pwm_duty(3, (int)(2 * -u));
  } else {
    output_bit(Motor_Zr, 1);
    output_bit(Motor_Zl, 1);
    set_pwm_duty(3, (int)(100));
  }
}

void Motor_a(int u) {
  if (u > 100)
    u = 100;
  if (u < -100)
    u = -100;
  if (u > 0) {
    output_bit(Motor_Ar, 1);
    output_bit(Motor_Al, 0);
    direction_a = 0;
    set_pwm_duty(2, (int)(2 * u));
  } else if (u < 0) {
    output_bit(Motor_Ar, 0);
    output_bit(Motor_Al, 1);
    direction_a = 1;
    set_pwm_duty(2, (int)(2 * -u));
  } else {
    output_bit(Motor_Ar, 1);
    output_bit(Motor_Al, 1);
    set_pwm_duty(2, (int)(100));
  }
}

void Motor_b(int u) {
  if (u > 100)
    u = 100;
  if (u < -100)
    u = -100;
  if (u > 0) {
    output_bit(Motor_Br, 1);
    output_bit(Motor_Bl, 0);
    direction_b = 0;
    set_pwm_duty(1, (int)(2 * u));
  } else if (u < 0) {
    output_bit(Motor_Br, 0);
    output_bit(Motor_Bl, 1);
    direction_b = 1;
    set_pwm_duty(1, (int)(2 * -u));
  } else {
    output_bit(Motor_Br, 1);
    output_bit(Motor_Bl, 1);
    set_pwm_duty(1, (int)(100));
  }
}

void PID(long r, long count, long s, long p, int *u, float K_P, float K_I,
         float K_D) {
  long e = r - count;
  s = s + e;
  *u = (K_P * e) + (K_I * s) + (K_D * (e - p));
  p = e;
}
//

// Utilities
int mergeInts(int MSB, int LSB) {
  long a = (256 * (int)(unsigned char)MSB) + (unsigned char)LSB;
  printf("merged %d and %d into: %d \n", MSB, LSB, a);
  return a;
}

float intsToFloat(unsigned char LSB, unsigned char hexadec) {
  float flo = (float)LSB + ((float)hexadec) / 256;
  printf("merged %d and %d into: %0.2f\n", LSB, hexadec, flo);
  return flo;
}
//

// COMMANDS//
void setHome() {
  setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
  setup_compare(2, COMPARE_PWM | COMPARE_TIMER3);
  setup_compare(1, COMPARE_PWM | COMPARE_TIMER3);
  set_pwm_duty(3, 0);
  set_pwm_duty(2, 0);
  set_pwm_duty(1, 0);
while (input(limitSw_z) == 1){
    Motor_z(-100);
  }
  Motor_z(0);
   while (input(limitSw_y) == 1){
    Motor_a(-100);
    Motor_b(-100);
  }
  // Motor_a(0);
  // Motor_b(0);
  while (input(limitSw_x) == 1){
    Motor_a(100);
    Motor_b(-100);
  }
  Motor_b(0);
  Motor_a(0);
  printf("%d, %d, %d\n", count_a, count_b, count_z);
  count_a = 0;
  count_b = 0;
  count_z = 0;
  printf("done");
  getPackage = 0;
}

void setPosAB() {
  long r_a = mergeInts((int)array[3], (int)array[4]);
  long r_b = mergeInts((int)array[5], (int)array[6]);
  if ((int)array[7] == 1) {
    r_a = 0 - r_a;
  }
  if ((int)array[8] == 1) {
    r_b = 0 - r_b;
  }
  printf("r_a = %d\n", (int)r_a);
  printf("r_b = %d\n", (int)r_b);
  while (abs(r_a - count_a) > tolerance_a || abs(r_b - count_b) > tolerance_b) {
    PID(r_a, count_a, a_s, a_p, a_u, K_Pa, K_Ia, K_Da);
    PID(r_b, count_b, b_s, b_p, b_u, K_Pb, K_Ib, K_Db);
    Motor_a(u_a);
    Motor_b(u_b);
  }
  Motor_a(0);
  Motor_b(0);
  printf("position = %d, %d\n", count_a, count_b);
  printf("done");
  getPackage = 0;
}

void setPosZ() {
  long r_z = mergeInts((int)array[3], (int)array[4]);
  printf("r_z = %d", (int)r_z);
  while (abs(r_z - count_z) > tolerance_z) {
    PID(r_z, count_z, z_s, z_p, z_u, K_Pz, K_Iz, K_Dz);
    Motor_z(u_z);
    // printf("count_z : %d\n",count_z);
    // delay_ms(10);
  }
  Motor_z(0);
  printf("position = %d\n", count_z);
  printf("done");
  getPackage = 0;
}

void gripClose() {
  setup_compare(5, COMPARE_PWM | COMPARE_TIMER2);
  set_pwm_duty(5, 2600);
  delay_ms(500);
  printf("done");
  getPackage = 0;
}

void gripOpen() {
  setup_compare(5, COMPARE_PWM | COMPARE_TIMER2);
  set_pwm_duty(5, 4200);
  delay_ms(500);
  printf("done");
  getPackage = 0;
}

void gripRotate() {
  int angle = mergeInts((int)array[3], (int)array[4]);
  setup_compare(4, COMPARE_PWM | COMPARE_TIMER2);
  set_pwm_duty(4, (int)(((angle * 0.186) + 12) * 80));
  delay_ms(500);
  printf("done");
  getPackage = 0;
}

void setAGains() {
  K_Pa = intsToFloat((unsigned char)array[3], (unsigned char)array[4]);
  K_Ia = intsToFloat((unsigned char)array[5], (unsigned char)array[6]);
  K_Da = intsToFloat((unsigned char)array[7], (unsigned char)array[8]);
  printf("done");
  getPackage = 0;
}

void setBGains() {
  K_Pb = intsToFloat((unsigned char)array[3], (unsigned char)array[4]);
  K_Ib = intsToFloat((unsigned char)array[5], (unsigned char)array[6]);
  K_Db = intsToFloat((unsigned char)array[7], (unsigned char)array[8]);
  printf("done");
  getPackage = 0;
}

void setZGains() {
  K_Pz = intsToFloat((unsigned char)array[3], (unsigned char)array[4]);
  K_Iz = intsToFloat((unsigned char)array[5], (unsigned char)array[6]);
  K_Dz = intsToFloat((unsigned char)array[7], (unsigned char)array[8]);
  printf("done");
  getPackage = 0;
}

void setTolerances(){
  tolerance_a = mergeInts((int)array[3], (int)array[4]);
  tolerance_b = mergeInts((int)array[5], (int)array[6]);
  tolerance_z = mergeInts((int)array[7], (int)array[8]);
  printf("done");
  getPackage = 0;
}

int sumCheck() {
  char sum = 0;
  char checksum = array[9];
  for (int i = 0; i < 9; i++) {
    sum = sum + (char)array[i];
  }
  sum = (char)sum;
  if (sum == checksum) {
    return 1;
  } else {
    return 0;
  }
}
//

//
void main() {
  disable_interrupts(GLOBAL);

  clear_interrupt(
      INT_RDA); // recommend style coding to confirm everything clear before use

  enable_interrupts(INT_RDA);
  Init_Interrupts();
  enable_interrupts(GLOBAL);
  setup_timer3(TMR_INTERNAL | TMR_DIV_BY_8, 200);
  setup_timer2(TMR_INTERNAL | TMR_DIV_BY_8, 8000);
  setup_compare(3, COMPARE_PWM | COMPARE_TIMER3);
  setup_compare(2, COMPARE_PWM | COMPARE_TIMER3);
  setup_compare(1, COMPARE_PWM | COMPARE_TIMER3);
  set_pwm_duty(3, 0);
  set_pwm_duty(2, 0);
  set_pwm_duty(1, 0);
  count_a = 0;
  count_b = 0;
  count_z = 0;
  // setPosAB();
  // gripOpen();
  // delay_ms(1000);
  // gripClose();
  // delay_ms(1000);
  // printf("System Ready!\r\n");
  while (TRUE) {
    if (getPackage >= 1) {
      int received = sumCheck();
      if (!received) {
        printf("resend");
        getPackage = 0;
      } else {
        switch (array[2]) {
        case 0:
          setHome();
          break;
        case 1:
          setPosAB();
          break;
        case 2:
          setPosZ();
          break;
        case 3:
          gripClose();
          break;
        case 4:
          gripOpen();
          break;
        case 5:
          gripRotate();
          break;
        case 6:
          setAGains();
          break;
        case 7:
          setBGains();
          break;
        case 8:
          setZGains();
          break;
        case 9:
          setTolerances();
          break;
        default:
          printf("resend");
          getPackage = 0;
          break;
        }
      }
    }
  }
}
