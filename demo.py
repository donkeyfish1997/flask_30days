import numpy as np,cv2

def fill_photo(img, out_path):
    h, w = img.shape[0], img.shape[1]
    side = max(h, w)
    new = np.zeros((side, side, 3), np.uint8)
    new.fill(255)
    if w > h:
        center = ((side - h) / 2.0)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                new[int(i + center), j] = img[i, j]
    else:
        center = ((side - w) / 2.0)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                new[i, int(j + center)] = img[i, j]
    cv2.imwrite(out_path, new)

img = cv2.imread(r'C:\Users\user\PycharmProjects\flask_30days\static\uploads\abc\aaa\photo\16020504713123393.jpg')
print(type(img))
print(dir(img))
fill_photo(img,r'C:\Users\user\Downloads\tmp\aa.jpg')