# -*- coding:utf-8 -*-
import sys
import pickle
import argparse
import traceback

from .custom_request import Request


class SpiderFeeder(object):

    def __init__(self, crawlid, spiderid, url,
                 urls_file, priority, port, host, custom):
        self.crawlid = crawlid
        self.spiderid = spiderid
        self.url = url
        self.urls_file = urls_file
        self.priority = priority
        self.port = port
        self.host = host
        self.custom = custom
        self.inc = 0
        self.failed_count, self.failed_rate, self.sucess_rate = 0, 0, 0

        if self.custom:
            from custom_redis.client import Redis
        else:
            from redis import Redis

        self.redis_conn = Redis(host=self.host, port=self.port)
        self.clean_previous_task(self.crawlid)

    def clean_previous_task(self, crawlid):
        failed_keys = self.redis_conn.keys("failed_download_*:%s" % crawlid)
        for fk in failed_keys:
            self.redis_conn.delete(fk)
        self.redis_conn.delete("crawlid:%s" % crawlid)
        self.redis_conn.delete("crawlid:%s:model" % crawlid)

    def start(self):
        success_rate, failed_rate = 0, 0
        # item抓取
        if self.urls_file:
            with open(self.urls_file) as f:
                lst = f.readlines()
                lines_count = len(lst)
                for index, url in enumerate(lst):
                    req = Request(
                        url=url.strip("\357\273\277\r\n"),
                        callback="parse_item",
                        meta={"crawlid": self.crawlid,
                              "spiderid": self.spiderid,
                              "priority": self.priority}
                    )
                    self.failed_count += self.feed(
                        self.get_name(), pickle.dumps(req))
                    success_rate, failed_rate = \
                        self.show_process_line(
                            lines_count, index + 1, self.failed_count)
                self.redis_conn.hset(
                    "crawlid:%s" % self.crawlid, "total_pages", lines_count)
        # 分类抓取
        else:
            url_list = self.url.split("     ")
            lines_count = len(url_list)

            for index, url in enumerate(url_list):
                req = Request(
                    url=url.strip(),
                    callback="parse",
                    meta={"crawlid": self.crawlid,
                          "spiderid": self.spiderid,
                          "priority": self.priority}
                )
                self.failed_count += self.feed(
                    self.get_name(), pickle.dumps(req))
                sucess_rate, failed_rate = self.show_process_line(
                    lines_count, index + 1, self.failed_count)
        print("\ntask feed complete. sucess_rate:%s%%, failed_rate:%s%%" % (
            success_rate, failed_rate))

    def get_name(self):
        return "{sid}:request:queue".format(sid=self.spiderid)

    def feed(self, queue_name, req):
        if self.custom:
            from custom_redis.client.errors import RedisError
        else:
            from redis import RedisError
        try:
            self.redis_conn.zadd(queue_name, req, -self.priority)
            return 0
        except RedisError:
            traceback.print_exc()
            return 1

    def show_process_line(self, count, num, failed):
        per = count / 100
        success = num - failed
        success_rate = success * 100.0 / count
        failed_rate = failed * 100.0 / count
        str_success_rate = "%.2f%%  " % success_rate
        str_failed_rate = "%.2f%%  " % failed_rate

        if num >= self.inc:
            self.inc += per
            if sys.platform == "win32":
                import ctypes
                std_out_handle = ctypes.windll.kernel32.GetStdHandle(-11)
                color_ctl = ctypes.windll.kernel32.SetConsoleTextAttribute
                color_ctl(std_out_handle, 2)
                print("\r", str_success_rate, "")
                color_ctl(std_out_handle, 32)
                print(int(success_rate * 30 / 100) * ' ', "")
                if int(failed_rate):
                    color_ctl(std_out_handle, 64)
                    print(int(failed_rate * 30 / 100) * ' ', "")
                color_ctl(std_out_handle, 0)
                color_ctl(std_out_handle, 4)
                print(str_failed_rate, "")
                color_ctl(std_out_handle, 7)
            else:
                print("\r", str_success_rate, "")
                print("%s%s" % (int(success_rate * 50 / 100) * '\033[42m \033[0m',
                                int(failed_rate * 50 / 100) * '\033[41m \033[0m'),
                      str_failed_rate)
        return success_rate, failed_rate
