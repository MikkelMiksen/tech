import re
import numpy as np


class DistCalc:
    SIGMA = (0.68, 1.14, 1.0)
    BIAS = (1.74, 4.45, 3.78)

    PATTERN = re.compile(
        r"ifft:\s*(-?\d+(?:\.\d+)?),\s*"
        r"phase_slope:\s*(-?\d+(?:\.\d+)?),\s*"
        r"rtt:\s*(-?\d+(?:\.\d+)?)"
    )

    def __init__(self, sigma=SIGMA, bias=BIAS, gate=1.0, q=0.01, min_sigma=0.05):
        self.sigma = np.maximum(np.asarray(sigma, dtype=float), min_sigma)
        self.bias = np.asarray(bias, dtype=float)
        self.gate = gate
        self.q = q
        self.x = None   # Kalman state: distance
        self.p = None   # Kalman state: variance

    def _fuse(self, est):
        ok = np.abs(est - np.median(est)) < self.gate
        if not ok.any():
            return float(np.median(est)), float(self.sigma.max())
        w = 1.0 / self.sigma[ok] ** 2
        d = np.sum(w * est[ok]) / np.sum(w)
        return float(d), float(np.sqrt(1.0 / np.sum(w)))

    def _kalman(self, z, r):
        if self.x is None:
            self.x, self.p = z, r
            return self.x
        self.p += self.q
        k = self.p / (self.p + r)
        self.x += k * (z - self.x)
        self.p *= (1 - k)
        return self.x

    def calculate_distance(self, serial_input):
        if isinstance(serial_input, bytes):
            serial_input = serial_input.decode("utf-8", errors="ignore")

        m = self.PATTERN.search(serial_input)
        if m is None:
            print("Did not find float values in text")
            return None

        raw = np.array([float(g) for g in m.groups()])
        est = raw - self.bias                 # apply stored bias correction
        d, sigma = self._fuse(est)
        return self._kalman(d, sigma ** 2)

