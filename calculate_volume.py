class VolCalc:
    def __init__(self, zero_distance:float=10.0, smooth_range:int=10):
        self.zero_distance = zero_distance           # number of meters away where the volume starts fading in
        self.smooth_range  = smooth_range            # length of the history list
        self.history       = [self.zero_distance]*self.smooth_range # history of distance values

    def calculate_volume(self, new_distance:float) -> float:
        if new_distance != None:
            self.history = self.history[1:]
            self.history.append(new_distance)
        history_avg = sum(self.history) / self.smooth_range
        normalized_avg = min((history_avg / self.zero_distance), 1.0)
        new_volume = 1 - normalized_avg
        scalar = 2
        sigmoid_volume = (new_volume**scalar)/(new_volume**scalar + (1 - new_volume)**scalar)
        return sigmoid_volume


def get_sample_distances() -> list[float]:
    import random
    sample_distances = []
    for _ in range(100):
        sample_distances.append(random.random() * 4)
    return sample_distances


if __name__ == "__main__":
    calc = VolCalc()
    sample_distances = get_sample_distances()
    for line in sample_distances:
        print(f"{calc.calculate_volume(line):.2f}")