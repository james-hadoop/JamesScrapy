# encoding: utf-8

from scrapy import cmdline
import os


# cmdline.execute("scrapy crawl beijing".split())

def main():
    # os_name = os.name
    # print("os_name=%s" % os_name)

    os_info = os.uname()
    if os_info.sysname == 'Darwin':
        chrome_path = r"/home/james/_AllDocMap/06_Software/chromedriver"
    else:
        chrome_path = r"/Users/qjiang/install/chromedriver"
    print("chrome_path=%s" % chrome_path)


if __name__ == '__main__':
    main()
