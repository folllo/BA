
times = []
file = open("aStarTimes.txt")
for line in file:
    tmp = float(line.rstrip())
    times.append(tmp)

countSmallerThanZero = len([i for i in times if int(i) == 0])
countBtwZeroAndTen = len([i for i in times if  10 > int(i) > 0])
countBtwTenAndOnehundred = len([i for i in times if 100 > int(i) >= 10])
countLargerThanOnehundred = len([i for i in times if int(i) >= 100])

print(len(times))
print("x <= 0:        ", countSmallerThanZero)
print("0 < x < 10:    ", countBtwZeroAndTen)
print("10 <= x < 100: ", countBtwTenAndOnehundred)
print("x >= 100:      ", countLargerThanOnehundred)
