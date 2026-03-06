import cv2
import numpy as np

# Create a white image
img = np.ones((200, 400, 3), dtype=np.uint8) * 255

# Write some text on it
cv2.putText(img, "MILK $4.00", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
cv2.putText(img, "BREAD $2.50", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Save it as receipt.jpg
cv2.imwrite("receipt.jpg", img)
print("Physical test image 'receipt.jpg' created!")