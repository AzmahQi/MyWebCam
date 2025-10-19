import argparse
import subprocess
import sys
import cv2 as cv


def get_image():
    img = cv.imread(cv.samples.findFile("sam1.avif"))
    if img is None:
        sys.exit("Could not read the image.")
    cv.imshow("Display window", img)
    k = cv.waitKey(0)
    if k == ord("s"):
        cv.imwrite("sm1-copy.avif", img)




def main():


    # default behaviour: show an example image and print versions
    #get_image()
    print("Hello, World!")
    print(cv.__version__)


if __name__ == "__main__":
    main()
