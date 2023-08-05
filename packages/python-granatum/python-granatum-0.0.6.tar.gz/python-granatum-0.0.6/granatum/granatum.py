from time import time

from dateutil.relativedelta import relativedelta
from lxml.html import fromstring
from requests import Session

from granatum import utils


class Granatum(object):
    '''Use for accessing Granatum.'''

    def __init__(self):
        self.session = Session()
        self.filter_options = {}

    def login(self, email, password):
        '''Execute login workflow.

        Parameters
        ----------
        email : str
            E-mail
        password : str
            Senha
        '''
        response_1 = self.session.get('https://contas.granatum.com.br/')
        response_2 = self.session.post(
            'https://contas.granatum.com.br/users/sign_in',
            data={
                'authenticity_token': utils.parse_authenticity_token(response_1.text),
                'commit': 'Acessar',
                'user[email]': email,
                'user[password]': password,
                'utf8': '✓',
            },
        )
        utils.parse_flash_alert(response_2.text)
        self.session.get('https://contas.granatum.com.br/')
        self.session.get('https://secure.granatum.com.br/oauth/granatum')
        response_3 = self.session.get(
            'https://contas.granatum.com.br/oauth/authorize?client_id=b9e18dcd8bfab8e34fe98f36d8fc8d68637b983bcb63f1bb1f06c1dbd829c276&redirect_uri=https%3A%2F%2Fsecure.granatum.com.br%2Foauth%2Fgranatum%2Fint_callback&scope=public&response_type=code'
        )
        self.session.post(
            'https://secure.granatum.com.br/oauth/callback',
            data={'opauth': utils.parse_opauth(response_3.text)},
        )

    def attr_filter_options(self):
        '''Attribute the available options for data filters.'''
        response = self.session.get(
            'https://secure.granatum.com.br/a/59361/admin/lancamentos'
        )
        self.filter_options = {
            'conta_id': utils.parse_conta_ids(response.text),
            'tipo': utils.parse_tipos(response.text),
            'categoria_id': utils.parse_categoria_ids(response.text),
        }

    def exportar(self, end_date, start_date, filters={}, return_type='list'):
        '''Download the file downloaded after clicking "Exportar" in the "LANCAMENTOS"
        tab.

        Parameters
        ----------
        end_date : date
            "De"
        start_date : date
            "Ate"
        filters : optional, dict of lists
            "conta_id", "tipo", "categoria_id"; default blank dict
        return_type : optional, str
            "list", "pandas.DataFrame", "str"; default "list"

        Return
        ------
        return_type
            Representation of the exported CSV data in a specified format
        '''
        if not bool(self.filter_options):
            self.attr_filter_options()
        self._post_filter(self._build_form(end_date, start_date, filters))
        self._get_carrega_balanco()
        self._post_ajax()
        response = self.session.get(
            'https://secure.granatum.com.br/a/59361/admin/lancamentos/exportar_lancamentos'
        )
        return utils.convert_csv(
            response.content.decode('latin-1'), return_type
        )

    def _build_form(self, end_date, start_date, filters):
        '''Construct the form data used to filter site results.

        Parameters
        ----------
        end_date : date
            "De"
        start_date : date
            "Ate"
        filters : optional, dict of lists
            Supported keys are "conta_id", "tipo", "categoria_id"

        Return
        ------
        list of tuples
        '''
        data = [
            ('_method', 'POST'),
            ('data[Lancamento][regime]', '1'),
            ('data[Lancamento][atalhoCalendario]', 'diario'),
            ('data[Lancamento][startDate]', start_date.strftime('%d/%m/%Y')),
            ('data[Lancamento][endDate]', end_date.strftime('%d/%m/%Y')),
            ('data[Lancamento][conta_id]', ''),
            ('data[Lancamento][centro_custo_lucro_id]', ''),
            ('data[Lancamento][busca]', ''),
            ('data[Lancamento][tipo]', ''),
            ('data[Lancamento][categoria_id]', ''),
            ('data[Lancamento][forma_pagamento_id]', ''),
            ('data[Lancamento][tipo_custo_nivel_producao_id]', ''),
            ('data[Lancamento][tipo_custo_apropriacao_produto_id]', ''),
            ('data[Lancamento][tipo_documento_id]', ''),
            ('data[Lancamento][cliente_id]', ''),
            ('data[Lancamento][fornecedor_id]', ''),
            ('data[Lancamento][tag_id]', ''),
            ('data[Lancamento][wgi_usuario_id]', ''),
        ]
        for key, values in filters.items():
            for value in values:
                data.append(
                    (
                        'data[Lancamento][{}][]'.format(key),
                        self.filter_options[key][value],
                    )
                )
        return data

    def _post_filter(self, data):
        '''Filter the result set on the website.

        Parameters
        ----------
        data : dict
            Form data
        '''
        self.session.post(
            'https://secure.granatum.com.br/a/59361/admin/filtros/filtrar/filter_name:Lancamentos/',
            data=data,
        )

    def _get_carrega_balanco(self):
        '''Send a necessary server request.'''
        self.session.get(
            'https://secure.granatum.com.br/a/59361/admin/contas/carrega_balanco',
            data={'_': int(time() * 1000.0)},
        )

    def _post_ajax(self):
        '''Send a necessary server request.'''
        self.session.post(
            'https://secure.granatum.com.br/a/59361/admin/lancamentos/index/page:1?ajax'
        )
