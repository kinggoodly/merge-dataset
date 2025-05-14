from collections import Counter
import glob

labels = glob.glob("data/labels/all/*.txt")
counter = Counter()

for path in labels:
    with open(path) as f:
        for line in f:
            class_id = line.strip().split()[0]
            counter[class_id] += 1

print(counter)
