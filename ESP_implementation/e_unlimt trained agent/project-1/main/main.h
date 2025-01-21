#ifndef MAIN_H
#define MAIN_H //per definire una sola volta le funzioni in compilazione
#define LOG_LEVEL_LOCAL ESP_LOG_VERBOSE
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "esp_timer.h"
#include "driver/mcpwm_prelude.h"
#include "esp_adc/adc_oneshot.h"
#include "hal/adc_types.h"
#include "esp_rom_sys.h"
#include "edge-impulse-sdk/classifier/ei_run_classifier.h"
#include "math.h"




void encoder_config(void);
void motor_pwm_config(void);
void go_cw(void);
void go_ccw(void);
void adc_config(void);
float get_angle(int count);
float clip(float value, float min, float max);




#endif //MAIN_H