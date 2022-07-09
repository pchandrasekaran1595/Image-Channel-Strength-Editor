import os
import re
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH  = os.path.join(BASE_PATH, "input")
OUTPUT_PATH = os.path.join(BASE_PATH, "output")

if not os.path.exists(OUTPUT_PATH): os.makedirs(OUTPUT_PATH)


def breaker(num: int = 50, char: str = "*") -> None:
    print("\n" + num*char + "\n")


def get_image(path: str) -> np.ndarray:
    return cv2.cvtColor(src=cv2.imread(path, cv2.IMREAD_COLOR), code=cv2.COLOR_BGR2RGB)


def show_image(image, cmap: str = "gnuplot2") -> None:
    plt.figure()
    plt.imshow(image, cmap=cmap)
    plt.axis("off")
    figmanager = plt.get_current_fig_manager()
    figmanager.window.state("zoomed")
    plt.show()


def show_images(
    image_1: np.ndarray,
    image_2: np.ndarray, 
    cmap_1: str="gnuplot2",
    cmap_2: str="gnuplot2",
    title_1: str="Original",
    title_2: str=None,
    ) -> None:

    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(image_1, cmap=cmap_1)
    plt.axis("off")
    if title_1: plt.title(title_1)
    plt.subplot(1, 2, 2)
    plt.imshow(image_2, cmap=cmap_2)
    plt.axis("off")
    if title_2: plt.title(title_2)
    figmanager = plt.get_current_fig_manager()
    figmanager.window.state("zoomed")
    plt.show()


def edit_image(image: np.ndarray, channel: str, factor: float) -> np.ndarray:
    if re.match(r"^red$", channel, re.IGNORECASE): index = 0
    if re.match(r"^green$", channel, re.IGNORECASE): index = 1
    if re.match(r"^blue$", channel, re.IGNORECASE): index = 2
    image = image / 255
    image[:, :, index] = image[:, :, index] * factor
    return np.clip(image / np.max(image) * 255, 0, 255).astype("uint8")


def main():
    args_1: tuple = ("--file", "-f")
    args_2: tuple = ("--channel", "-c")
    args_3: str = "--factor"
    args_4: tuple = ("--save", "-s")

    filename: str = "Test_1.jpg"
    channel: str = "red"
    factor: float = 1.0
    save: bool = False

    if args_1[0] in sys.argv: filename = sys.argv[sys.argv.index(args_1[0]) + 1]
    if args_1[1] in sys.argv: filename = sys.argv[sys.argv.index(args_1[1]) + 1]

    if args_2[0] in sys.argv: channel = sys.argv[sys.argv.index(args_2[0]) + 1]
    if args_2[1] in sys.argv: channel = sys.argv[sys.argv.index(args_2[1]) + 1]

    if args_3 in sys.argv: factor = float(sys.argv[sys.argv.index(args_3) + 1])

    if args_4[0] in sys.argv or args_4[1] in sys.argv: save = True

    assert filename is not None, "Enter an argument for --file | -f"
    assert filename in os.listdir(INPUT_PATH), "File Not Found"

    assert channel is not None, "Enter an argument for --channel | -c"
    assert re.match(r"^blue$", channel, re.IGNORECASE) \
        or re.match(r"^green$", channel, re.IGNORECASE) \
        or re.match(r"^red$", channel, re.IGNORECASE), "Invalid Channel"

    image = get_image(os.path.join(INPUT_PATH, filename))
    edited_image = edit_image(image, channel, factor)

    if save: cv2.imwrite(os.path.join(OUTPUT_PATH, filename.split(".")[0] + " - Edited.jpg"), cv2.cvtColor(src=edited_image, code=cv2.COLOR_RGB2BGR))
    else: show_images(image_1=image, image_2=edited_image, title_2="Edited")
    

if __name__ == "__main__":
    sys.exit(main() or 0)
