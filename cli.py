import argparse

from diff_and_merge import DiffMerge


def parse_args():
    description = """Merge two folder containing images, the first source
    folder (a) the second source folder (b) into a destination folder (c).

    Two images that look the same are considered the same. This can be tweaked
    with the threshold.

    To create (c). The script read every images in alphabetic order from both
    (a) and (b) and find the differences in the two folders
    (like the diff command). Then it takes (b) as a reference and
    replace every images that are the same in (a).

    So the output is like (b) but with the images of (a).
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("a", help="Source folder (a)")
    parser.add_argument("b", help="Source folder (b)")
    parser.add_argument("c", help="Destination folder (c)")

    parser.add_argument(
        "-t", "--threshold", type=int, default=15,
        help="""0 : Must be nearly exactly the same
        50 : Nearly every image are considered the same""")

    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Don't output anything to stdout")
    parser.add_argument(
        "-y", "--yes", action="store_true",
        help="Don't ask for user validation, always yes")

    return parser.parse_args()


def printq(*arg, **argv):
    if printq.bool:
        return print(*arg, **argv)


printq.bool = True


def pipeline(args):
    printq.bool = not args.quiet
    diff_merge = DiffMerge(args.a, args.b, args.c, args.threshold)
    printq("load")
    diff_merge.load()
    printq("diff_and_merge")
    diff_merge.diff_and_merge()
    printq("create_merge")
    diff_merge.create_merge()

    max_src = max([len(x[0]) for x in diff_merge.merge_paths])
    max_dst = max([len(x[1]) for x in diff_merge.merge_paths])

    form = "{:" + str(max_src) + "} -> {:" + str(max_dst) + "}"
    for src, dst in diff_merge.merge_paths:
        printq(form.format(src, dst))

    if not args.yes:
        is_ok = False
        while True:
            try:
                answer = input("Is ok ? [Y/n] : ")
            except KeyboardInterrupt:
                printq("n")
                answer = "n"

            if answer.lower() == "y" or answer == "":
                is_ok = True
                break
            if answer.lower() == "n":
                is_ok = False
                break
    else:
        is_ok = True

    if is_ok:
        printq("merge")
        diff_merge.merge()
        printq("done.")
    else:
        printq("aborted.")


def main():
    args = parse_args()
    pipeline(args)


if __name__ == '__main__':
    main()
