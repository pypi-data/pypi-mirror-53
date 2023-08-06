# coding=utf-8
import win32com,os
from win32com.client import Dispatch,DispatchEx


def fileTypeCheck(fPath):
    '''
    @功能 检查该文件是不是docx/doc/wps/txt文件的其中一种 \n
    @参数 fpath 文件名 \n
    @返回 如果是docx/doc/wps/txt的一种，返回True，否则返回False \n
    '''
    fileTypes = ["docx","doc","wps","txt"]
    fileType = str(os.path.split(fPath)[1]).split(".")[-1]
    if fileType not in fileTypes:
        return False
    else:
        return True

def parse(path):
    '''
    @功能 获取docx/doc/wps/txt文件的文件内容 \n
    @参数 path 文件名 \n
    @返回  返回该文件的文件内容，内容以list形式存在，每一行为list的一个元素 \n
    '''
    if fileTypeCheck(path) is not True:
        raise Exception("不支持的文档格式")
    try:
        openResult = []
        word = Dispatch('Word.Application')  # 打开word应用程序
        # word = DispatchEx('Word.Application') #启动独立的进程
        word.Visible = 0  # 后台运行,不显示
        word.DisplayAlerts = 0  # 不警告
        doc = word.Documents.Open(FileName=path, Encoding='utf-8')
        for para in doc.paragraphs:
            openResult.append(str(para.Range.text).replace("\r\x07", ""))
        return openResult
    except Exception as e:
        raise e
    finally:
        doc.Close()  # 关闭word文档
        word.Quit  # 关闭word程序
#parse(r"F:\普华\机器人\冀北信通分公司机器人\数据样例\归档文件实例\2014_177_国网冀北电力_8EBCNZM14078_正版化软件购置\1_国网冀北电力_正版化软件购置_可行性研究报告.doc")
