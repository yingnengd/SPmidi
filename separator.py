import pretty_midi
import numpy as np
from sklearn.cluster import KMeans
from feature_extractor import extract_features


class AdvancedMidiSeparator:

    def __init__(self, midi_path, n_clusters=4):
        self.pm = pretty_midi.PrettyMIDI(midi_path)
        self.notes = []
        for inst in self.pm.instruments:
            self.notes.extend(inst.notes)

        self.n_clusters = n_clusters

    def separate(self):

        features = extract_features(self.notes)

        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        labels = kmeans.fit_predict(features)

        clusters = {}
        for label, note in zip(labels, self.notes):
            clusters.setdefault(label, []).append(note)

        return self.assign_roles(clusters)

    def assign_roles(self, clusters):

        roles = {
            "bass": [],
            "drums": [],
            "melody": [],
            "piano": []
        }

        stats = {}

        for label, notes in clusters.items():
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
                "mean_overlap": np.mean(overlaps)
            }

        # 规则判断角色
        sorted_by_pitch = sorted(stats.items(), key=lambda x: x[1]["mean_pitch"])

        # 最低音域 = bass
        roles["bass"] = clusters[sorted_by_pitch[0][0]]

        # 最高音域 = melody
        roles["melody"] = clusters[sorted_by_pitch[-1][0]]

        # 短音密集 = drums
        drum_label = min(stats.items(), key=lambda x: x[1]["mean_duration"])[0]
        roles["drums"] = clusters[drum_label]

        # 剩余 = piano
        remaining = set(clusters.keys()) - {
            sorted_by_pitch[0][0],
            sorted_by_pitch[-1][0],
            drum_label
        }

        if remaining:
            roles["piano"] = clusters[remaining.pop()]

        return roles
