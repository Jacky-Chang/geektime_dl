import pdfkit
import os
from ..geektime_ebook import maker


cover_string = '<!DOCTYPE html>\n\
<html lang="en">\n\
<head>\n\
    <meta charset="UTF-8">\n\
    <title>Title</title>\n\
</head>\n\
<body>\n\
<p><img style="width:100%;height:auto;" src="cover.jpg" /></p>\n\
</body>\n\
</html>\n'


def render_pdf(output_dir, articles, file_name):
    """
    生成pdf
    :param output_dir:
    :param articles:
    :param file_name:
    :return:
    """
    options = {
        'quiet': '',
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'outline-depth': 10,
    }
    cover = render_cover(output_dir)
    # 简介页面
    source_list = list()
    source_dir = os.path.join(output_dir, '简介.html')
    source_list.append(source_dir)

    for article in articles:
        title = maker.format_file_name(article['article_title'])
        source_dir = os.path.join(output_dir, '{}.html'.format(title))
        source_list.append(source_dir)
    pdfkit.from_file(source_list, os.path.join(output_dir, '../{}.pdf'.format(file_name)),
                     cover=cover, options=options)
    print('生成 {}.pdf done'.format(file_name))


def render_cover(output_dir):
    """
    生成封面
    :param output_dir:
    :return:
    """
    if os.path.isfile(os.path.join(output_dir, 'cover.jpg')):
        with open(os.path.join(output_dir, 'cover.html'), 'w') as f:
            f.writelines(cover_string)
        return os.path.join(output_dir, 'cover.html')
    return None
