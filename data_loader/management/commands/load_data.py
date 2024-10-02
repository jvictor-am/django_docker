# data_loader/management/commands/load_data.py
import pandas as pd
import asyncio
import aiohttp
import logging
import os
from django.core.management.base import BaseCommand
from data_loader.models import DataRecord
from asgiref.sync import sync_to_async

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Carrega dados a partir de uma planilha (CSV ou Excel) e enriquece com endereço da API dos Correios'

    def handle(self, *args, **kwargs):
        file_path = 'data.csv'  # Substitua pelo caminho do seu arquivo
        if not os.path.exists(file_path):
            logger.error("Arquivo data.csv não encontrado.")
            return

        # Carregar planilha com pandas
        try:
            df = self.load_data(file_path)
        except Exception as e:
            logger.error(f"Erro ao ler o arquivo: {e}")
            return

        # Limpar e preparar dados
        self.clean_data(df)

        logger.info(f"Dados carregados: {len(df)} registros encontrados.")

        # Executar chamadas assíncronas
        asyncio.run(self.process_data(df))

    def load_data(self, file_path):
        """Carrega dados do arquivo CSV ou Excel usando pandas."""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            return pd.read_excel(file_path)
        else:
            logger.error("Formato de arquivo não suportado. Utilize CSV ou Excel.")
            raise ValueError("Formato de arquivo não suportado.")

    def clean_data(self, df):
        """Limpa e prepara os dados do DataFrame."""
        df['CEP'] = df['CEP'].astype(str).str.replace(r'\D', '', regex=True)  # Manter apenas números no CEP
        df.dropna(subset=['CEP'], inplace=True)  # Remover linhas com CEP vazio
        df = df[df['CEP'] != '']  # Remover linhas com CEP vazio
        return df

    async def fetch_address(self, session, cep):
        """Faz uma chamada assíncrona à API dos Correios para buscar o endereço."""
        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Levanta um erro para códigos de resposta 4xx/5xx
                return await response.json()
        except aiohttp.ClientError as e:
            logger.error(f"Erro ao consultar o CEP {cep}: {e}")
            return None

    async def process_data(self, df):
        """Processa cada linha do DataFrame de forma assíncrona."""
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.enrich_and_save_data(session, row)) for _, row in df.iterrows()]
            await asyncio.gather(*tasks)

    async def enrich_and_save_data(self, session, row):
        """Enriquece os dados com o endereço e salva no banco de dados."""
        cep = row['CEP']
        address_data = await self.fetch_address(session, cep)
        if address_data and 'logradouro' in address_data:
            endereco = address_data.get('logradouro')  # Obtém logradouro
            uf = address_data.get('uf')  # Estado
            regiao = address_data.get('regiao')  # Região
        else:
            endereco = None
            uf = None
            regiao = None
            logger.warning(f"Endereço não encontrado para o CEP: {cep}")

        # Criar ou atualizar o registro no banco de dados
        await self.save_data(row['Nome'], row['Idade'], cep, endereco, uf, regiao)

    @sync_to_async
    def save_data(self, nome, idade, cep, endereco, uf, regiao):
        """Salva ou atualiza os dados no banco de dados."""
        try:
            DataRecord.objects.update_or_create(
                nome=nome,
                defaults={
                    'idade': idade,
                    'cep': cep,
                    'endereco': endereco,
                    'uf': uf,
                    'regiao': regiao
                }
            )
            logger.info(f"Registro salvo ou atualizado: {nome}")
        except Exception as e:
            logger.error(f"Erro ao salvar o registro {nome}: {e}")
