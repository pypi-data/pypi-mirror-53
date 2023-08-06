# NaivePDF 
*yet another pdf texts and tables extractor*

This project is inspired by [pdfminer](https://github.com/euske/pdfminer), 
and the pdf parts use, rewrite or redesign a lots of it's codes.

The main purpose of this project is to provide a tool 
that can naively extract text lines and **bordered tables** from pdf files, 
and write them into a html file. 
In most cases it works well.

On the other hand, it's pdf parts can be an alternative of pdfminer
that you can use it to extract texts, lines and shapes more simply.


# How to Install
* Python3.6+ required

```cmd
pip install naivepdf
```

# Example of Use

very simple to use

```python
# encoding: utf-8

from naivepdf.pdfdocument import PDFDocument
from naivepdf.reconstructor import PageReconstructor
from naivepdf.utils.html import html


def main():
    with open('examples/1206061047.pdf', 'rb') as fp:
        data = []
        doc = PDFDocument(fp)
        for i, page in enumerate(doc.pages):
            # as an alternative of pdfminer, just:
            # data.append(page.data)
            reconstructor = PageReconstructor(page)
            data.extend(reconstructor.reconstruct())

    # as an alternative of pdfminer, just:
    # return data
    with open('examples/1206061047.html', 'w', encoding='utf-8') as fp:
        html(fp, data)


if __name__ == '__main__':
    main()

```
