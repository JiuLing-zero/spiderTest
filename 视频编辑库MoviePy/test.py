import matplotlib.pyplot as plt
import numpy as np
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

from moviepy.editor import *

x = np.linspace(-2, 2, 200)

duration = 20

fig, ax = plt.subplots()


def make_frame(t):
    ax.clear()
    ax.plot(x, np.sinc(x ** 2) + np.sin(x + 2 * np.pi / duration * t), lw=3)
    ax.set_ylim(-1.5, 2.5)
    return mplfig_to_npimage(fig)

animation = VideoClip(make_frame, duration=duration)
animation.ipython_display(fps=20, loop=True, autoplay=True)



# 从本地载入视频__temp__.mp4并截取00:00:05 - 00:00:15部分
clip = VideoFileClip("__temp__.mp4").subclip(5, 15)

# 调低音频音量 (volume x 0.8)
clip = clip.volumex(0.8)

# 做一个txt clip. 自定义样式，颜色
txt_clip = TextClip("my first clip", fontsize=70, color='blue')

# 文本clip在屏幕中央持续显示10秒
txt_clip = txt_clip.set_pos('center').set_duration(10)

# 把 text clip 的内容覆盖 video clip
video = CompositeVideoClip([clip, txt_clip])

# 把最后生成的视频导出到文件内
video.write_videofile("my_edited.mp4")