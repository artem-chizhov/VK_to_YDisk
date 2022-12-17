from progress.bar import IncrementalBar
import time

def progress_bar(text:str, count:int):
    bar = IncrementalBar(text, max = count)
    bar.next()
    time.sleep(1.12)
def progress_bar_stop():
    IncrementalBar().finish()