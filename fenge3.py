import cv2
import numpy as np

# 读取图像
img = cv2.imread('data/54.jpg')

# 转换为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 进行阈值分割
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# 进行形态学操作，去除噪声和小区域
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# 进行连通区域分析
n, labels, stats, centroids = cv2.connectedComponentsWithStats(opening)

# 找到最大连通区域
max_area = 0
max_label = 0
for i in range(1, n):
    if stats[i, cv2.CC_STAT_AREA] > max_area:
        max_area = stats[i, cv2.CC_STAT_AREA]
        max_label = i

# 提取最大连通区域
mask = np.zeros_like(gray)
mask[labels == max_label] = 255

# 进行形态学操作，填充区域
kernel = np.ones((5, 5), np.uint8)
closed_mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# 进行轮廓检测
contours, hierarchy = cv2.findContours(closed_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
cv2.drawContours(img, contours, -1, (0, 0, 255), 2)

# 显示结果
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
