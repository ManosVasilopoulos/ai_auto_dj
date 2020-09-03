import time


class TimeHandler:
    cue_current: float
    cue_next: float
    start_mix_current: float
    start_mix_next: float
    stop_mix_current: float
    stop_mix_next: float
    pitch_percentage_next: float
    t_mix_current: float
    t_mix_next: float

    def __init__(self, pois_current: list, pois_next: list, pitch_percentage_next: float):
        if abs(pitch_percentage_next) > 1:
            raise Exception('TimeHandlerError: "pitch_percentage_next" cannot be greater than 1 or less than -1.'
                            ' Given value: ' + str(pitch_percentage_next))
        if not pois_current:
            pois_current = [0, 0, 0]
            pitch_percentage_next = 0

        self.cue_current = pois_current[0]
        self.cue_next = pois_next[0]
        self.start_mix_current = pois_current[1]
        self.start_mix_next = pois_next[1]
        self.stop_mix_current = pois_current[2]
        self.stop_mix_next = pois_next[2]

        self.pitch_percentage_next = pitch_percentage_next

        self.t_mix_current = self.stop_mix_current - self.start_mix_current
        self.t_mix_next = self.stop_mix_next - self.start_mix_next

        self.t_cue_to_startmix_next = self.start_mix_next - self.cue_next

        self.t_to_mix_next = self.__calculate_to_mix_next()

    def __calculate_to_mix_next(self):
        A_star_next = self.t_mix_current
        D_next = self.t_cue_to_startmix_next

        t_to_mix_next = D_next - A_star_next * (1 + self.pitch_percentage_next)
        return t_to_mix_next

    @staticmethod
    def sleep_for(seconds: float):
        time.sleep(seconds)
