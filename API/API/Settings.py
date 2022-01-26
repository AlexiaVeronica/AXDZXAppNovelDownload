from function.instance import *


def setup_config():
    Vars.cfg.load()
    config_change = False
    if type(Vars.cfg.data.get('save_book')) is not str or Vars.cfg.data.get('save_book') == "":
        Vars.cfg.data['save_book'] = 'novel'
        config_change = True
    if type(Vars.cfg.data.get('config_book')) is not str or Vars.cfg.data.get('config_book') == "":
        Vars.cfg.data['config_book'] = 'config'
        config_change = True
    if type(Vars.cfg.data.get('Pool')) is not int or Vars.cfg.data.get('ThVars.cfg.data_Pool') == "":
        Vars.cfg.data['Pool'] = 12
        config_change = True
    if type(Vars.cfg.data.get('agreed_to_Vars.cfg.datame')) is not str or Vars.cfg.data.get('agreed_to_Vars.cfg.datame') == "":
        Vars.cfg.data['agreed_to_Vars.cfg.datame'] = 'No'
        config_change = True
    if type(Vars.cfg.data.get('agree_terms')) is not str or Vars.cfg.data.get('agree_terms') == "":
        Vars.cfg.data['agree_terms'] = '是否以仔细阅读且同意LICENSE中叙述免责声明\n如果同意声明，请输入英文 \"yes\" 或者中文 \"同意\" 后按Enter建，如果不同意请关闭此程式'
        config_change = True
    if type(Vars.cfg.data.get('show_book_info')) is not str or Vars.cfg.data.get('show_book_info') == "":
        Vars.cfg.data['show_book_info'] = '书名:{}\n作者:{}\n状态:{}\n字数:{}\n更新:{}\n标签:{}\n最后更新章节:{}\n简介信息\n{}'
        config_change = True
    if type(Vars.cfg.data.get('help')) is not str or Vars.cfg.data.get('help') == "":
        Vars.cfg.data['help'] = 'https://m.aixdzs.com/\nd | bookid\t\t\t\t\t———输入书籍序号下载单本小说\nt | tagid\t\t\t\t\t———输入分类号批量下载分类小说\n' + \
            'n | bookname\t\t\t\t\t———下载单本小说\nh | help\t\t\t\t\t———获取使用程序帮助\nq | quit\t\t\t\t\t———退出运行的程序\n' + \
            'm | method\t\t\t\t\t———切换多线程和多进程\np | pool\t\t\t\t\t———改变线程数目\nu | updata\t\t\t\t\t———下载指定文本中的bookid'
        config_change = True
    if type(Vars.cfg.data.get('tag')) is not dict or Vars.cfg.data.get('tag') == "":
        Vars.cfg.data['tag'] = {1: '玄幻', 2: '奇幻', 3: '武侠', 4: '仙侠', 5: '都市', 6: '职场', 7: '历史',
                       8: '军事', 9: '游戏', 10: '竞技', 11: '科幻', 12: '灵异', 13: '同人', 14: '轻小说'}
        config_change = True
    if type(Vars.cfg.data.get('USER_AGENT_LIST')) is not list or Vars.cfg.data.get('USER_AGENT_LIST') == "":
        Vars.cfg.data['USER_AGENT_LIST'] = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        config_change = True


    if config_change:
        Vars.cfg.save()
        
setup_config()
