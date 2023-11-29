import cv2

image = cv2.imread("MAP_1_PIXELART_DOUBLE.png")
#cv2.imshow("ori",image)
#cv2.waitKey()

GOAL_SIZE = (90,195)

resize = cv2.resize(image, GOAL_SIZE, interpolation= cv2.INTER_LINEAR)
gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
print(gray)
cv2.imwrite("gray.png",gray)

for i in range(0, GOAL_SIZE[1]):
    for j in range(0, GOAL_SIZE[0]):
        if gray[i,j] > 200:
            gray[i,j]= 255
        elif gray[i,j] < 170:
            gray[i,j]= 0
        else: gray[i,j] = 125

csv = gray.copy()
for i in range(0, GOAL_SIZE[1]):
    for j in range(0, GOAL_SIZE[0]):
        if csv[i,j] == 255:
            csv[i,j]= 0
        elif csv[i,j] == 0:
            csv[i,j]= 2
        else: csv[i,j] = 1


csv_cache = []
for row in csv:
    tmp = []
    for col in row:
        tmp.append(str(col))
    csv_cache.append(tmp)

with open('floor_plan_weiling.csv', 'w') as f:
    for row in csv_cache:
        f.write(','.join(row) + '\n')

cv2.imshow("down",gray)
cv2.waitKey()
cv2.imshow("csv",csv)
cv2.waitKey()
