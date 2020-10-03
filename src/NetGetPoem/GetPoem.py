# coding=utf-8
import urllib.request as ure
import urllib.parse as upa
import re
import bs4
import sys
import traceback
from src import *


def cutName(htmlContent: str) -> [bool, list]:
    """仅当诗歌名发生错误时会被调用，返回正确诗歌名和对应网址的序列"""
    bs = bs4.BeautifulSoup(htmlContent, 'lxml' if IF_BS4_PARSER[0] else None)
    poemList = bs.find(id='data-container')
    result = []
    for poemContainer in poemList.find_all_next(attrs={'class': "poem-list-item"}):
        poemContainer: bs4.PageElement
        poemCorrectName = re.sub(r'[\r\n ]+', ' ', poemContainer.text).split('[')[0].strip(' ')
        detailUrl = HANYU_URL + poemContainer.find_next('a', attrs={'class': "check-red"})['href']
        if 'zici' not in detailUrl:  # 排除字词选项（只要诗歌）
            result.append((poemCorrectName, detailUrl))
    return result


def cutPoemMessage(htmlContent: str):
    """获取诗歌信息"""
    main = bs4.BeautifulSoup(htmlContent, 'lxml' if IF_BS4_PARSER[0] else None)
    message = main.find(id="body-wrapper").find_next(id="poem-detail-header")  # 寻找诗的信息
    poemHeadMessage = list(filter(lambda a: bool(a),
                                  re.sub(r'[\r\n ]+', '\n', message.find_next(name='div').text).split('\n')
                                  ))
    poemName = message.find_next(name="h1").next_element
    author = poemHeadMessage[0][4:]
    dynasty = poemHeadMessage[1][4:]
    return poemName, author, dynasty


def cutPoemContent(htmlContent: str) -> tuple:
    """获取现代诗歌基本信息，返回诗歌名，作者名，朝代，和诗歌内容"""
    bs = bs4.BeautifulSoup(htmlContent, 'lxml' if IF_BS4_PARSER[0] else None)
    poemContainer_All = bs.find(id="body-wrapper").find_next(id="poem-detail-header") \
        .find_next(attrs={'class': 'poem-detail-item-content'})
    poemContent = ''
    for poemContainer in poemContainer_All.find_all_next(
            attrs={'id': 'body_p'} if checkTranslation(htmlContent) else {
                'class': "poem-detail-main-text"}):  # 翻译与没翻译的两种情况
        poemContent += re.sub(r'\s+', '', poemContainer.text)
    poemName, author, dynasty = cutPoemMessage(htmlContent)
    return poemName, author, dynasty, poemContent


def checkTranslation(htmlContent: str):
    """检查是否有翻译"""
    if 'means_p' in htmlContent:
        return True


def checkGroup(htmlContent: str):
    """判断返回的是否为诗歌组"""
    return 'poem-list' in htmlContent


def checkEmpty(htmlContent: str):
    """判断搜索结果是否为空"""
    return 'empty-tips' in htmlContent


def checkRight(htmlContent: str):
    """判断返回的是否是诗歌的内容"""
    return not checkGroup(htmlContent) and not checkEmpty(htmlContent)


def getPoemMessageByUrl(url: str) -> [bool, list]:
    """
    第一个返回值为是否正确接收到诗歌内容
    如果为1：
        第二个返回值为诗歌的基本信息，排序为【诗名，作者，朝代，内容】
    如果为2：
        第二个返回值为建议的正确诗名列表
    如果为3：
        第二个返回值为错误详细信息
    """
    headers = {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50'}
    req = ure.Request(url=url, headers=headers)
    response = ure.urlopen(req)
    get = response.read().decode() # TODO 测试完修改回来

    # get = open('WrongExample.html', 'rb').read().decode()
    # get = open('Example(诗名纠正).html', 'rb').read().decode()

    #get = open(r'D:\Program_Projects\Python_Projects\TestPoem\src\NetGetPoem\Example(无译文古代).html', 'rb').read().decode()
    # get = open('Example(有译文古代).html', 'rb').read().decode()
    # get = open('Example(无译文现代).html', 'rb').read().decode()
    # get = open('Example(有译文现代).html', 'rb').read().decode()

    try:
        if checkEmpty(get):
            return 3, 'Searching no result'
        elif checkRight(get):  # 判断诗名是否正确
            message = cutPoemContent(get)
            return 1, message
        elif checkGroup(get):
            message = cutName(get)  # 寻找建议尝试
            return 2, message  # 诗名建议和错误情况
        else:
            raise FileNotFoundError('找不到对应的html结构或诗歌内容！')
    except Exception:
        traceback.print_exc(file=sys.stderr)
        return 3, ''.join(traceback.format_exception(*sys.exc_info()))


def getPoemMessageByName(name: str) -> [bool, list]:
    return getPoemMessageByUrl(f'{HANYU_URL}/s?wd={upa.quote(name)}')


if __name__ == '__main__':
    # print(getPoemMessageByName('行路难'))
    print(getPoemMessageByUrl('https://hanyu.baidu.com/shici/detail?pid=04017624111a4e64bc34633748059cdd'))
