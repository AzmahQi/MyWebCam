"""
Minimal demo for YuNet face detector (adapted from OpenCV Zoo).
This demo expects a model file in the same directory, by default:
  face_detection_yunet_2023mar.onnx

Install requirements: opencv-python>=4.10
"""
import argparse
import cv2 as cv
from yunet import YuNet


def parse_args():
    parser = argparse.ArgumentParser(description='YuNet demo')
    parser.add_argument('--input', '-i', type=str,
                        help='Path to an input image. Omit to use webcam.')
    parser.add_argument('--model', '-m', type=str, default='face_detection_yunet_2023mar.onnx',
                        help='Model filename (in this directory)')
    parser.add_argument('--vis', '-v', action='store_true', help='Visualize results')
    parser.add_argument('--conf_threshold', type=float, default=0.9)
    parser.add_argument('--nms_threshold', type=float, default=0.3)
    parser.add_argument('--top_k', type=int, default=5000)
    return parser.parse_args()


def visualize(image, results):
    out = image.copy()
    for det in results:
        bbox = det[0:4].astype(int)
        conf = float(det[-1])
        cv.rectangle(out, (bbox[0], bbox[1]), (bbox[0]+bbox[2], bbox[1]+bbox[3]), (0,255,0), 2)
        cv.putText(out, f"{conf:.3f}", (bbox[0], bbox[1]+12), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
    return out


if __name__ == '__main__':
    args = parse_args()
    model = YuNet(modelPath=args.model,
                  inputSize=[320,320],
                  confThreshold=args.conf_threshold,
                  nmsThreshold=args.nms_threshold,
                  topK=args.top_k)

    if args.input:
        img = cv.imread(args.input)
        if img is None:
            raise SystemExit('Could not read input image')
        h, w = img.shape[:2]
        model.setInputSize([w, h])
        results = model.infer(img)
        print(f"{results.shape[0]} faces detected.")
        out = visualize(img, results)
        if args.vis:
            cv.imshow('result', out)
            cv.waitKey(0)
        else:
            cv.imwrite('result.jpg', out)
            print('Saved result.jpg')
    else:
        cap = cv.VideoCapture(0)
        if not cap.isOpened():
            raise SystemExit('Cannot open camera')
        w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        model.setInputSize([w, h])
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = model.infer(frame)
            frame = visualize(frame, results)
            cv.imshow('YuNet demo', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()
