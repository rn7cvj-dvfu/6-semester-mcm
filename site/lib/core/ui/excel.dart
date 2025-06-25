import 'dart:js_interop';
import 'dart:typed_data';

import 'package:excel/excel.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:web/web.dart' hide Text;

import '../settings.dart';

// Функция для создания Excel с промежуточными паузами
Future<List<int>?> _createExcelInBackground(Map<String, dynamic> params) async {
  final columnNames = params['columnNames'] as List<String>;
  final data = params['data'] as Map<String, List<dynamic>>;

  var excel = Excel.createExcel();
  var sheet = excel['Sheet1'];

  // Добавляем заголовки
  sheet.cell(CellIndex.indexByString('A1')).value =
      TextCellValue(columnNames[0]);
  sheet.cell(CellIndex.indexByString('B1')).value =
      TextCellValue(columnNames[1]);

  List<dynamic> column1Data = data[columnNames[0]]!;
  List<dynamic> column2Data = data[columnNames[1]]!;

  int maxLength =
      [column1Data.length, column2Data.length].reduce((a, b) => a > b ? a : b);

  // Обрабатываем данные порциями, чтобы не блокировать UI
  const int batchSize = 1000;
  for (int batchStart = 0; batchStart < maxLength; batchStart += batchSize) {
    int batchEnd = (batchStart + batchSize).clamp(0, maxLength);

    for (int i = batchStart; i < batchEnd; i++) {
      var value1 = i < column1Data.length ? column1Data[i] : null;
      if (value1 != null) {
        sheet.cell(CellIndex.indexByString('A${i + 2}')).value =
            value1 is String
                ? TextCellValue(value1)
                : value1 is int
                    ? IntCellValue(value1)
                    : value1 is double
                        ? DoubleCellValue(value1)
                        : TextCellValue(value1.toString());
      }

      var value2 = i < column2Data.length ? column2Data[i] : null;
      if (value2 != null) {
        sheet.cell(CellIndex.indexByString('B${i + 2}')).value =
            value2 is String
                ? TextCellValue(value2)
                : value2 is int
                    ? IntCellValue(value2)
                    : value2 is double
                        ? DoubleCellValue(value2)
                        : TextCellValue(value2.toString());
      }
    }

    // Даем UI время для обновления после каждой порции
    if (batchEnd < maxLength) {
      await Future.delayed(const Duration(milliseconds: 1));
    }
  }

  return excel.encode();
}

Future<void> createAndDownloadExcel(
  List<String> columnNames,
  Map<String, List<dynamic>> data, {
  String fileName = 'data',
}) async {
  if (columnNames.length != 2) {
    throw ArgumentError('columnNames должен содержать ровно 2 элемента');
  }

  if (!data.containsKey(columnNames[0]) || !data.containsKey(columnNames[1])) {
    throw ArgumentError(
        'data должен содержать ключи, соответствующие columnNames');
  }

  // Выполняем создание Excel с промежуточными паузами
  final excelBytes = await _createExcelInBackground({
    'columnNames': columnNames,
    'data': data,
  });

  if (excelBytes != null) {
    final blob = Blob([Uint8List.fromList(excelBytes).toJS].toJS);
    final url = URL.createObjectURL(blob);

    HTMLAnchorElement()
      ..href = url
      ..download = "$fileName.xlsx"
      ..click();

    URL.revokeObjectURL(url);
  }
}

class ExcelButton extends StatefulWidget {
  final String fileName;
  final String col1_name;
  final String col2_name;
  final Future<List<(double, double)>> fetchData;

  const ExcelButton({
    super.key,
    required this.fetchData,
    required this.col1_name,
    required this.col2_name,
    required this.fileName,
  });

  @override
  State<ExcelButton> createState() => _ExcelButtonState();
}

class _ExcelButtonState extends State<ExcelButton> {
  bool _isLoading = false;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: _isLoading
            ? null
            : () async {
                setState(() {
                  _isLoading = true;
                });

                try {
                  // Сначала показываем что получаем данные
                  final data = await widget.fetchData;

                  // Затем создаем Excel файл
                  await createAndDownloadExcel(
                    [widget.col1_name, widget.col2_name],
                    {
                      widget.col1_name: data.map((e) => e.$1).toList(),
                      widget.col2_name: data.map((e) => e.$2).toList(),
                    },
                    fileName: widget.fileName,
                  );
                } catch (e) {
                  if (mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Ошибка создания файла: $e')),
                    );
                  }
                } finally {
                  if (mounted) {
                    setState(() {
                      _isLoading = false;
                    });
                  }
                }
              },
        child: Padding(
          padding: const EdgeInsets.all(AppUISettings.defaultPadding),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              _isLoading
                  ? const SizedBox(
                      width: 16,
                      height: 16,
                      child: CircularProgressIndicator(strokeWidth: 2),
                    )
                  : const Icon(Icons.downloading_rounded),
              const SizedBox(width: 8.0),
              Text(
                _isLoading ? "Создание..." : "Скачать excel",
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
