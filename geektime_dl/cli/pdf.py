import pdfkit
import os
from ..geektime_ebook import maker
from PyPDF2 import PdfFileMerger


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
    source_dir = os.path.join(output_dir, '简介.html')
    dest_dir = os.path.join(output_dir, '简介.pdf')
    pdfkit.from_file(source_dir, dest_dir, cover=cover, options=options)

    for article in articles:
        title = maker.format_file_name(article['article_title'])
        source_dir = os.path.join(output_dir, '{}.html'.format(title))
        dest_dir = os.path.join(output_dir, '{}.pdf'.format(title))
        pdfkit.from_file(source_dir, dest_dir, options=options)

    merge_pdf(output_dir, articles, file_name)


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


def merge_pdf(output_dir, articles, file_name):
    """
    合并pdf
    :param output_dir:
    :param articles:
    :param file_name:
    :return:
    """
    merger = PdfFileMerger()
    merger.append(open(os.path.join(output_dir, '简介.pdf'), 'rb'), import_bookmarks=False)
    for article in articles:
        title = maker.format_file_name(article['article_title'])
        pdf_dir = os.path.join(output_dir, '{}.pdf'.format(title))
        print('append ' + pdf_dir)
        merger.append(open(pdf_dir, 'rb'), import_bookmarks=False)
        # merger.append(PdfFileReader(file('test.pdf', 'rb')), import_bookmarks=False)
    merge_dir = os.path.join(output_dir, "../{}.pdf".format(file_name))
    print('merge pdf dir: ' + merge_dir)
    with open(merge_dir, "wb") as f:
        merger.write(f)
    merger.close()
    print('merge pdf file success...')


# if __name__ == '__main__':
    # render_pdf()

