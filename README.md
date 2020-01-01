# Purpose

The purpose of this script is to take two folder of images (a and b) and merge into another folder (c), in the following way :

-   Every images in (a) and (b) have their order considered (by their filename)
-   Images in (a) and (b) can be compared with a threshold to determine if they are related (considered as the same image).
-   (b) is considered as the reference. We use comparison of imagehash for this task.
-   If images in (a) are not in (b), these images are removed. (Extra image)
-   If images in (b) are not in (a), these images are added. (Missing image)
-   If an image is both in (a) and (b), the image from (a) is kept. (New image)

The script can be used for example to create a new folder of image (c) based on a scanlation of a manga (a)
and the original manga (b).
(c) will contain the original manga with the page translated but without the images added by the scanlation team.

# How to use it ?

## Install

```bash
git clone https://github.com/TheRaphael0000/diff_and_merge_raw_translation
cd diff_and_merge_raw_translation
pip install -r requirements.txt
```

## Example

```bash
python cli.py --help
python cli.py "translation" "raw" "output" -t 17 -y -q
```

# TODO

-   [x] Algorithm
-   [x] CLI
-   [ ] Use os.walk instead of os.listfiles when loading images to handle subfolder, and also verify that we only load images without crashes.
-   [ ] GUI : to check that the diff&merge is correct and to adapt the threshold
-   [ ] README.md : Visual example of the algorithm.
-   [ ] Package : Create a proper python package
-   [ ] Setuptools : Create the setup.py script (include a script to run the cli and the gui)
-   [ ] Pypi : Publish to pypi
