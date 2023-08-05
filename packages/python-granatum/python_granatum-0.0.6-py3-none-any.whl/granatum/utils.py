from io import StringIO

from lxml.html import fromstring
import pandas as pd


def parse_authenticity_token(text):
    return fromstring(text).xpath('//input[@name="authenticity_token"]/@value')[0]


def parse_flash_alert(text):
    try:
        raise ValueError(fromstring(text).xpath('//div[@id="flash_alert"]/text()')[0])
    except IndexError:
        pass


def parse_opauth(text):
    return fromstring(text).xpath('//input[@name="opauth"]/@value')[0]


def parse_conta_ids(text):
    result = {}
    root = fromstring(text)
    for input, label in zip(
        root.xpath('//input[@name="data[Lancamento][conta_id][]"]'),
        root.xpath('//label[@name="data[Lancamento][conta_id][]"]'),
    ):
        if input.xpath('./@name')[0] != 'selectAll':
            result[label.xpath('./text()')[0]] = input.xpath('./@value')[0]
    return result


def parse_tipos(text):
    result = {}
    for label in fromstring(text).xpath(
        '//div[@id="filtro-tipo"]//div[@class="checkbox"]/label'
    ):
        result[label.xpath('./text()')[0]] = label.xpath('./input/@value')[0]
    return result


def parse_categoria_ids(text):
    result = {}
    root = fromstring(text)
    for input, label in zip(
        root.xpath('//input[@name="data[Lancamento][categoria_id][]"]'),
        root.xpath('//label[@name="data[Lancamento][categoria_id][]"]'),
    ):
        result[label.xpath('./text()')[0]] = input.xpath('./@value')[0]
    return result


def convert_csv(csv, return_type):
    '''Format a downloaded CSV file str as the desired return_type.

    Parameters
    ----------
    csv : str
        Raw file str downloaded
    return_type : str
        "list", "pandas.DataFrame", "str"
    '''
    if return_type in ('list', 'pandas.DataFrame'):
        df = pd.read_csv(StringIO(csv), sep=';', decimal=',')
        if return_type == 'list':
            df.fillna('', inplace=True)
            return df.to_dict(orient='records')
        else:
            return df
    elif return_type == 'str':
        return csv
    else:
        print('Invalid return_type "{}"; returning str'.format(return_type))
        return csv
