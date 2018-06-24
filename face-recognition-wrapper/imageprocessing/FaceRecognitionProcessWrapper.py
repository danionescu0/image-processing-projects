from multiprocessing import Queue

from imageprocessing.FaceRecognitionProcess import FaceRecognitionProcess
from imageprocessing.FaceRecognition import FaceRecognition


class FaceRecognitionProcessWrapper:
    def __init__(self, face_recognition: FaceRecognition, queue_size: int, nr_threads: int) -> None:
        self.__face_recognition = face_recognition
        self.__nr_threads = nr_threads
        self.__input_queue = None
        self.__output_queue = None
        self.__queue_size = queue_size
        self.__process_list = []

    def start(self):
        self.__input_queue = Queue(maxsize=self.__queue_size)
        self.__output_queue = Queue(maxsize=self.__queue_size)

        for thread_nr in range(self.__nr_threads):
            process = FaceRecognitionProcess(self.__face_recognition, self.__input_queue, self.__output_queue)
            process.daemon = True
            process.start()
            self.__process_list.append(process)

    def put_image(self, image):
        self.__input_queue.put(image)

    def get_result(self):
        if self.__output_queue.qsize() > 0:
            return self.__output_queue.get()

        return None, None