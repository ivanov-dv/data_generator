import abc
import csv
import io
import xlsxwriter

from typing import Generator

from config import TXT_ENCODING, CSV_ENCODING, OUTPUT_DIR


class IFileCreator(abc.ABC):
    """Interface for creating files."""

    def __init__(self, data: list | Generator, filename: str = None, output_dir = OUTPUT_DIR):
        self.data = data
        self.filename = filename
        self.output_dir = output_dir


    @abc.abstractmethod
    def create(self) -> io.BytesIO | str:
        """
        Create file with random data.
        :return: BytesIO or created filename.
        """


class ExcelFileCreator(IFileCreator):
    def create(self):
        output = f'{self.output_dir}/{self.filename}.xlsx' if self.filename else io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        row = 0
        for record in self.data:
            worksheet.write_row(row, 0, record)
            row += 1
        workbook.close()

        output.seek(0) if not self.filename else None

        return f'{self.filename}.xlsx' if self.filename else output


class CsvFileCreator(IFileCreator):
    def _create_to_file(self):
        """Helper method. Create csv file with random data to file."""
        with open(f'{self.output_dir}/{self.filename}.csv', 'w', newline='', encoding=CSV_ENCODING) as csvfile:
            writer = csv.writer(csvfile)
            for row in self.data:
                writer.writerow(row)
            return f'{self.filename}.csv'

    def _create_to_buffer(self):
        """Helper method. Create csv file with random data to buffer."""
        output = io.StringIO()
        writer = csv.writer(output)
        for row in self.data:
            writer.writerow(row)
        output.seek(0)
        return io.BytesIO(output.getvalue().encode('utf-8'))

    def create(self):
        return self._create_to_file() if self.filename else self._create_to_buffer()


class TxtFileCreator(IFileCreator):
    def _create_to_file(self):
        """Helper method. Create txt file with random data to file."""
        with open(f'{self.output_dir}/{self.filename}.txt', 'w', encoding=TXT_ENCODING) as txt_file:
            for row in self.data:
                txt_file.write(', '.join(map(str, row)) + '\n')
            return f'{self.filename}.txt'

    def _create_to_buffer(self):
        """Helper method. Create txt file with random data to buffer."""
        output = io.StringIO()
        for row in self.data:
            output.write(', '.join(map(str, row)) + '\n')
        output.seek(0)
        return io.BytesIO(output.getvalue().encode('utf-8'))

    def create(self):
        return self._create_to_file() if self.filename else self._create_to_buffer()
