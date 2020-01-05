import statistics as st

filename = "satTimesWithLowerStartingPoint.txt"


times = []
file = open(filename)
for line in file:
    tmp = float(line.rstrip())
    times.append(tmp)

if filename == "aStarTimes.txt":
    countSmallerThanZero = len([i for i in times if int(i) == 0])
    countBtwZeroAndTen = len([i for i in times if  10 > int(i) > 0])
    countBtwTenAndOnehundred = len([i for i in times if 100 > int(i) >= 10])
    countLargerThanOnehundred = len([i for i in times if int(i) >= 100])
    countLargerThanOnethousand = len([i for i in times if int(i) >= 1000])

    print(len(times))
    print("x <= 0       : ", countSmallerThanZero)
    print("0 < x < 10   : ", countBtwZeroAndTen)
    print("10 <= x < 100: ", countBtwTenAndOnehundred)
    print("x >= 100     : ", countLargerThanOnehundred)
    print("x >= 1000    : ", countLargerThanOnethousand)
    print("Average time : ", st.mean(times))
    x = sum(times)/len(times)
    print(x)

    for time in times:
    	if(int(time) >= 1000):
    		print(time)

elif filename == "satTimes.txt" or filename == "satTimesWithLowerStartingPoint.txt":
    countSmallerThanTen = len([i for i in times if int(i) <= 10])
    countBtwTenAndTwenty = len([i for i in times if  20 > int(i) > 10])
    countBtwTwentyAndFourty = len([i for i in times if  40 > int(i) >= 20])
    countBtwFourtyAndEighty = len([i for i in times if  80 > int(i) >= 40])
    countBtwEightyAndOnehundred = len([i for i in times if  100 > int(i) >= 80])

    print(len(times))
    print("x <= 10      : ", countSmallerThanTen)
    print("20 > x >= 10 : ", countBtwTenAndTwenty)
    print("40 > x >= 20 : ", countBtwTwentyAndFourty)
    print("80 > x >= 40 : ", countBtwFourtyAndEighty)
    print("100 > x >= 80: ", countBtwEightyAndOnehundred)
    print("Average time : ", st.mean(times))

file.close()
