import sys

try:
    raise Exception("Wow!")
except:
    t, v, tb  = sys.exc_info()
    print(f"Error: {t}, {v}\nFrame: {tb.tb_frame}")