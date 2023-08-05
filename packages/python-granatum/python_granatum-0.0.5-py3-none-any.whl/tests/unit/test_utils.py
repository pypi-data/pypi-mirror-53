import os
import unittest

from lxml.html import fromstring
import pandas as pd

from granatum import utils

FIXTURES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir, 'fixtures'
)


class TestParse(unittest.TestCase):
    '''Test functions for parsing Granatum web pages.'''

    def test_parse_authenticity_token(self):
        expected = 'ZgqJCFG+frhVEVkRDlLRftbB+GKqELZ+vy27nPgwSX0='
        with open(
            os.path.join(FIXTURES_PATH, 'contas.html'), 'r', encoding='utf-8'
        ) as file:
            text = file.read()

        result = utils.parse_authenticity_token(text)

        self.assertEqual(expected, result)

    def test_parse_flash_alert_invalid_email_or_password(self):
        expected = 'Email ou senha inválidos.'
        with open(
            os.path.join(FIXTURES_PATH, 'sign_in_flash_alert.html'),
            'r',
            encoding='utf-8',
        ) as file:
            text = file.read()

        try:
            utils.parse_flash_alert(text)
            self.assertFail()
        except ValueError as result:

            self.assertEqual(expected, str(result))

    def test_parse_flash_alert_none(self):
        with open(
            os.path.join(FIXTURES_PATH, 'oauth.html'), 'r', encoding='utf-8'
        ) as file:
            text = file.read()

        result = utils.parse_flash_alert(text)

        self.assertIsNone(result)

    def test_parse_opauth(self):
        expected = 'YTozOntzOjQ6ImF1dGgiO2E6Mzp7czoxMToiY3JlZGVudGlhbHMiO2E6NDp7czoxMjoiYWNjZXNzX3Rva2VuIjtzOjY0OiJmYjFlYzM3NzQ1NzI1MjE3NjY4NGEyMmE3NDVhZmNmOWUwNTc5Zjg0ZjExYmQyYWQwZjJlOGQyZjNjY2VkMDAwIjtzOjEwOiJ0b2tlbl90eXBlIjtzOjY6ImJlYXJlciI7czoxMzoicmVmcmVzaF90b2tlbiI7czo2NDoiOWYyODMzMjk1ODUyOTc5NzQzZDZmOGFhNzUwYzY2MGY2Zjc5MDQ5YTNhZDVmZTNkOTMwMGQ1YzcyMzJmYjMzYSI7czo1OiJzY29wZSI7czo2OiJwdWJsaWMiO31zOjQ6InVzZXIiO2E6MTA6e3M6MjoiaWQiO2k6NzE4NjI7czoxMzoiZmluYW5jZWlyb19pZCI7aTo3MTg2MjtzOjM6Il9pZCI7czoyNDoiNWFhMTQwNjk2OTcwMmQyZGUyOWNhODE5IjtzOjQ6Im5hbWUiO3M6NjoiRHVzdGluIjtzOjU6ImVtYWlsIjtzOjIyOiJkdXN0aW4uZ2xhc3NAZ21haWwuY29tIjtzOjEzOiJzaWduX2luX2NvdW50IjtpOjE4MTtzOjEzOiJwYXJ0bmVyX3Rva2VuIjtzOjA6IiI7czoxMDoiY3JlYXRlZF9hdCI7czoyNDoiMjAxOC0wMy0wOFQxMzo1Mzo0NS4wMzFaIjtzOjE1OiJjdXJyZW50X2FjY291bnQiO2E6Mjg6e3M6MjoiaWQiO2k6NTkzNjE7czoxMzoiZmluYW5jZWlyb19pZCI7aTo1OTM2MTtzOjM6Il9pZCI7czoyNDoiNTcwZDNiZDI2OTcwMmQ2ODNkMzUxZjAzIjtzOjEwOiJsZWdhbF9uYW1lIjtzOjYzOiJDZW50cm8gRXNww61yaXRhIEJlbmVmaWNlbnRlIFVuacOjbyBkbyBWZWdldGFsIC0gTsO6Y2xlbyBHYXNwYXIiO3M6MTA6InRyYWRlX25hbWUiO3M6MTQ6Ik7DmkNMRU8gR0FTUEFSIjtzOjg6ImRvY3VtZW50IjtzOjE0OiIzMzQ4NTYxNjAwMDE1OSI7czoyOiJpbSI7czowOiIiO3M6NToicGhvbmUiO3M6MTU6Iig2MSkgOTkyODYtNzAwMyI7czo5OiJzZWN0b3JfaWQiO2k6MztzOjg6InN0YXRlX2lkIjtpOjc7czoxMToiYnVzaW5lc3NfaWQiO2k6MDtzOjc6ImNpdHlfaWQiO2k6MTtzOjc6ImFkZHJlc3MiO3M6NDY6IsOBcmVhIElzb2xhZGEgbsK6IDQsIEZhemVuZGEgRW5nZW5obyBRdWVpbWFuZG8iO3M6MTQ6ImFkZHJlc3NfbnVtYmVyIjtzOjE6IjQiO3M6MTg6ImFkZHJlc3NfY29tcGxlbWVudCI7czowOiIiO3M6ODoiZGlzdHJpY3QiO3M6MTE6IkJyYXpsw6JuZGlhIjtzOjg6InppcF9jb2RlIjtzOjA6IiI7czo5OiJpc19hY3RpdmUiO2k6MTtzOjE1OiJpc19maXJzdF9hY2Nlc3MiO2k6MDtzOjEwOiJpc19jb21wYW55IjtpOjE7czoxMDoiZXhwaXJhdGlvbiI7czoxMDoiMjAxNi0wNC0xOSI7czoxNjoiaXVndV9jdXN0b21lcl9pZCI7czozMjoiOTRCOEFBODBEQjk4NDQxOEJEMUI5Mzg0NzJCRTc4RDkiO3M6MzA6ImFkZGl0aW9uYWxfZGF5c19mb3JfZXhwaXJhdGlvbiI7aTowO3M6MTA6ImNyZWF0ZWRfYXQiO3M6MjQ6IjIwMTYtMDQtMTJUMTg6MTg6NDguMTg4WiI7czoxOToibnVtYmVyX29mX2VtcGxveWVlcyI7aToxO3M6NDoibG9nbyI7czoxMzU6Imh0dHBzOi8vczMtc2EtZWFzdC0xLmFtYXpvbmF3cy5jb20vZ3JhbmF0dW0vcHJvZHVjdGlvbi91cGxvYWRzL2FjY291bnQvbG9nby81NzBkM2JkMjY5NzAyZDY4M2QzNTFmMDMvc21hbGxfTG9nb19HYXNwYXJfMzBfQW5vc19KcGVnLmpwZyI7czoxNDoiaXNfc3VwZXJfYWRtaW4iO2k6MDtzOjEzOiJzdWJzY3JpcHRpb25zIjthOjE6e2k6MDthOjc6e3M6MzoiX2lkIjtzOjI0OiI1NzBkM2MwODY5NzAyZDY4M2Q3ZjFmMDMiO3M6MTA6ImFjY291bnRfaWQiO3M6MjQ6IjU3MGQzYmQyNjk3MDJkNjgzZDM1MWYwMyI7czoxMDoiZXhwaXJhdGlvbiI7czoxMDoiMjAyMC0wMS0yNSI7czo4OiJpbl90cmlhbCI7aTowO3M6MTU6InNob3dfb25ib2FyZGluZyI7aTowO3M6MzA6ImFkZGl0aW9uYWxfZGF5c19mb3JfZXhwaXJhdGlvbiI7aTowO3M6MTE6ImFwcGxpY2F0aW9uIjthOjE6e3M6MzoidWlkIjtzOjY0OiJiOWUxOGRjZDhiZmFiOGUzNGZlOThmMzZkOGZjOGQ2ODYzN2I5ODNiY2I2M2YxYmIxZjA2YzFkYmQ4MjljMjc2Ijt9fX19czo1OiJyb2xlcyI7YToxOntpOjA7YTo1OntzOjM6Il9pZCI7czoyNDoiNWFhMTQwNjk2OTcwMmQyZGUyOWRhODE5IjtzOjE2OiJhcHBsaWNhdGlvbl9yb2xlIjthOjI6e3M6MjoiaWQiO2k6OTtzOjM6Il9pZCI7czoyNDoiNTNmYjk2M2I2MTYzNjMyMjgxMDAwMDAwIjt9czoxMToiYXBwbGljYXRpb24iO2E6Mjp7czozOiJ1aWQiO3M6NjQ6ImI5ZTE4ZGNkOGJmYWI4ZTM0ZmU5OGYzNmQ4ZmM4ZDY4NjM3Yjk4M2JjYjYzZjFiYjFmMDZjMWRiZDgyOWMyNzYiO3M6NDoibmFtZSI7czozMToiR3JhbmF0dW0gRmluYW5jZWlybyBFbXByZXNhcmlhbCI7fXM6NzoiYWNjb3VudCI7YToyNTp7czoyOiJpZCI7aTo1OTM2MTtzOjEzOiJmaW5hbmNlaXJvX2lkIjtpOjU5MzYxO3M6MzoiX2lkIjtzOjI0OiI1NzBkM2JkMjY5NzAyZDY4M2QzNTFmMDMiO3M6MTA6ImxlZ2FsX25hbWUiO3M6NjM6IkNlbnRybyBFc3DDrXJpdGEgQmVuZWZpY2VudGUgVW5pw6NvIGRvIFZlZ2V0YWwgLSBOw7pjbGVvIEdhc3BhciI7czoxMDoidHJhZGVfbmFtZSI7czoxNDoiTsOaQ0xFTyBHQVNQQVIiO3M6ODoiZG9jdW1lbnQiO3M6MTQ6IjMzNDg1NjE2MDAwMTU5IjtzOjI6ImltIjtzOjA6IiI7czo1OiJwaG9uZSI7czoxNToiKDYxKSA5OTI4Ni03MDAzIjtzOjk6InNlY3Rvcl9pZCI7aTozO3M6ODoic3RhdGVfaWQiO2k6NztzOjExOiJidXNpbmVzc19pZCI7aTowO3M6NzoiY2l0eV9pZCI7aToxO3M6NzoiYWRkcmVzcyI7czo0Njoiw4FyZWEgSXNvbGFkYSBuwrogNCwgRmF6ZW5kYSBFbmdlbmhvIFF1ZWltYW5kbyI7czoxNDoiYWRkcmVzc19udW1iZXIiO3M6MToiNCI7czoxODoiYWRkcmVzc19jb21wbGVtZW50IjtzOjA6IiI7czo4OiJkaXN0cmljdCI7czoxMToiQnJhemzDom5kaWEiO3M6ODoiemlwX2NvZGUiO3M6MDoiIjtzOjk6ImlzX2FjdGl2ZSI7aToxO3M6MTU6ImlzX2ZpcnN0X2FjY2VzcyI7aTowO3M6MTA6ImlzX2NvbXBhbnkiO2k6MTtzOjEwOiJleHBpcmF0aW9uIjtzOjEwOiIyMDE2LTA0LTE5IjtzOjMwOiJhZGRpdGlvbmFsX2RheXNfZm9yX2V4cGlyYXRpb24iO2k6MDtzOjQ6ImxvZ28iO3M6MTM1OiJodHRwczovL3MzLXNhLWVhc3QtMS5hbWF6b25hd3MuY29tL2dyYW5hdHVtL3Byb2R1Y3Rpb24vdXBsb2Fkcy9hY2NvdW50L2xvZ28vNTcwZDNiZDI2OTcwMmQ2ODNkMzUxZjAzL3NtYWxsX0xvZ29fR2FzcGFyXzMwX0Fub3NfSnBlZy5qcGciO3M6MTA6ImNyZWF0ZWRfYXQiO3M6MjQ6IjIwMTYtMDQtMTJUMTg6MTg6NDguMTg4WiI7czoxNDoiaXNfc3VwZXJfYWRtaW4iO2k6MDt9czoxMjoic3Vic2NyaXB0aW9uIjthOjQ6e3M6MTA6ImV4cGlyYXRpb24iO3M6MTA6IjIwMjAtMDEtMjUiO3M6MzA6ImFkZGl0aW9uYWxfZGF5c19mb3JfZXhwaXJhdGlvbiI7aTowO3M6ODoiaW5fdHJpYWwiO2k6MDtzOjE1OiJzaG93X29uYm9hcmRpbmciO2k6MDt9fX19czo4OiJwcm92aWRlciI7czo4OiJHcmFuYXR1bSI7fXM6OToidGltZXN0YW1wIjtzOjI1OiIyMDE5LTA5LTE5VDE3OjQwOjQxLTAzOjAwIjtzOjk6InNpZ25hdHVyZSI7czozMToiM2Z5OHR3dmNjZzRrc3Nra29rc293NG9ra2tna3NvOCI7fQ=='
        with open(
            os.path.join(FIXTURES_PATH, 'oauth.html'), 'r', encoding='utf-8'
        ) as file:
            text = file.read()

        result = utils.parse_opauth(text)

        self.assertEqual(expected, result)

    def test_parse_conta_ids(self):
        expected = {'C1. Caixa Local': '62507', 'C2. BB - Conta Corrente': '62503'}
        with open(
            os.path.join(FIXTURES_PATH, 'lancamentos.html'), 'r', encoding='utf-8'
        ) as file:
            text = file.read()

        result = utils.parse_conta_ids(text)

        self.assertEqual(expected, result)

    def test_parse_tipos(self):
        expected = {'Pagos': 'LP', 'Recebidos': 'LR'}
        with open(
            os.path.join(FIXTURES_PATH, 'lancamentos.html'), 'r', encoding='utf-8'
        ) as file:
            text = file.read()

        result = utils.parse_tipos(text)

        self.assertEqual(expected, result)

    def test_parse_categoria_ids(self):
        expected = {
            '01. Receitas Operacionais': '749509',
            '01.1. Mensalidade (Fundo Operacional)': '749510',
            '01.2. Dízimo/Boa Vontade': '751905',
            '02. Receitas de Alimentação': '751889',
            '02.1 Taxa de Alimentação - Sócio': '751892',
            '02.2. Taxa de Alimentação - Filhos': '751893',
        }
        with open(
            os.path.join(FIXTURES_PATH, 'lancamentos.html'), 'r', encoding='utf-8'
        ) as file:
            text = file.read()

        result = utils.parse_categoria_ids(text)

        self.assertEqual(expected, result)


class TestFormatCsv(unittest.TestCase):
    '''Test the format_csv function with different return_types.'''

    with open(
        os.path.join(FIXTURES_PATH, 'export.txt'), 'r', encoding='utf-8'
    ) as file:
        csv = file.read()

    def test_list(self):
        expected = [
            {'Data': '03/09/2019', 'Valor': 1.0},
            {'Data': '14/09/2019', 'Valor': 0.01},
        ]

        result = utils.convert_csv(self.csv, 'list')

        self.assertEqual(expected, result)

    def test_pandas_data_frame(self):
        expected = pd.DataFrame(
            {'Data': ['03/09/2019', '14/09/2019'], 'Valor': [1.0, 0.01]}
        )

        result = utils.convert_csv(self.csv, 'pandas.DataFrame')

        self.assertTrue(expected.equals(result))


if __name__ == '__main__':
    unittest.main()
