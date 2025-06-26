import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import 'utils.dart';

class SingleChart extends StatelessWidget {
  final String xAxisLabel;
  final String yAxisLabel;
  final Future<List<(double, double)>> fetchData;
  final double? angleThreshold;

  const SingleChart({
    super.key,
    required this.xAxisLabel,
    required this.yAxisLabel,
    required this.fetchData,
    this.angleThreshold = 0.01,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return FutureBuilder<List<(double, double)>>(
      future: fetchData,
      builder: (context, snapshot) => switch (snapshot) {
        AsyncSnapshot(connectionState: ConnectionState.waiting) => const Center(
            child: CircularProgressIndicator(),
          ),
        AsyncSnapshot(hasError: true) => Center(
            child: Text('Ошибка: ${snapshot.error}'),
          ),
        AsyncSnapshot(hasData: true, data: final data!) => () {
            final spots = ChartUtils.getVisibleSpots(data);
            final values = spots.map((e) => e.y).toList();

            final maxValue =
                values.isEmpty ? 0 : values.reduce((a, b) => a > b ? a : b);
            final minValue =
                values.isEmpty ? 0 : values.reduce((a, b) => a < b ? a : b);

            return LineChart(
              LineChartData(
                maxY: maxValue * 1.1,
                minY: minValue * 1.1,
                lineTouchData: LineTouchData(enabled: true),
                borderData: FlBorderData(show: true),
                titlesData: FlTitlesData(
                  topTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  rightTitles: const AxisTitles(
                    sideTitles: SideTitles(showTitles: false),
                  ),
                  bottomTitles: AxisTitles(
                    axisNameWidget: Text(xAxisLabel),
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 32,
                    ),
                  ),
                  leftTitles: AxisTitles(
                    axisNameWidget: Text(yAxisLabel),
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 64,
                    ),
                  ),
                ),
                lineBarsData: [
                  LineChartBarData(
                    // barWidth: 0.5,
                    isCurved: true,
                    color: theme.colorScheme.primary,
                    spots: spots,
                  ),
                ],
              ),
            );
          }(),
        _ => const Center(child: Text('Нет данных')),
      },
    );
  }
}
