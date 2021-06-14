import sys

try:
    for i in range(1, len(sys.argv), 3):
        filename = sys.argv[i]
        title = sys.argv[i + 1]
        color = sys.argv[i + 2]

    # do stuff

    print('RESULT: output.xslx, image1.png, image2.png, image3.png')

except Exception as e:
    print(e, file=sys.stderr)
    sys.exit(1)