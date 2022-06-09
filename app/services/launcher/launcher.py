import multiprocessing as mp
from app.services.gesture_recognizer import case_start

q_output = mp.Queue()
process_status = mp.Manager().Value('process_status', 0)


def run():
    global q_output, process_status
    case = mp.Process(target=case_start, args=(q_output, process_status), daemon=True)
    case.start()


def stop():
    global process_status
    process_status.set(0)

