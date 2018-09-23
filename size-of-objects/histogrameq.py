import cv2
import numpy as np

original = [5, 3, 1, 0, 1, 0, 2, 1, 0, 5, 1, 5, 0, 1, 2, 4, 2, 6, 2, 1, 6, 2, 0, 1, 5]
L = 7  # max intensity
hist = [0, 0, 0, 0, 0, 0, 0, 0]
cumHist = [0, 0, 0, 0, 0, 0, 0, 0]
transformed = []
lut = []
for i in range(25):
    transformed.append(0)
    lut.append(0)
row = ""
# show original
print("original is: ")
for i in range(len(original)):
    row += str(original[i])+' '
    if (i + 1) % 5 == 0:
        print(row)
        row = ""
# histogram
for i in original:
    hist[i] += 1
print("histogram values: ")
print(hist)

# cumulative histogram
# also build a lookup table to tranform the image
sum = 0
for i in range(len(hist)):
    # print("sum = " + str(sum))
    sum += hist[i]
    cumHist[i] = sum
    lut[i] = sum * L / (len(original))
print("cumulative histogram: ")
print(cumHist)

# tranform using look up table (s from the slide)
for i in range(len(original)):
    transformed[i] = int(lut[original[i]])
    # print(str(lut[i]))

print("result: ")
row = ""
for i in range(len(transformed)):
    row += str(transformed[i])+' '
    if (i + 1) % 5 == 0:
        print(row)
        row = ""
