import os
import re
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt


READ_PATH = "Files"
SAVE_PATH = "Processed"
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)


def edit(image: np.ndarray, channel: str, factor: float) -> np.ndarray:
    if re.match(r"^blue$", channel, re.IGNORECASE): index = 0
    if re.match(r"^green$", channel, re.IGNORECASE): index = 1
    if re.match(r"^red$", channel, re.IGNORECASE): index = 2
    image = image / 255
    image[:, :, index] = image[:, :, index] * factor
    return np.clip(image / np.max(image) * 255, 0, 255).astype("uint8")


def show(image, cmap: str = "gnuplot2") -> None:
    plt.figure()
    plt.imshow(image, cmap=cmap)
    plt.axis("off")
    figmanager = plt.get_current_fig_manager()
    figmanager.window.state("zoomed")
    plt.show()


def run():
    args_1: tuple = ("--file", "-f")
    args_2: tuple = ("--channel", "-c")
    args_3: tuple = ("--save", "-s")

    filename: str = None
    channel: str = None
    factor: float = 1.0
    save: bool = False

    if args_1[0] in sys.argv: filename = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: filename = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: 
        channel = sys.argv[sys.argv.index(args_2[0]) + 1]
        factor = float(sys.argv[sys.argv.index(args_2[0]) + 2])
    if args_2[1] in sys.argv: 
        channel = sys.argv[sys.argv.index(args_2[1]) + 1]
        factor = float(sys.argv[sys.argv.index(args_2[1]) + 2])

    if args_3[0] in sys.argv or args_3[1] in sys.argv: save = True

    assert filename is not None, "Enter an argument for --file | -f"
    assert filename in os.listdir(READ_PATH), "File Not Found"

    assert channel is not None, "Enter an argument for --channel | -c"
    assert re.match(r"^blue$", channel, re.IGNORECASE) or re.match(r"^green$", channel, re.IGNORECASE) or re.match(r"^red$", channel, re.IGNORECASE), "Invalid Channel"
    
    image = cv2.imread(os.path.join(READ_PATH, filename))
    image = edit(image, channel, factor)
    
    if save:
        cv2.imwrite(os.path.join(SAVE_PATH, filename.split(".")[0] + " - Edited.jpg"), image)
    else:
        show(cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB))
