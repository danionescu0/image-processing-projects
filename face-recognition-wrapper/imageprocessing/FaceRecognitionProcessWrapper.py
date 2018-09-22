from multiprocessing import Queue

from imageprocessing.FaceRecognitionProcess import FaceRecognitionProcess
from imageprocessing.FaceRecognition import FaceRecognition


class FaceRecognitionProcessWrapper:
    def __init__(self, face_recognition: FaceRecognition, nr_threads: int) -> None:
        self.__face_recognition = face_recognition
        self.__nr_threads = nr_threads
        self.__input_queue = None
        self.__output_queue = None
        self.__process_list = []

    def start(self):
        self.__input_queue = Queue(maxsize=self.__nr_threads)
        self.__output_queue = Queue(maxsize=self.__nr_threads)

        for thread_nr in range(self.__nr_threads):
            process = FaceRecognitionProcess(self.__face_recognition, self.__input_queue, self.__output_queue)
            process.daemon = True
            process.start()
            self.__process_list.append(process)

    def put_image(self, image):
        self.__empty_input_queue()
        try:
            self.__input_queue.put(image, block=False)
        except:
            pass

    def get_result(self):
        if self.__output_queue.qsize() > 0:
            try:
                return self.__output_queue.get(block=False)
            except:
                return None, None
        return None, None

    def __empty_input_queue(self):
        while not self.__input_queue.empty():
            try:
                self.__input_queue.get(block=False)
            except:
                return
