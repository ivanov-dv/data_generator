import csv
import io
import xlsxwriter

from typing import Generator

from config import TXT_ENCODING, CSV_ENCODING, OUTPUT_DIR
from utils.entities import IFileCreator

# Если тут будет 50 разных ипов -этот файл будет содержать 50 методов?
# Не сликшом ли сложно + представь чо нужно в название файла добавлять цифру 123 для одного случая и цифру 2345 для другого?
# ТАкже есть повторяющийся код - это не драй
class FileCreator(IFileCreator):
    @staticmethod
    def create_excel(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Создает Excel файл и сохраняет в файл или буфер.

        :param data: Данные
        :param file_name: Имя файла. Если None, то сохранение в буфер.
        :return: Объект io.BytesIO или None
        """

        output = f'{OUTPUT_DIR}/{file_name}' if file_name else io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        # магические числа

        row = 0
        for record in data:
            worksheet.write_row(row, 0, record)
            row += 1

        workbook.close()

        if not file_name:
            output.seek(0)
            return output

    @staticmethod
    def create_csv(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Создает CSV файл и сохраняет в файл или буфер.

        :param data: Данные
        :param file_name: Имя файла. Если None, то сохранение в буфер.
        :return: Объект io.BytesIO или None
        """

        if file_name:
            with open(f'{OUTPUT_DIR}/{file_name}', 'w', newline='', encoding=CSV_ENCODING) as csvfile:
                writer = csv.writer(csvfile)
                for row in data:
                    writer.writerow(row)

        else:
            output = io.StringIO()
            writer = csv.writer(output)
            for row in data:
                writer.writerow(row)
            output.seek(0)
            return io.BytesIO(output.getvalue().encode('utf-8'))

    @staticmethod
    def create_txt(data: list | Generator, file_name: str = None) -> io.BytesIO | None:
        """
        Создает TXT файл и сохраняет в файл или буфер.

        :param data: Данные
        :param file_name: Имя файла. Если None, то сохранение в буфер.
        :return: Объект io.BytesIO или None
        """

        if file_name:
            with open(f'{OUTPUT_DIR}/{file_name}', 'w', encoding=TXT_ENCODING) as txt_file:
                for row in data:
                    txt_file.write(', '.join(map(str, row)) + '\n')
        else:
            output = io.StringIO()
            for row in data:
                output.write(', '.join(map(str, row)) + '\n')
            output.seek(0)
            return io.BytesIO(output.getvalue().encode('utf-8'))
