import numpy as np


def count_overlaps(note, notes):
    count = 0
    for n in notes:
        if abs(n.start - note.start) < 0.05:
            count += 1
    return count


def extract_features(notes):

    features = []

    for note in notes:
        duration = note.end - note.start
        overlap = count_overlaps(note, notes)

        features.append([
            note.pitch,
            duration,
            note.velocity,
            overlap
        ])

    return np.array(features)
