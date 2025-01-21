#include "main.h"
//e0
#define LOG_TAG "MAIN"
// ports
#define PHASE_A GPIO_NUM_34
#define PHASE_B GPIO_NUM_35
#define MOTOR_IN1 GPIO_NUM_18
#define MOTOR_IN2 GPIO_NUM_19

//Encoder
#define STEP_PER_REV 2000
static volatile int encoder_count = 0;// Contatore dell'encoder
int phase_a_level;
int phase_b_level;

//PWM
#define PWM_FREQ 20000 //10KHz
#define TIMER_FREQ 10000000 //10MHz
#define MAX_DUTY TIMER_FREQ/PWM_FREQ //1000
volatile int dutyCycle; 
volatile int prev_duty = 0;
mcpwm_timer_handle_t timer = NULL;
mcpwm_gen_handle_t gen1 = NULL; // gen pwm in1 
mcpwm_gen_handle_t gen2 = NULL; // gen pwm in2
mcpwm_cmpr_handle_t comparator = NULL;


#define MAX_STP 200
#define TANK_INIT 0.4
float features[3];

///////////////////////////////////INTERRUPT HANDLERS AND TASKS////////////////////////////////////////

static void IRAM_ATTR phase_a_isr_handler(void *arg) 
{

        phase_a_level = gpio_get_level(PHASE_A);
        phase_b_level= gpio_get_level(PHASE_B);

        if (phase_a_level == 1) { // Rising edge on Phase A
            if (phase_b_level == 0) {
                encoder_count--; // CW
            } else {
                encoder_count++; // CCW
            }
        } else { // Falling edge on Phase A
            if (phase_b_level == 1) {
                encoder_count--; // CW
            } else {
                encoder_count++; // CCW
            }
        }
}

static void IRAM_ATTR phase_b_isr_handler(void *arg) 
{

        phase_a_level = gpio_get_level(PHASE_A);
        phase_b_level= gpio_get_level(PHASE_B);

        if (phase_b_level == 1) { // Rising edge on Phase B
            if (phase_a_level == 1) {
                encoder_count--; // CW
            } else {
                encoder_count++; // CCW
            }
        } else { // Falling edge on Phase B
            if (phase_a_level == 0) {
                encoder_count--; // CW
            } else {
                encoder_count++; // CCW
            }
        }
   
}

///////////////////////////////////CONFIGURATION FUNCTIONS/////////////////////////////////////////////////

void encoder_config(void)
{
    // Configurazione dei pin
    gpio_config_t io_conf = {};
        io_conf.intr_type = GPIO_INTR_ANYEDGE;
        io_conf.mode = GPIO_MODE_INPUT;
        io_conf.pin_bit_mask = ((1ULL << PHASE_A) | (1ULL << PHASE_B));
        io_conf.pull_up_en = GPIO_PULLUP_ENABLE;
    gpio_config(&io_conf);

    //configurazione degli interrupt

}

void motor_pwm_config(void)
{
       gpio_config_t io_conf_motor = {};
        io_conf_motor.intr_type = GPIO_INTR_DISABLE;
        io_conf_motor.mode = GPIO_MODE_OUTPUT;
        io_conf_motor.pin_bit_mask = ((1ULL << MOTOR_IN1) | (1ULL << MOTOR_IN2));
        io_conf_motor.pull_up_en = GPIO_PULLUP_DISABLE;
        io_conf_motor.pull_down_en = GPIO_PULLDOWN_DISABLE;
    gpio_config(&io_conf_motor);

    
    //Initialize MCPWM unit
    
    mcpwm_timer_config_t timer_config = {};
        timer_config.group_id = 0;
        timer_config.clk_src = MCPWM_TIMER_CLK_SRC_DEFAULT;
        timer_config.resolution_hz = TIMER_FREQ;  // 1MHz resolution
        timer_config.period_ticks = TIMER_FREQ / PWM_FREQ;  // PWM frequency
        timer_config.count_mode = MCPWM_TIMER_COUNT_MODE_UP;
    
    ESP_ERROR_CHECK(mcpwm_new_timer(&timer_config, &timer));

    // Initialize MCPWM operator
    mcpwm_oper_handle_t oper = NULL;
    mcpwm_operator_config_t operator_config = {};
        operator_config.group_id = 0;
   
    ESP_ERROR_CHECK(mcpwm_new_operator(&operator_config, &oper));

    // Connect operator to timer
    ESP_ERROR_CHECK(mcpwm_operator_connect_timer(oper, timer));

     // Create a comparator
    
    mcpwm_comparator_config_t comparator_config = {};
        comparator_config.flags.update_cmp_on_tez = true;
    ESP_ERROR_CHECK(mcpwm_new_comparator(oper,&comparator_config, &comparator));

    // Set the compare value
    ESP_ERROR_CHECK(mcpwm_comparator_set_compare_value(comparator, 0));  // Initial duty cycle 0

    // Create pwm generator for in1
   
    mcpwm_generator_config_t gen_config_1 = {};
        gen_config_1.gen_gpio_num = MOTOR_IN1;
    ESP_ERROR_CHECK(mcpwm_new_generator(oper, &gen_config_1, &gen1));

    // Create pwm generator for in2
    
    mcpwm_generator_config_t gen_config_2 = {};
        gen_config_2.gen_gpio_num = MOTOR_IN2;
    ESP_ERROR_CHECK(mcpwm_new_generator(oper, &gen_config_2, &gen2));

    //questa parte non cambia mai: MCPWM_GEN_ACTION_LOW non cambia mai in MCPWM_GEN_ACTION_HIGH
    //setta il comportamento del comparatore
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_compare_event(gen1,
            MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, comparator, MCPWM_GEN_ACTION_LOW)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_compare_event(gen2,
            MCPWM_GEN_COMPARE_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, comparator, MCPWM_GEN_ACTION_LOW))); 
        
    // Start the timer
    mcpwm_timer_enable(timer);
    ESP_ERROR_CHECK(mcpwm_timer_start_stop(timer, MCPWM_TIMER_START_NO_STOP));
}


///////////////////////////////////OTHER FUNCTIONS/////////////////////////////////////////////////

void go_cw(void)
{
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_timer_event(gen1,
                    MCPWM_GEN_TIMER_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_TIMER_EVENT_EMPTY, MCPWM_GEN_ACTION_LOW)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_timer_event(gen2,
                    MCPWM_GEN_TIMER_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_TIMER_EVENT_EMPTY, MCPWM_GEN_ACTION_HIGH)));
}

void go_ccw(void)
{
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_timer_event(gen1,
                        MCPWM_GEN_TIMER_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_TIMER_EVENT_EMPTY, MCPWM_GEN_ACTION_HIGH)));
    ESP_ERROR_CHECK(mcpwm_generator_set_action_on_timer_event(gen2,
                        MCPWM_GEN_TIMER_EVENT_ACTION(MCPWM_TIMER_DIRECTION_UP, MCPWM_TIMER_EVENT_EMPTY, MCPWM_GEN_ACTION_LOW)));
}

float get_angle(int count)
{
    // Calcola l'angolo in base al conteggio dell'encoder
    float deg = ((float)count / (float)STEP_PER_REV) * 360.0;

    // Mappa l'angolo nell'intervallo [0, 360)
    deg = fmod(deg, 360.0);

    // Se l'angolo è negativo, lo portiamo nell'intervallo positivo [0, 360)
    if (deg < 0) {
        deg += 360.0;
    }

    return deg * M_PI/180.0;
}

float clip(float value, float min, float max) 
{
    return fmax(min, fmin(value, max));
}

float normalize_angle(float th) {
    float th_norm = fmod(th + M_PI, 2.0 * M_PI);  // Calcolo del modulo su 2*pi
    if (th_norm < 0) {
        th_norm += 2.0 * M_PI;  // Assicura che sia positivo
    }
    return th_norm - M_PI;  // Riporta il risultato nell'intervallo [-pi, pi]
}

float calculate_pos_err(float th) {
    float th_normalized = normalize_angle(th);  // Normalizza l'angolo tra -pi e pi
    float pos_err;

    if (th_normalized >= 0.157) {
        pos_err = 0.335 * th_normalized - 0.0526;
    } else if (th_normalized <= -0.096) {
        pos_err = -0.329 * th_normalized + 0.0316;
    } else {
        pos_err = 0;
    }

    return pos_err;
}

void set_angle(float angle)
{
    encoder_count = angle/360.0 * STEP_PER_REV;
}

int raw_feature_get_data(size_t offset, size_t length, float *out_ptr) {
    memcpy(out_ptr, features + offset, length * sizeof(float));
    return 0;
}

///////////////////////////////////MAIN FUNCTION/////////////////////////////////////////////////

void inference_task(void *arg)
{
    int stp,ep,tot_steps = 0;
    int64_t inference_start_time, inference_end_time, inference_duration;
    float th, vel,prev_th,de,tank, delta_theta,pos_err;
    float best_action,prev_best_action,dt,u = 0;
    uint16_t dutyCycle;
    signal_t obs;
    ei_impulse_result_t result; 
    EI_IMPULSE_ERROR resp;
    while (1)
    {
        mcpwm_comparator_set_compare_value(comparator, 0);
        printf("Posizionare il pendolo\n");
        vTaskDelay(500);
        set_angle(180.0);
        th,vel,de,prev_th,stp = 0;
        tank = TANK_INIT;
        ep ++;
        while (stp <= MAX_STP)
        {
            //////////////PREDIZIONE MODELLO ///////////
            // funzioni richieste dall'API di Edge Impulse
            features[0] = cos(th);
            features[1] = sin(th);
            features[2] = tanh(vel);
            obs.total_length = 3;
            obs.get_data = &raw_feature_get_data;
            resp = run_classifier(&obs, &result,false);
            if (resp != EI_IMPULSE_OK) {
                ei_printf("ERROR: Failed to run classifier (%d)\n", resp);
                continue;
            }
            best_action =clip(result.classification[0].value,-1.0,1.0);
            ////////////////////COMANDO///////////////////
            dutyCycle = (int)(MAX_DUTY * abs(best_action));
            mcpwm_comparator_set_compare_value(comparator, dutyCycle);
            if (best_action > 0) 
                go_ccw();
             else 
                go_cw();
            ///////////////AGGIORNAMENTO STATO////////////
            inference_end_time = esp_timer_get_time();
            dt= inference_end_time - inference_start_time;
            dt = (float)dt/1000000;
            if(stp != 0)
            {
            th = get_angle(encoder_count);
            delta_theta = th-prev_th;
            if (delta_theta > M_PI) {
                delta_theta -= 2.0 * M_PI;
                } else if (delta_theta < -M_PI) {
                delta_theta += 2.0 * M_PI;
                }
                vel = delta_theta / dt;
            }
            inference_start_time = esp_timer_get_time();
            /////////////UPDATE TANK/////////////////////
            u = (prev_best_action*12 - vel*0.07)*0.07/32;
            de = u*(delta_theta); //ricordare il caso in cui V è 0
            if (de > 0  && best_action != 0)
                tank = tank - de;
            if (tank <= 0)
                break;
            //////////////////////////////////////////////
            pos_err = normalize_angle(th);
            prev_best_action = best_action;
            prev_th = th;
            stp++;
            tot_steps++;
            printf("%d,%d,%f,%f,%f\n",ep,tot_steps,pos_err,vel,TANK_INIT-tank);
        }
    }
}


extern "C" void app_main(void) //extern "C", poichè il compilatore C++ manda in errore la funzione app_main() altrimenti
{
    ESP_LOGI(LOG_TAG, "SETUP!");

    encoder_config();

    motor_pwm_config();

    gpio_install_isr_service(0);
    gpio_isr_handler_add(PHASE_A, phase_a_isr_handler, (void*) GPIO_NUM_16);
    gpio_isr_handler_add(PHASE_B, phase_b_isr_handler, (void*) GPIO_NUM_17);

    xTaskCreatePinnedToCore(inference_task, "Inference Task", 4096, NULL, 5, NULL, 1);

}

