import 'package:flutter/material.dart';

import '../core/settings.dart';
import '../navigation/navigator.dart';

class LabsPage extends StatelessWidget {
  const LabsPage({super.key});

  static const labTitles = [
    "Нагревательный прибор",
    "Математический маятник",
    "Модель Лотки-Вольтера",
    "Движение тела на вращающемся диске (Сила Кориолиса)",
    "Одномерное уравнение переноса",
    "Двухмерное уравнение движения",
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Лабораторные работы"),
      ),
      body: Center(
        child: ConstrainedBox(
          constraints:
              const BoxConstraints(maxWidth: AppUISettings.maxScreenWidth),
          child: ListView.builder(
            padding:
                const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
            itemCount: labTitles.length,
            primary: false,
            itemBuilder: (context, index) {
              final title = labTitles[index];
              return Card(
                elevation: 2.0,
                margin: const EdgeInsets.symmetric(vertical: 8.0),
                clipBehavior: Clip.antiAlias,
                child: InkWell(
                  onTap: () => AppNavigator.openLab(index + 1),
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Text(
                      title,
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
