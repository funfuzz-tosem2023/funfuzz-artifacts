import os

if __name__ == '__main__':
    flag = not not os.getenv('TEST')
    print(flag)
