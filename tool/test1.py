from gooey import Gooey, GooeyParser


@Gooey()
def main():
    parser = GooeyParser(description='阿道夫')

    parser.add_argument(
        '啊幅度萨芬',
        metavar='案说法',
        help='阿斯蒂')

    parser.add_argument(
        '-f', '--foo',
        metavar='Some Flag',
        action='store_true',
        help='I turn things on and off')

    args = parser.parse_args()
    print('Hooray!')


if __name__ == '__main__':
    main()