import os
import pandas as pd
from django.core.management.base import BaseCommand
from app.models import ModelTeste1, ModelTeste2

class Command(BaseCommand):
    help = 'Atualiza informações extras a partir de um arquivo Excel'

    def handle(self, *args, **kwargs):
        self.stdout.write("Começo da alteração")
        excel_path = self.get_excel_path('alteracao.xlsx')
        df = self.read_excel_file(excel_path)

        for _, row in df.iterrows():
            numero, obs, valor = self.extract_row_data(row)
            self.update_model_data(numero, obs, valor)

        self.stdout.write("Fim da alteração em lote")

    def get_excel_path(self, filename):
        """Retorna o caminho completo do arquivo Excel."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, 'excel', filename)

    def read_excel_file(self, path):
        """Lê o arquivo Excel e retorna o dataframe."""
        return pd.read_excel(path)

    def extract_row_data(self, row):
        """Extrai os dados relevantes da linha do Excel."""
        numero = row['Numero']
        obs = row['Observação']
        valor = row['Valor']
        return numero, obs, valor

    def update_model_data(self, numero, obs, valor):
        """Atualiza as informações nos modelos ModelTeste1 e ModelTeste2."""
        try:
            model_teste1 = self.update_model_teste1(numero, obs)
            self.update_model_teste2(model_teste1.id, valor)
            self.stdout.write(self.style.SUCCESS(f'Produto {numero} atualizado com sucesso.'))
        except ModelTeste1.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'ModelTeste1 {numero} não encontrado.'))
        except ModelTeste2.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'ModelTeste2 para o ModelTeste1 {numero} não encontrado.'))

    def update_model_teste1(self, numero, obs):
        """Atualiza o campo 'obs' em ModelTeste1, se necessário."""
        model_teste1 = ModelTeste1.objects.get(numero=numero)
        if not pd.isna(obs) and obs != '':
            model_teste1.obs = obs
        model_teste1.save()
        return model_teste1

    def update_model_teste2(self, model_teste1_id, valor):
        """Atualiza o campo 'valor' em ModelTeste2, se necessário."""
        model_teste2 = ModelTeste2.objects.get(model_teste1_id=model_teste1_id)
        if not pd.isna(valor) and valor != '':
            model_teste2.valor = valor
        model_teste2.save()
