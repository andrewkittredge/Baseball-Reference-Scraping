#! /usr/bin/python

import urllib
from BeautifulSoup import BeautifulSoup
import re

STANDARD_BATTING_COLUMNS=(
'Year',
'Age',
'Team',
'League',
'Games Played or Pitched',
'Plate Appearances',
'At Bats',
'Runs Scored/Allowed',
'Hits/Hits Allowed',
'2B',
'3B',
'HR',
'RBI',
'SB',
'CS',
'BB',
'SO',
'BA',
'OBP',
'SLG',
'OPS',
'OPX+',
'TB',
'GDP',
'HBP',
'SH',
'IBB',
'Pos',
'Awards'
)


def url_to_beautiful_soup(url): 
    url = urllib.urlopen(url)
    soup = BeautifulSoup(''.join(url.readlines()))
    return soup

def link_to_url(domain, link_element):
    href = filter(lambda attr: attr[0] == 'href', link_element.attrs)[0][1]
    return ''.join(('http://', domain, href))

def find_batting_standard_table(soup):
    for table in soup.findAll('table'):
        try:
            if table['id'] == 'batting_standard':
                return table
        except KeyError:
            '''table does not have an "id" attribute, oh-well, the 
            table we're looking for does'''
            pass
    raise Expection('Did not find "batting_standard" table in %s' % soup)

batting_standard_re = 'batting_standard\.((18|19|20)[0-9]{2})'

def decompose_batting_table(batting_table_soup):
    '''Takes the soup of batting statistics table

    '''

    batting_table_body = batting_table_soup.findAll('tbody')[0]
    for table_row in batting_table_body.findAll('tr'):
        table_row_id = table_row.get('id')
        if not table_row_id:
            continue
        year = re.findall(batting_standard_re, table_row_id)
        row_values = {}
        my_keys_with_values = zip(STANDARD_BATTING_COLUMNS, 
                                table_row.findAll('td')
                                  )

        for key, element in my_keys_with_values:
            value = element.text
            row_values[key] = value
            
        yield row_values
