# tech
main 1.0


Steps (nRF Connect SDK, v3.2.x)

Install the nRF Connect SDK and the VS Code extension.
Build the Nordic samples channel_sounding_ras_reflector and channel_sounding_ras_initiator for the nRF54L15 DK. Nordic users run these two samples on a pair of nRF54L15 boards, and Nordic says it supports its own nRF repo samples more than the Zephyr ones. 
nordicsemi
nordicsemi
Flash the reflector to one board and the initiator to the other. The initiator connects, runs the ranging procedure and logs distance estimates (ifft, phase_slope, rtt).
Add the function below to the initiator’s main.c and call it where the sample prints the estimates.
