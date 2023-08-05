from astropy.units import cgs
import webbrowser
import ads
from typing import Union
from warnings import warn

ads_link = 'https://ui.adsabs.harvard.edu/abs/{bibcode}/'
ext_link = 'https://ui.adsabs.harvard.edu/link_gateway/{bibcode}/'


class Reference:
    def __init__(self, bibcode: Union[bytes, str]):
        try:
            self.bibcode = bibcode.decode()
        except AttributeError:
            self.bibcode = bibcode

        try:
            self.article = \
                [paper for paper in ads.SearchQuery(bibcode=self.bibcode, fl=['id', 'title','pubdate', 'abstract', 'author'])][0]
        except:
            warn(f"Can't find reference on ADS for {self.bibcode}",UserWarning)
            return

        self.title = self.article.title[0]
        self.authors = self.article.author
        self.pubdate = self.article.pubdate
        self.abstract = self.article.abstract
        self.link = ads_link.format(bibcode=self.bibcode)
        self.ext_link = ext_link.format(bibcode=self.bibcode)

    def get_citation(self, index: int):
        try:
            return Reference(self.article.citation[index])
        except IndexError:
            return None

    def get_reference(self, index: int):
        try:
            return Reference(self.article.citation[index])
        except IndexError:
            return None

    def show(self):
        if self.link is not None:
            webbrowser.open(self.link + "abstract", new=2)

    def arxiv(self):
        if self.link is not None:
            webbrowser.open(self.ext_link + "EPRINT_PDF", new=2)

    def publisher(self):
        if self.link is not None:
            webbrowser.open(self.ext_link + "PUB_PDF", new=2)

    def __repr__(self):
        return self.title