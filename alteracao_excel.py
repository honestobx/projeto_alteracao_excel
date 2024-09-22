import os
import pandas as pd
from django.core.management.base import BaseCommand
 
from app.models import ModelTeste1, ModelTeste2


class Command(BaseCommand):
    help = 'Atualiza informações extras a partir de um arquivo Excel'
 
    def handle(self, *args, **kwargs):
        print("Começo da alteração")
        current_dir = os.path.dirname(os.path.abspath(__file__))
 
        # Caminho do arquivo Excel na subpasta "excel"
        excel_path = os.path.join(current_dir, 'excel', 'alteracao.xlsx')  
        df = pd.read_excel(excel_path)
 
        for _, row in df.iterrows():
            # Pega os dados da linha atual pegando pelo nome da coluna
            numero = row['Numero']
            obs = row['Observação']
            valor = row['Valor']
 
            try:
                # Pega o o produto ou o que seja pelo numero dele no caso por um campo especifico que é bom ser único se não for pelo ID em si
                model_teste1 = ModelTeste1.objects.get(numero=numero)

                # Atualiza campo da tabela ModelTeste1 se o campo não vier vazio no excel
                if not pd.isna(obs) and obs !='':
                    model_teste1.obs = obs
                model_teste1.save()
 
                # Atualiza a tabela ModelTeste2, vinculada pelo model_teste1_id que vincula ela a tabela ModelTeste2
                model_teste2 = ModelTeste2.objects.get(model_teste1_id=model_teste1.id)
 
                if not pd.isna(valor) and valor !='':
                    model_teste2.valor = valor
 
                model_teste2.save()
 
                self.stdout.write(self.style.SUCCESS(f'Produto {numero} atualizado com sucesso.'))
 
            except ModelTeste1.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'ModelTeste1 {numero} não encontrado.'))
            except ModelTeste2.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'ModelTeste2 para o caso {numero} não encontrado.'))
 
        print("Fim da alteração em lote")