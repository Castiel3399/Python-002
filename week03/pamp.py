import argparse
import telnetlib
import threading
from queue import Queue

from ping3 import ping


class ScanIP(threading.Thread):

    def __init__(self, thread_id, ipQueue):
        super(ScanIP, self).__init__()
        self.ipQueue = ipQueue
        self.thread_id = thread_id

    def run(self):
        '''
        重写run方法
        '''
        print(f'启动线程：{self.thread_id}')
        self.scanPing()
        print(f'结束线程：{self.thread_id}')

    def scanPing(self):
        while True:
            if self.ipQueue.empty():
                break
            else:
                ip=self.ipQueue.get()
                resonse = ping(ip)
                if resonse is not None:
                    print('{0} 可以ping通 '.format(ip))


class TcpIp(threading.Thread):
    def __init__(self, thread_id, ip, ipQueue):
        super(TcpIp, self).__init__()
        self.ip = ip
        self.thread_id = thread_id
        self.portQueue = ipQueue

    def run(self):
        '''
        重写run方法
        '''
        print(f'启动线程：{self.thread_id}')
        self.scanPortThread()
        print(f'结束线程：{self.thread_id}')

    def scanPortThread(self):
        while True:
            if self.portQueue.empty():
                break
            else:
                try:
                    port = self.portQueue.get()
                    server = telnetlib.Telnet()
                    server.open(self.ip, port)
                    file = open('port.json', 'a', encoding='utf-8')
                    file.write(self.ip + ':' +port + '\n')
                    file.close()
                    print('{0} port {1} is open'.format(self.ip, port))
                except Exception as e:
                    print('{0} port {1} is off'.format(self.ip, port))
                    print(e)

    # IP 转换list


def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]


def num2ip(num):
    return '%s.%s.%s.%s' % ((num & 0xff000000) >> 24,
                            (num & 0x00ff0000) >> 16,
                            (num & 0x0000ff00) >> 8,
                            num & 0x000000ff)

    # 把输入的ip范围组合成一个list形式


def get_ip(ip):
    start, end = [ip2num(x) for x in ip.split('-')]
    return [num2ip(num) for num in range(start, end + 1) if num & 0xff]


if __name__ == '__main__':
    '''define parameter'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', nargs=1, type=int, required=True)
    parser.add_argument('-f', nargs=1, type=str, required=True)
    parser.add_argument('-ip', nargs=1, type=str, required=False)
    args = parser.parse_args()
    thread_num = args.n[0]
    cmd= args.f[0]
    ip=args.ip[0]
    print(thread_num)
    print(cmd)
    print(ip)

    # 任务队列，存放IP/port队列
    ipQueue = Queue(1024)
    ip_threads = []
    if (cmd == 'ping'):
        iplist = get_ip(ip)
        print(iplist)
        for i in iplist:
            ipQueue.put(i)

        for i in range(0, thread_num):
            thread = ScanIP(i, ipQueue)
            thread.start()
            ip_threads.append(thread)
    elif (cmd == 'tcp'):
        for i in range(1,1024):
            ipQueue.put(i)
        for i in range(0, thread_num):
            thread = TcpIp(i,ip,ipQueue)
            thread.start()
            ip_threads.append(thread)
    else:
        print('命令错误')

    for t in ip_threads:
        t.join()
