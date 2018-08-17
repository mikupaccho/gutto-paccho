import csv
import numpy as np


def get_katakanas_and_weights(tsv_file_path):
    assert tsv_file_path.endswith('.tsv')

    katakanas, weights = [], []
    with open(tsv_file_path, newline='') as f:
        reader = csv.reader(f, delimiter='\t', quotechar='"')
        for row in reader:
            katakanas.append(row[0])
            weights.append(int(row[1]))
    weights = np.array(weights) / sum(weights)

    return katakanas, weights
