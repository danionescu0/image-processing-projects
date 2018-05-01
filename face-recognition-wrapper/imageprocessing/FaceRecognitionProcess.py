from multiprocessing import Process, Queue

from imageprocessing.FaceRecognition import FaceRecognition


class FaceRecognitionProcess(Process):
    def __init__(self, face_recognition: FaceRecognition, input_queue: Queue, output_queue: Queue):
        Process.__init__(self)
        self.__face_recognition = face_recognition
        self.__input_queue = input_queue
        self.__output_queue = output_queue
        self.__stop = False

    def stop_process(self):
        self.__stop = True

    def process_image(self, image):
        faces = self.__face_recognition.find(image)
        if len(faces) > 0 and not self.__output_queue.full():
            self.__output_queue.put((image, faces))

    def __get_image(self):
        if not self.__input_queue.empty():
            return True, self.__input_queue.get()
        else:
            return False, None

    def run(self):
        while not self.__stop:
            has_frame, frame = self.__get_image()
            if has_frame:
                self.process_image(frame)