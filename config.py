import os


SECRET_KEY = 'you-guess'

# 个人站点配置信息
# 站点标题
SITE_TITLE = '密斯想 个人博客'
# 站点副标题
SITE_SUBTITLE = '2333333333333333'

# 放置 md 文件夹
# 文章 md 文件夹
POST_PATH = './source/_posts/'
# 页面 md 文件夹
PAGE_PATH = './source/_pages/'
# 输出 html 文件夹
GENERATED_PATH = './quiet/static/generated/'
# 默认分类
DEFAULT_CATEGORY = '未分类'
# 默认标签
DEFAULT_TAG = ['其他']

# 存放 shelve 数据文件
BLOG_DAT = './quiet/static/generated/data.dat'

# 管理员信息,建议配置环境变量
# 登录名，密码
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME') or 'quiet'
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD') or 'password'

