main为主函数。util含有多模块共用的基本函数和全局变量。part1到3分别对应实验的三个部分。第一部分为测试被试者是否理解了题目，第二部分让被试者自己做决策，第三部分告诉被试者虚假信息：之前他选择的答案有一般是多数人的选择，一半是少数人的选择，看他是否会改变选择

src存放所有图片， res为输出的表单

config.ini里可以进行基本的配置：
- DEBUG：开关debug模式，可以设置为T或F
- IMG_PIC：图片的数量，对应着第二和第三部分题目的数量。从1开始计数，格式固定为png
- TITLE_FONT_SIZE：标题字号
- TEXT_FONT_SIZE：正文字号
- PIC_SIZE=500,170：图片大小
- TITLE_PREFIX_EMPTY_LINE_NUM：标题前的空行数
- TITLE_SUFFIX_EMPTY_LINE_NUM：标题后的空行数