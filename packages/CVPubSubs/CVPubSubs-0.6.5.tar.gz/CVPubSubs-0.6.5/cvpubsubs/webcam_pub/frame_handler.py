import threading

import numpy as np

from cvpubsubs.webcam_pub.pub_cam import pub_cam_thread
from cvpubsubs.webcam_pub.camctrl import CamCtrl
from cvpubsubs.window_sub.winctrl import WinCtrl
from cvpubsubs.serialize import uid_for_source

if False:
    from typing import Union, Tuple, Any, Callable, List, Optional

    FrameCallable = Callable[[np.ndarray, int], Optional[np.ndarray]]

from cvpubsubs.callbacks import global_cv_display_callback

display_callbacks = [global_cv_display_callback]


class VideoHandlerThread(threading.Thread):
    "Thread for publishing frames from a video source."

    def __init__(self, video_source=0,  # type: Union[int, str, np.ndarray]
                 callbacks=(),  # type: Union[List[FrameCallable], FrameCallable]
                 request_size=(-1, -1),  # type: Tuple[int, int]
                 high_speed=True,  # type: bool
                 fps_limit=240  # type: float
                 ):
        """Sets up the main thread loop.

        :param video_source: The video or image source. Integers typically access webcams, while strings access files.
        :type video_source: Union[int, str]
        :param callbacks: A list of operations to be performed on every frame, including publishing.
        :type callbacks: List[Callable[[np.ndarray, int], Any]]
        :param request_size: Requested video size. Actual size may vary, since this is requesting from the hardware.
        :type request_size: Tuple[int, int]
        :param high_speed: If true, use compression to increase speed.
        :type high_speed: bool
        :param fps_limit: Limits frames per second.
        :type fps_limit: float
        """
        super(VideoHandlerThread, self).__init__(target=self.loop, args=())
        self.cam_id = uid_for_source(video_source)
        self.video_source = video_source
        if callable(callbacks):
            self.callbacks = [callbacks]
        else:
            self.callbacks = callbacks
        self.request_size = request_size
        self.high_speed = high_speed
        self.fps_limit = fps_limit
        self.exception_raised = None

    def loop(self):
        """Continually gets frames from the video publisher, runs callbacks on them, and listens to commands."""
        t = pub_cam_thread(self.video_source, self.request_size, self.high_speed, self.fps_limit)
        while str(self.cam_id) not in CamCtrl.cv_cams_dict:
            continue
        sub_cam = CamCtrl.cam_frame_sub(str(self.cam_id))
        sub_owner = CamCtrl.handler_cmd_sub(str(self.cam_id))
        msg_owner = sub_owner.return_on_no_data = ''
        while msg_owner != 'quit':
            frame = sub_cam.get(blocking=True, timeout=1.0)  # type: np.ndarray
            if frame is not None:
                frame_c = None
                for c in self.callbacks:
                    try:
                        frame_c = c(frame)
                    except TypeError as te:
                        raise TypeError("Callback functions for cvpubsub need to accept two arguments: array and uid")
                    except Exception as e:
                        self.exception_raised = e
                        frame = frame_c = self.exception_raised
                        CamCtrl.stop_cam(self.cam_id)
                        WinCtrl.quit()
                        raise e
                if frame_c is not None:
                    global_cv_display_callback(frame_c, self.cam_id)
                else:
                    global_cv_display_callback(frame, self.cam_id)
            msg_owner = sub_owner.get()
        sub_owner.release()
        sub_cam.release()
        CamCtrl.stop_cam(self.cam_id)
        t.join()

    def display(self,
                callbacks=()  # type: List[Callable[[List[np.ndarray]], Any]]
                ):
        from cvpubsubs.window_sub import SubscriberWindows

        """Default display operation. For multiple video sources, please use something outside of this class.

        :param callbacks: List of callbacks to be run on frames before displaying to the screen.
        :type callbacks: List[Callable[[List[np.ndarray]], Any]]
        """
        self.start()
        SubscriberWindows(video_sources=[self.cam_id], callbacks=callbacks).loop()
        self.join()
        if self.exception_raised is not None:
            raise self.exception_raised
