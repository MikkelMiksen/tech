#include <math.h>
#include <stdbool.h>
#include <stdint.h>

/* ---- Configuration ---- */
#define DISTANCE_NEAR_M  0.5f   /* at or below this distance -> byte 255 */
#define DISTANCE_FAR_M   5.0f   /* at or above this distance -> byte 0   */
#define SMOOTHING        0.3f   /* 0..1, lower = smoother but slower     */

static float   smoothed_distance_m = 0.0f;
static bool    have_first_reading  = false;
static uint8_t last_byte           = 0;

/* Maps a distance in meters to a byte: near -> 255, far -> 0 */
static uint8_t distance_to_byte(float distance_m)
{
    /* Step 1: clamp to the calibrated range */
    if (distance_m < DISTANCE_NEAR_M) {
        distance_m = DISTANCE_NEAR_M;
    }
    if (distance_m > DISTANCE_FAR_M) {
        distance_m = DISTANCE_FAR_M;
    }

    /* Step 2: normalize to 0.0 .. 1.0 (1.0 = closest) */
    float fraction = (DISTANCE_FAR_M - distance_m) /
                     (DISTANCE_FAR_M - DISTANCE_NEAR_M);

    /* Step 3: scale to 0 .. 255 */
    return (uint8_t)(fraction * 255.0f + 0.5f);
}

/* Call this once per new distance estimate. Returns the current byte. */
uint8_t update_proximity_byte(float raw_distance_m)
{
    /* Ignore invalid results (the sample can report NaN or negative values) */
    if (isnan(raw_distance_m) || raw_distance_m < 0.0f) {
        return last_byte;
    }

    /* Exponential moving average to calm the jitter */
    if (!have_first_reading) {
        smoothed_distance_m = raw_distance_m;
        have_first_reading = true;
    } else {
        smoothed_distance_m = SMOOTHING * raw_distance_m +
                              (1.0f - SMOOTHING) * smoothed_distance_m;
    }

    last_byte = distance_to_byte(smoothed_distance_m);
    return last_byte;
}
