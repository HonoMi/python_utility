import argparse
import re
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default=sys.stdout)
    parser.add_argument('--input', '-i', default=sys.stdin)
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    lines = [line.rstrip()
             for line in open(args.input).readlines()]

    line_level = []
    level_pre = -1
    spaces_pre = ''
    for line in lines:
        if not any([re.match(r'^\s*[-\*] .*', line), re.match(r'^\s*[0-9]\.', line), re.match(r'^\s\s*\S.*', line)]):
            level_pre = -1
            line_level.append((line, -1, False, None))
            continue

        def get_movement(pre, cur):
            diff = cur - pre
            if diff > 0:
                return 1
            elif diff == 0:
                return 0
            else:
                return cur - pre

        spaces_cur = re.sub(r'^([\s]*).*', r'\g<1>', line)
        level_cur = 0
        if level_pre == -1:
            level_cur = 0
        else:
            level_cur = level_pre + get_movement(int(len(spaces_pre) / 4), int(len(spaces_cur) / 4))

        line_content = None
        item_no = None
        with_itemize = True
        if re.match('^\s*[0-9]\..*', line):
            line_content = re.sub(r'^\s*[0-9]*\. (.*)', r'\g<1>', line)
            item_no = re.sub(r'^\s*([0-9])*\..*', r'\g<1>', line)
        elif re.match(r'^\s*[-\*] .*', line):
            line_content = re.sub(r'^\s*[-\*] (.*)', r'\g<1>', line)
            with_itemize = True
        else:
            line_content = re.sub(r'^\s*(.*)', r'\g<1>', line)
            with_itemize = False

        line_level.append((line_content, level_cur, with_itemize, item_no))
        level_pre = level_cur
        spaces_pre = spaces_cur

    f_out = args.output if args.output == sys.stdout else open(args.output, 'w')
    for line_content, level, with_itemize, item_no in line_level:
        if level < 0:
            print(line_content, file=f_out)
        else:
            itemization_mark = ''
            if item_no is not None:
                itemization_mark = item_no + '. '
            else:
                if with_itemize:
                    itemization_mark = '* ' if level % 2 == 0 else '- '
            print(''.join(['    '] * level) + itemization_mark + line_content, file=f_out)
    f_out.close()

if __name__ == "__main__":
    main()
