import struct
import os
import shutil
from fileoperate.log import ILog

logger = ILog(__file__)
from fileoperate import pdf as readPdf
from fileoperate import word as readWord

allfile = []


def file_isexist(file=None) :
    '''
    @功能 文件是否存在  \n
    @参数 file 文件全路径 \n
    @返回  True or False or Exception \n
    '''
    logger.debug('file_isexist方法执行开始')
    logger.info('传入参数:file=' + str(file))
    try :
        if os.path.isfile(file) :
            logger.info('确认文件存在')
            return True
        else :
            return False
    except Exception as e :
        logger.exception('file_isexist执行出现异常')
        return False
    finally :
        logger.debug('file_isexist方法执行结束')


def dir_isexist(dir=None) :
    '''
    @功能 文件夹是否存在  \n
    @参数 dir 文件夹全路径 \n
    @返回  True or False or Exception \n
    '''
    logger.debug('dir_isexist方法执行开始')
    logger.info('传入参数:dir=' + str(dir))
    try :
        if os.path.isdir(dir) :
            logger.info('确认文件夹存在')
            return True
        else :
            return False
    except Exception as e :
        logger.exception('dir_isexist执行出现异常')
        return False
    finally :
        logger.debug('dir_isexist方法执行结束')


def create_dir(path=None) :
    '''
    @功能 创建路径  \n
    @参数 path 路径地址 \n
    @返回  True or False or Exception \n
    '''
    logger.debug('create_dir方法执行开始')
    logger.info('传入参数:path=' + str(path))
    try :
        if not os.path.exists(path) :
            os.makedirs(path)
            logger.info('路径创建成功')
            return True
        else :
            logger.exception("路径已存在")
            return False
    except Exception as e :
        logger.exception('create_dir执行出现异常')
        raise e
    finally :
        logger.debug('create_dir方法执行结束')


def create_file(srcfile=None) :
    '''
    @功能 创建文件  \n
    @参数 path 路径地址 \n
    @参数 file 文件 \n
    @返回  True or Exception \n
    '''
    logger.debug('create_file方法执行开始')
    logger.info('传入参数:srcfile=' + str(srcfile))
    path, file = os.path.split(srcfile)
    file = ""
    try :
        if os.path.isfile(path + "\\" + file) :
            raise Exception('文件已存在，无需创建')
        else :
            if os.path.exists(path) :
                file = open(path + "\\" + file, 'w')
                logger.info('文件创建成功')
                return True
            else :
                raise Exception('创建文件时，路径创建失败')
    except Exception as e :
        logger.exception('create_file执行出现异常')
        raise e
    finally :
        if file != "" :
            file.close()
        logger.debug('create_file方法执行结束')


def copy_file(src_file=None, dst_file=None) :
    '''
    @功能 复制文件  \n
    @参数 src_file 源文件全路径 \n
    @参数 dst_file 目标文件全路径 \n
    @返回  True or Exception \n
    '''
    logger.debug('copy_file方法执行开始')

    # logger.info('传入参数:src_file='+str(src_file)+'dst_file='+ str(dst_file))
    try :
        if os.path.isfile(dst_file) :
            raise Exception('目标文件已存在')
        elif os.path.isfile(src_file) :
            logger.info('确认源文件存在，目标文件不存在')
            fpath = os.path.split(dst_file)[0]
            if os.path.exists(fpath) :
                logger.info('确认目标路径存在')
                shutil.copy(src_file, dst_file)
                logger.info('拷贝文件成功')
                return True
            else :
                logger.info('确认目标路径不存在')
                if create_dir(fpath) :
                    shutil.copy(src_file, dst_file)
                    logger.info('拷贝文件成功')
                    return True
                else :
                    raise Exception('拷贝文件时，创建目标资源路径失败')
        else :
            raise Exception('复制文件时，源文件不存在')
    except Exception as e :
        logger.exception('copy_file执行出现异常')
        raise e
    finally :
        logger.debug('copy_file方法执行结束')


def move_file(src_file=None, dst_path=None) :
    '''
    @功能 移动文件  \n
    @参数 src_file 源文件全路径 \n
    @参数 dst_path 目标文件全路径 \n
    @返回  True or Exception \n
    '''
    logger.debug('move_file方法执行开始')
    # logger.info('传入参数:src_file='+str(src_file)+'dst_file='+str(dst_file))
    try :
        if os.path.isfile(src_file) :
            if os.path.isfile(dst_path + "\\" + os.path.split(src_file)[1]) :
                raise Exception("目标文件存在，无法移动")
            else :
                shutil.move(src_file, dst_path)
                logger.info('文件移动成功')
                return True
        else :
            raise Exception("源文件不存在，无法移动")
    except Exception as e :
        logger.exception('move_file执行出现异常')
        raise e
    finally :
        logger.debug('move_file方法执行结束')


def move_folder(src_path=None, dst_path=None) :
    '''
    @功能 移动文件夹  \n
    @参数 src_path 源路径 \n
    @参数 dst_path 目标路径 \n
    @返回  True or Exception \n
    '''
    logger.debug('move_folder方法执行开始')
    logger.info('传入参数:src_path=' + str(src_path) + 'dst_path=' + str(dst_path))
    try :
        if os.path.exists(src_path) :
            shutil.move(src_path, dst_path)
            logger.info('文件夹移动成功')
            return True
        else :
            raise Exception("原路径有误")
    except Exception as e :
        logger.exception('move_folder执行出现异常')
        raise e
    finally :
        logger.debug('move_folder方法执行结束')


def del_file(file=None) :
    '''
    @功能 删除文件  \n
    @参数 file 文件全路径 \n
    @返回  True or Exception \n
    '''
    logger.debug('del_file方法执行开始')
    logger.info('传入参数:file=' + str(file))
    try :
        if os.path.isfile(file) :
            os.remove(file)
            logger.info('文件删除成功')
            return True
        else :
            raise Exception("文件不存在,无法删除")
    except Exception as e :
        logger.exception('del_file执行出现异常')
        raise e
    finally :
        logger.debug('del_file方法执行结束')


def del_dir(dir=None) :
    '''
    @功能 删除文件夹 \n
    @参数 dir 文件夹全路径 \n
    @返回  True or Exception \n
    '''
    try :
        logger.debug('del_dir方法执行开始')
        logger.info('传入参数:dir=' + str(dir))
        if os.path.isdir(dir) :
            shutil.rmtree(dir, True)
            logger.info('文件夹删除成功')
            return True
        else :
            logger.error('文件夹删除失败')
            return False
    except Exception as e :
        logger.error('有异常发生，文件夹删除失败,异常为：' + str(e))
        return False
    finally :
        logger.debug('del_dir方法执行结束')


def replaceSpecialChar(content) :
    '''
    @功能 删除输入内容中的特殊字符，主要为回车符  \n
    @参数 content 需要处理的内容，可以为list或者为字符串 \n
    @返回  返回去除特殊字符后的字符串，并在list每个元素后边添加**作为分隔 \n
    '''
    content = '**'.join(content)
    return content.replace("\r", "").replace("\n", '').replace("/r", "").replace("/n", "").replace("/'", "").strip()


def getFileContent(file=None) :
    '''
    @功能 读取文件的内容  \n
    @参数 file 文件名 \n
    @返回  读取成功返回文件内容，失败返回空字符串 \n
    '''
    try :
        fileType = filetype(file)
        fileContent = ""
        if fileType is typeList().get("255044462D312E") :
            fileContent = readPdf.parse(file)
        elif fileType in [typeList().get("D0CF11E0"),
                          typeList().get("504B0304")] :
            fileContent = readWord.parse(file)
        fileContent = replaceSpecialChar(fileContent)
        return fileContent
    except Exception as e :
        fileContent = ""
        logger.error("文件读取失败: %s " % str(file))
        logger.error(str(e))


# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少则2字符，长则8字符
def typeList() :
    '''
    @功能 得到文件类型及对应表  \n
    @返回  文件类型及其对应表 \n
    '''
    return {
        "255044462D312E" : "PDF",
        "FFD8FF" : "JPEG",
        "89504E47" : "PNG",
        "D0CF11E0" : "DOC",
        "D0CF11E0" : "XLS",
        "504B0304" : "DOCX"
    }


# 字节码转16进制字符串
def bytes2hex(bytes) :
    '''
    @功能 字节码转16进制字符串  \n
    @参数 bytes 字节码 \n
    @返回  返回16进制字符串 \n
    '''
    num = len(bytes)
    hexstr = u""
    for i in range(num) :
        t = u"%x" % bytes[i]
        if len(t) % 2 :
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# 获取文件类型
def filetype(filename) :
    '''
    @功能 获取文件的文件类型  \n
    @参数 filename 文件名 \n
    @返回  返回该文件的文件类型，如果没有匹配则返回unknown \n
    '''
    binfile = open(filename, 'rb')  # 必需二制字读取
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys() :
        fnumOfBytes = len(hcode) / 2  # 需要读多少字节
        numOfBytes = int(fnumOfBytes)
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode :
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype


def getOneLayerFile(path="") :
    '''
    @功能 得到目录下一层的文件列表  \n
    @参数 path 全路径 \n
    @返回  文件列表 \n
    '''
    allFile = []
    try :
        if os.path.isdir(path) :
            fileList = os.listdir(path)
            for file in fileList :
                if os.path.isfile(file) :
                    filepath = os.path.join(path, file)
                    allFile.append(filepath)
        else :
            logger.error("源文件夹不存在，无法得到文件列表")
    except Exception as e :
        logger.error('getallfile执行出现异常')
        raise e
    finally :
        logger.debug('getallfile方法执行结束')
        return allFile


def getallfile(path="") :
    '''
    @功能 得到目录下的文件列表，不包含文件夹  \n
    @参数 path 全路径 \n
    @返回  文件列表 \n
    '''
    allFile = []
    try :
        if os.path.isdir(path) :
            fileList = os.listdir(path)
            for file in fileList :
                filepath = os.path.join(path, file)
                # 判断是不是文件夹
                if os.path.isdir(filepath) :
                    getallfile(filepath)
                allFile.append(filepath)
        else :
            logger.error("源文件夹不存在，无法得到文件列表")
    except Exception as e :
        logger.error('getallfile执行出现异常')
        raise e
    finally :
        logger.debug('getallfile方法执行结束')
        return allFile


def getallDirectories(path="") :
    '''
    @功能 得到目录下的文件夹列表，深度只有一层  \n
    @参数 path 全路径 \n
    @返回  文件列表 \n
    '''
    directoryList = []
    try :
        if os.path.isdir(path) :
            dl = os.listdir(path)
            for directory in dl :
                filepath = path + '/' + directory
                # filepath = os.path.join(path, directory)
                # 判断是不是文件夹
                if os.path.isdir(filepath) :
                    directoryList.append(filepath)
        else :
            logger.error("源文件夹不存在，无法得到文件列表")
    except Exception as e :
        logger.error('getallDirectories执行出现异常')
    finally :
        logger.debug('getallDirectories方法执行结束')
        return directoryList
