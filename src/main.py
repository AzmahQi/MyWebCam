import sys
import cv2 as cv


def get_image():
    img = cv.imread("samples/sample1.jpg")
    if img is None:
        sys.exit("Could not read the image.")
    cv.imshow("Display window", img)
    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("samples/sample1-copy.jpg", img)




def main():

    get_image()
    # default behaviour: show an example image and print versions
    #get_image()
    print("Hello, World!")
    print(cv.__version__)


if __name__ == "__main__":
    main()
