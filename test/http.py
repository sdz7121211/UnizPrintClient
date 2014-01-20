#coding:utf8
'''
Created on 2014-1-13

@author: sdz
'''
#from PyQt4 import QtNetwork
#
#htp = QtNetwork.QHttp(r"http://www.uniz.cc/modelview/content/EiffelTower.7z")
#print htp
#print htp.bytesAvailable()



# coding: utf-8
# KPBroswer.py
# KPBroswer是一个基于QtWebKit的最小化浏览器程序，通过被第三方程序调用，能实现对复杂页面加载后数据（例如，复杂Ajax、数据加密）的抓取，支持屏幕截图。

import sys
import os
import re
import time
from optparse import OptionParser
from PyQt4.QtGui import QApplication, QImage, QPainter
from PyQt4.QtCore import QUrl, QTimer, QDateTime, QEventLoop
from PyQt4.QtWebKit import QWebView
from PyQt4.QtNetwork import QNetworkProxy, QNetworkCookie, QNetworkCookieJar

def to_unicode(obj, encoding='utf8'):
    """转换为unicode类型
    """
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = obj.decode(encoding, 'ignore')
    return obj

class _ExtendedNetworkCookieJar(QNetworkCookieJar):
    def mozillaCookies(self):
        """
        Return all cookies in Mozilla text format:  
        # domain domain_flag path secure_connection expiration name value  
        .firefox.com     TRUE   /  FALSE  946684799   MOZILLA_ID  100103
        """
        def bool2str(value):
            return {True: "TRUE", False: "FALSE"}[value]
        def byte2str(value):
            return str(value)
        def get_line(cookie):
            domain_flag = str(cookie.domain()).startswith(".")
            return "\t".join([
                byte2str(cookie.domain()),
                bool2str(domain_flag),
                byte2str(cookie.path()),
                bool2str(cookie.isSecure()),
                byte2str(cookie.expirationDate().toTime_t()),
                byte2str(cookie.name()),
                byte2str(cookie.value()),
            ])
        lines = [get_line(cookie) for cookie in self.allCookies()]
        return "\n".join(lines)
  
    def setMozillaCookies(self, string_cookies):
        """Set all cookies from Mozilla test format string.
        .firefox.com     TRUE   /  FALSE  946684799   MOZILLA_ID  100103
        """
        def str2bool(value):
            return {"TRUE": True, "FALSE": False}[value]
        def get_cookie(line):
            fields = map(str.strip, line.split("\t"))
            if len(fields) != 7:
                return
            domain, domain_flag, path, is_secure, expiration, name, value = fields
            cookie = QNetworkCookie(name, value)
            cookie.setDomain(domain)
            cookie.setPath(path)
            cookie.setSecure(str2bool(is_secure))
            cookie.setExpirationDate(QDateTime.fromTime_t(int(expiration)))
            return cookie
        cookies = [get_cookie(line) for line in string_cookies.splitlines()
          if line.strip() and not line.strip().startswith("#")]
        self.setAllCookies(filter(bool, cookies))

class KPBroswer:
    def __init__(self, gui=False, timeout=120, cookies=None):
        """gui - 是否显示浏览器窗口
           timeout - 页面加载超时时间（单位：秒）
        """
        self.app = QApplication(sys.argv)
        self.web = QWebView()
        self.web.loadProgress.connect(self.load_progress)
        self.cookiesjar = _ExtendedNetworkCookieJar()
        if cookies:
            self.cookiesjar.setMozillaCookies(string_cookies=cookies)
        self.web.page().networkAccessManager().setCookieJar(self.cookiesjar)
        self.timeout = timeout
        if gui:
            self.web.show()

    def set_proxy(self, proxy):
        """设置代理，代理格式为：ip:port或者username:password@ip:port
        """
        if isinstance(proxy, basestring):
            match = re.match('((?P<username>\w+):(?P<password>\w+)@)?(?P<host>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(:(?P<port>\d+))?', proxy)
            if match:
                groups = match.groupdict()
                username = groups.get('username') or ''
                password = groups.get('password') or ''
                host = groups.get('host')
                port = groups.get('port')
                proxy = QNetworkProxy(QNetworkProxy.HttpProxy, host, int(port), username, password)
            else:
                print 'Invalid proxy:%s' % proxy
                proxy = None
        if proxy:
            QNetworkProxy.setApplicationProxy(proxy)

    def get(self, url):
        """加载页面，等待结束
        """
        self.loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(self.loop.quit)
        self.web.load(QUrl(url))
        timer.start(self.timeout * 1000)
        self.loop.exec_()
    
        if timer.isActive():
            return self.current_html()
        else:
            print 'timeout'
            
    def load_progress(self, load):
        """加载进度
        注意：页面加载完成并不意味页面内容都就位了。
        例如，Ajax动态加载内容，是在页面加载完毕后，才进行的。这是需要借助wait_flag来判断才准确。
        """
        # 页面加载完成
        if load == 100:
            self.loop.exit()
            
    def get_cookie(self):
        """获取Cookie
        """
        return self.cookiesjar.mozillaCookies()
        
    def current_html(self):
        """返回当前页面的HTML，unicode类型
        """
        return unicode(self.web.page().mainFrame().toHtml())
        
    def wait(self, secs=1):
        """等待，主线程不会卡
        """
        deadline = time.time() + secs
        while time.time() < deadline:
            time.sleep(0.1)
            self.app.processEvents()
            
    def wait_flag(self, flags=[], secs=5):
        """等待页面出现预期的标记字符串，用于判断页面内容是否就绪。如果在secs秒内仍未出现，则返回。
        flags - 多个标记字符串，都出现才返回True。每个标记元素支持或条件，例如'Total results|No mached result'。
        secs - 等待的最长时间（单位：秒）
        """
        deadline = time.time() + secs
        def check_flags():
            flags_found = 0
            for flag in flags:
                for item in flag.split('|'):
                    if item in self.current_html():
                        flags_found += 1
                        break
            if len(flags) == flags_found:
                # 所有标记都找到了
                self.loop.exit()
                return True
        while not check_flags() and time.time() < deadline:
            self.wait(1)
        return False
    
    def screenshot(self, output_file):
        """屏幕截图
        """
        frame = self.web.page().mainFrame()
        self.web.page().setViewportSize(frame.contentsSize())
        image = QImage(self.web.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        print 'saving', output_file
        image.save(output_file)    

    def close(self):
        """关闭窗口
        """
        self.web.close()
            
if __name__ == '__main__':
    parser = OptionParser('%prog <URL> [options]')
    parser.add_option('-p', '--proxy', dest='proxy', help='Proxy to use.')
    parser.add_option('-t', '--timeout', dest='timeout', type='int', default=120, help='The timeout time of loading page.')
    parser.add_option('-f', '--flags', dest='flags', help='Flags need to wait for. Semicolon can be used as a eperator.')
    parser.add_option('-w', '--wait_timeout', dest='wait_timeout', type='int', default=60, help='The timeout time of waitting for flags.')
    parser.add_option('-g', '--gui', dest='gui', action='store_true', default=False, help='Whether to show the broswer GUI.')
    parser.add_option('-o', '--output', dest='output', default=None, help='The output filename.')
    parser.add_option('-s', '--screenshot', dest='screenshot', default=None, help='If the value is not empty, take a screenshot and save it here.')
    parser.add_option('-c', '--cookie', dest='cookie', default=None, help='If the value is not empty, save the cookie here.')
    parser.add_option('-d', '--initial_cookie_file', dest='initial_cookie_file', default=None, help='The initial coookies.')
    
    options, args = parser.parse_args()
    if args:
        url = args[0]
        cookies = None
        if options.initial_cookie_file and os.path.exists(options.initial_cookie_file):
            with open(options.initial_cookie_file) as f:
                cookies = f.read()
        broswer = KPBroswer(gui=options.gui, timeout=options.timeout, cookies=cookies)
        if options.proxy:
            # 设置代理
            broswer.set_proxy(options.proxy)
        # 加载页面
        broswer.get(url)
        if options.flags:
            # 等待标记出现
            flags = map(to_unicode, options.flags.split(';'))
            broswer.wait_flag(flags=flags, secs=options.wait_timeout)
        # 保存页面内容
        if options.output:
            html = broswer.current_html()
            if html:
                # 保存前先转为UTF8编码
                html = html.encode('utf8')
                open(options.output, 'w').write(html)
        # 屏幕截图
        if options.screenshot:
            broswer.screenshot(output_file=options.screenshot)
        # 保存cookie
        if options.cookie:
            cookies = broswer.get_cookie()
            if cookies:
                open(options.cookie, 'w').write(cookies)
        broswer.close()
    else:
        parser.print_help()