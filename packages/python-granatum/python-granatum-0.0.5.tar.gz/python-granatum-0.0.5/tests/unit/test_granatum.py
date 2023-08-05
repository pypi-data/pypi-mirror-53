from datetime import date
import unittest
from unittest.mock import Mock

from granatum.granatum import Granatum


class TestBuildForm(unittest.TestCase):
    '''Test the Granatum._build_form method with varied inputs.'''

    end_date = date(2019, 8, 31)
    start_date = date(2019, 8, 1)
    granatum = Granatum()
    granatum.filter_options = {
        'conta_id': {'conta_id_1': '1', 'conta_id_2': '2'},
        'tipo': {'tipo_1': '1'},
        'categoria_id': {'categoria_id_1': '1'},
    }

    def setUp(self):
        self.expected = [
            ('_method', 'POST'),
            ('data[Lancamento][regime]', '1'),
            ('data[Lancamento][atalhoCalendario]', 'diario'),
            ('data[Lancamento][startDate]', '01/08/2019'),
            ('data[Lancamento][endDate]', '31/08/2019'),
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

    def test_no_filters(self):
        result = self.granatum._build_form(self.end_date, self.start_date, {})

        self.assertEqual(self.expected, result)

    def test_one_conta_id(self):
        self.expected.append(('data[Lancamento][conta_id][]', '1'))

        result = self.granatum._build_form(
            self.end_date, self.start_date, {'conta_id': ['conta_id_1']}
        )

        self.expected.sort()
        result.sort()
        self.assertEqual(self.expected, result)

    def test_two_conta_ids(self):
        self.expected.append(('data[Lancamento][conta_id][]', '1'))
        self.expected.append(('data[Lancamento][conta_id][]', '2'))

        result = self.granatum._build_form(
            self.end_date,
            self.start_date,
            {'conta_id': ['conta_id_1', 'conta_id_2']}
        )

        self.expected.sort()
        result.sort()
        self.assertEqual(self.expected, result)

    def test_conta_id_and_tipo_and_categoria_id(self):
        self.expected.append(('data[Lancamento][conta_id][]', '1'))
        self.expected.append(('data[Lancamento][tipo][]', '1'))
        self.expected.append(('data[Lancamento][categoria_id][]', '1'))

        result = self.granatum._build_form(
            self.end_date,
            self.start_date,
            {
                'conta_id': ['conta_id_1'],
                'tipo': ['tipo_1'],
                'categoria_id': ['categoria_id_1'],
            },
        )

        self.expected.sort()
        result.sort()
        self.assertEqual(self.expected, result)


if __name__ == '__main__':
    unittest.main()
