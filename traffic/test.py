from traffic import * 
from collections import Counter

images, labels = load_data("dataset")

counter = Counter(labels)

for i in range(43):
    if counter.get(i) != 3 and counter.get(str(i)) != 3:
        print(f"Expected 3 labels for category {i}, instead got {counter.get(i)}")

print("Finished")