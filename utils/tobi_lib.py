def hello_world():
    print("Hello world")

def loop_1(counter):
    counter += 1
    print("Hello")
    loop_2(counter)

def loop_2(counter):
    counter += 1
    print("World")
    if counter > 100:
        raise SystemError("100 reached")
    else:
        print(counter)
        loop_1(counter)

if __name__ == "__main__":
    hello_world()