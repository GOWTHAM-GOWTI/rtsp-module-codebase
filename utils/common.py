import cv2

from yolo.object_detection import do_inference

def gen_frames(rtsp_stream):  
    while True:
        success, frame = rtsp_stream.read()
        if not success:
            break
        else:
            frame = do_inference(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')