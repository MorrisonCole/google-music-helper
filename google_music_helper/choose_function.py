import sys


def query_intended_function(question, valid_range):
    prompt = "Response (%r..%r): " % (valid_range[0], valid_range[-1])

    while True:
        sys.stdout.write(question + prompt)
        choice = int(raw_input())
        if choice in valid_range:
            return choice
        else:
            sys.stdout.write("Please respond with an integer in the range %r..%r\n" % (valid_range[0], valid_range[-1]))