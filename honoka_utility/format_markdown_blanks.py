import argparse
import re

# from cytoolz import partial
# from functional import seq


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o')
    parser.add_argument('--input', '-i')
    args = parser.parse_args()
    return args


def main():
    args = get_args()

    # format_chap = partial(re.sub, '\n*\n#([^#])', '\n\n\n\n\n#\g<1>')
    # format_sec = partial(re.sub, '\n*\n##([^#])', '\n\n##\g<1>')

    # formatted = seq(open(args.input).read())\
    #     .map(format_chap)\
    #     .map(format_sec)\
    #     .to_list()[0]

    formatted = re.sub('\n*\n#([^#])', '\n\n\n\n\n#\g<1>', open(args.input).read())
    formatted = re.sub('\n*\n##([^#])', '\n\n##\g<1>', formatted)

    open(args.output, 'w').write(formatted)


    ''' code using Option. (not used because we need explicit exception)
        formatted = Option.from_call(open, args.input).map(_.call('read'))\
            .map(format_chap)\
            .map(format_sec)\
            .get_or('[Got None]')

        Option.from_call(open, args.output, 'w')\
            .map(_.call('write', formatted))
    '''


if __name__ == "__main__":
    main()
