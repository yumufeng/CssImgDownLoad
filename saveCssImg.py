# coding: utf-8 -*-
import urllib
import re, os
from urllib.parse import urljoin
from urllib.request import urlopen


class saveCssBackImg():
    def __init__(self, cssUrl, savePath, outInfo):

        self.cssUrl = cssUrl
        self.savePath = mkdir(savePath)
        self.outInfo = outInfo

    def saveImg(self):
        counter = 1
        errnum = 0
        imgList = self.getImgList()
        img_num = len(imgList)

        for img in imgList:
            img = img.strip("'")
            img = img.strip('"')

            if re.match('^https?://', img):
                imgsrc = img.split('?')[0]
            else:
                imgsrc = urljoin(self.cssUrl, img).split('?')[0]

            imgname = os.path.split(imgsrc)[1]

            httpcode = None
            try:
                responseHttp = urlopen(imgsrc, timeout=3)
                httpcode = responseHttp.code
            except urllib.request.URLError as e:
                if hasattr(e, 'code'):
                    httpcode = e.code
            finally:
                if responseHttp:
                    responseHttp.close()


            if httpcode == 200:
                try:
                    urllib.request.urlretrieve(imgsrc, os.path.join(self.savePath, imgname))
                    info = u'[%2d/%2d]<a href="%s">%s</a>' % (counter, img_num, imgsrc, imgsrc)
                except:
                    errnum += 1
                    info = u'[%2d/%2d]<a href="%s">%s</a> <span style="color:red">保存失败[%s]</span>' % (
                        counter, img_num, imgsrc, imgsrc, errnum)
            else:
                errnum += 1
                info = u'[%2d/%2d]<a href="%s">%s</a> <span style="color:red">[%s][code:%s]</span>' % (
                    counter, img_num, imgsrc, imgsrc, errnum, httpcode)

            self.outInfo(info)
            counter += 1
        totalInfo = u'下载完成，总计%s ，有%s个下载失败' % (img_num, errnum)
        self.outInfo(totalInfo)

    def getImgList(self):
        css = self.getCssContent()
        html = css.decode('utf-8')  # python3
        allimglist = re.findall(r'url\s*\((.*?)\)', html)
        imgList = set(allimglist)
        return imgList

    def getCssContent(self):

        try:
            rsp = urlopen(self.cssUrl, timeout=1)
            return rsp.read()
        except Exception as e:
            self.outInfo('<font color=red>%s</font>' % e)

        except BaseException as e:
            self.outInfo('<font color=red>%s</font>' % e)


def mkdir(savePath):
    fullPath = os.path.join(os.getcwd(), savePath)
    if not os.path.exists(fullPath):
        try:
            os.mkdir(os.path.join(os.getcwd(), savePath))
            return fullPath
        except:
            print('can\'t creat dir: %s, please creat it manually! ', fullPath)
            return
    return fullPath
