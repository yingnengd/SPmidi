import numpy as np


class RoleClassifier:

    def __init__(self, clusters):
        self.clusters = clusters
        self.stats = self.compute_stats()

    def compute_stats(self):

        stats = {}

        for label, notes in self.clusters.items():

            pitches = [n.pitch for n in notes]
            durations = [n.end - n.start for n in notes]

            overlaps = []
            for n in notes:
                overlaps.append(
                    sum(abs(n.start - x.start) < 0.05 for x in notes)
                )

            stats[label] = {
                "mean_pitch": np.mean(pitches),
                "mean_duration": np.mean(durations),
                "mean_overlap": np.mean(overlaps),
                "note_count": len(notes)
            }

        return stats

    def assign_roles(self):

        roles = {
            "bass": [],
            "drums": [],
            "melody": [],
            "piano": []
        }

        stats_items = list(self.stats.items())

        # 1️⃣ 贝斯 = 最低音域
        bass_label = min(stats_items, key=lambda x: x[1]["mean_pitch"])[0]
        roles["bass"] = self.clusters[bass_label]

        # 2️⃣ 鼓 = 最短时值
        drum_label = min(stats_items, key=lambda x: x[1]["mean_duration"])[0]
        roles["drums"] = self.clusters[drum_label]

        # 3️⃣ 旋律 = 最高音域
        melody_label = max(stats_items, key=lambda x: x[1]["mean_pitch"])[0]
        roles["melody"] = self.clusters[melody_label]

        # 4️⃣ 剩余 = 钢琴
        used = {bass_label, drum_label, melody_label}
        remaining = set(self.clusters.keys()) - used

        if remaining:
            piano_label = remaining.pop()
            roles["piano"] = self.clusters[piano_label]

        return roles
