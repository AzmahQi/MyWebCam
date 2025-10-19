"""
Minimal Yunet wrapper for OpenCV's FaceDetectorYN or ONNX fallback.
This is a lightweight adaptation to be used with the demo. It tries to use
cv.FaceDetectorYN (if available in your OpenCV build) or loads an ONNX model
via cv.dnn.
"""
from typing import List
import numpy as np
import cv2 as cv


class YuNet:
    def __init__(self, modelPath, inputSize=[320, 320], confThreshold=0.6,
                 nmsThreshold=0.3, topK=5000, backendId=0, targetId=0):
        self._modelPath = modelPath
        self._inputSize = tuple(inputSize)
        self._confThreshold = confThreshold
        self._nmsThreshold = nmsThreshold
        self._topK = topK
        self._backendId = backendId
        self._targetId = targetId

        # Prefer the built-in FaceDetectorYN when available
        try:
            self._model = cv.FaceDetectorYN.create(
                model=self._modelPath,
                config="",
                input_size=self._inputSize,
                score_threshold=self._confThreshold,
                nms_threshold=self._nmsThreshold,
                top_k=self._topK,
                backend_id=self._backendId,
                target_id=self._targetId)
            self._use_builtin = True
        except Exception:
            # Fallback: load ONNX with DNN and implement a small wrapper
            self._net = cv.dnn.readNet(self._modelPath)
            self._use_builtin = False

    def name(self):
        return self.__class__.__name__

    def setBackendAndTarget(self, backendId, targetId):
        self._backendId = backendId
        self._targetId = targetId

    def setInputSize(self, input_size):
        if self._use_builtin:
            self._model.setInputSize(tuple(input_size))
        else:
            self._inputSize = tuple(input_size)

    def infer(self, image) -> np.ndarray:
        if self._use_builtin:
            faces = self._model.detect(image)
            return np.empty(shape=(0, 5)) if faces[1] is None else faces[1]
        else:
            # Very small wrapper for DNN fallback - behavior may differ
            h, w = image.shape[:2]
            blob = cv.dnn.blobFromImage(image, scalefactor=1.0/255.0, size=self._inputSize,
                                         mean=(0,0,0), swapRB=True, crop=False)
            self._net.setInput(blob)
            out = self._net.forward()
            # For ONNX models with custom output format, downstream code may need adapting.
            return out
