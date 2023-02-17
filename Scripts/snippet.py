import glob
from pdf2image import convert_from_path
import os

ls = glob.glob('/media/ksmt0/HD-ADU3/book-viewer/static/pdfs/h/*.pdf')

def rename_filename():
    for i, l in enumerate(ls):
        base_path, pdf_path = l.split('/pdfs/')
        filename = pdf_path.split('.pdf.pdf')[0].split('.pdf')[0]
        filename_ = filename.replace(' ', '_')
        os.rename(
            l,
            f'{base_path}/pdfs/{filename_}.pdf'
        )
    
def get_pdf_path():
    logstr = ''
    for l in ls:
        s = l.split('pdfs/')[-1][:-4]
        logstr += f'''<a href="/static/pdfs/{s}.pdf" target="_blank"><img src="/static/thumbnails/{s}.jpeg" class="img-fluid img-thumbnail img-responsive mx-auto d-block w-50"></a>
'''       
    with open('Scripts/tmp_data/filenames.txt', mode='w') as f:
        f.write(logstr)
        
        
def pdf_to_image():
    print(len(ls))
    
    for i, l in enumerate(ls):
        s = l.split('/')[-1][:-4]
        base_path, pdf_path = l.split('/pdfs/')
        filename = pdf_path.split('.pdf')[0]
        print(i, f'{base_path}/pdfs/{filename}.pdf')
        pages = convert_from_path(
            f'{base_path}/pdfs/{filename}.pdf', dpi=40)
        pages[0].save(f'{base_path}/thumbnails/{filename}.jpeg', "JPEG")
        del s, base_path, pdf_path, filename, pages
        
# rename_filename()
# pdf_to_image()
get_pdf_path()