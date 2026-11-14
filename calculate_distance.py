import re
import numpy as np

def calculate_distance(serial_input: str) -> float:

    ifft        = re.match(r"(?<=ifft: )\d+\.\d+",        serial_input)
    phase_slope = re.match(r"(?<=phase_slope: )\d+\.\d+", serial_input)
    rtt         = re.match(r"(?<=rtt: )\d+\.\d+",         serial_input)

    try:
        ifft        = int(ifft)
        phase_slope = int(phase_slope)
        rtt         = int(rtt)

        # Placeholder sigmas (meters): replace with your measured values
        SIGMA = np.array([ifft, phase_slope, rtt])   # ifft, phase_slope, rtt
        GATE  = 1.0                                  # max deviation from median (m)

        def fuse(ifft, phase_slope, rtt):
            est = np.array([ifft, phase_slope, rtt])
            ok = np.abs(est - np.median(est)) < GATE
            if not ok.any():
                return float(np.median(est)), SIGMA.max()
            w = 1.0 / SIGMA[ok]**2
            d = np.sum(w * est[ok]) / np.sum(w)
            var = 1.0 / np.sum(w)
            return float(d), float(np.sqrt(var))

        class Kalman1D:
            def __init__(self, d0, p0=1.0, q=0.01):
                self.x, self.p, self.q = d0, p0, q
            def update(self, z, r):
                self.p += self.q                 # predict (process noise)
                k = self.p / (self.p + r)        # gain
                self.x += k * (z - self.x)
                self.p *= (1 - k)
                return self.x

        # usage
        d, sigma = fuse(ifft, phase_slope, rtt)
        kf = Kalman1D(d)                       # init on first sample
        smoothed = kf.update(d, sigma**2)

        return smoothed

    except:
        return None
