import 'dart:math' as math;
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

class SingleChart extends StatefulWidget {
  final String xAxisLabel;
  final String yAxisLabel;
  final Future<List<(double, double)>> fetchData;
  final double? angleThreshold;

  const SingleChart({
    super.key,
    required this.xAxisLabel,
    required this.yAxisLabel,
    required this.fetchData,
    required this.angleThreshold,
  });

  @override
  State<SingleChart> createState() => _SingleChartState();
}

class _SingleChartState extends State<SingleChart> {
  List<(double, double)>? _allData;

  double _calculateAngle(
      (double, double) p1, (double, double) p2, (double, double) p3) {
    final v1 = (p2.$1 - p1.$1, p2.$2 - p1.$2);
    final v2 = (p3.$1 - p2.$1, p3.$2 - p2.$2);

    final dot = v1.$1 * v2.$1 + v1.$2 * v2.$2;
    final mag1 = math.sqrt(v1.$1 * v1.$1 + v1.$2 * v1.$2);
    final mag2 = math.sqrt(v2.$1 * v2.$1 + v2.$2 * v2.$2);

    if (mag1 == 0 || mag2 == 0) return 0;

    final cosAngle = dot / (mag1 * mag2);
    final angleRad = math.acos(cosAngle.clamp(-1.0, 1.0));
    final angleDeg = angleRad * 180 / math.pi;

    return angleDeg;
  }

  List<(double, double)> _simplifyByAngle(
      List<(double, double)> data, double threshold) {
    if (data.length <= 2) return data;

    final simplified = <(double, double)>[data.first];
    int deleted = 0;

    for (int i = 1; i < data.length - 1; i++) {
      final angle = _calculateAngle(simplified.last, data[i], data[i + 1]);

      if (angle.abs() > threshold) {
        simplified.add(data[i]);
      } else {
        deleted++;
      }
    }
    print('Deleted: $deleted');

    simplified.add(data.last);
    return simplified;
  }

  List<FlSpot> _getVisibleSpots() {
    if (_allData == null) return [];

    var visibleData = _allData!;

    // Упрощение по углу
    if (widget.angleThreshold != null && widget.angleThreshold! > 0) {
      visibleData = _simplifyByAngle(visibleData, widget.angleThreshold!);
    }

    // Ограничение количества точек
    // if (visibleData.length > 1000) {
    //   final step = visibleData.length / 1000;
    //   visibleData = [
    //     for (int i = 0; i < visibleData.length; i += step.ceil()) visibleData[i]
    //   ];
    // }

    return visibleData.map((e) => FlSpot(e.$1, e.$2)).toList();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return FutureBuilder<List<(double, double)>>(
      future: widget.fetchData,
      builder: (context, snapshot) => switch (snapshot) {
        AsyncSnapshot(connectionState: ConnectionState.waiting) => const Center(
            child: CircularProgressIndicator(),
          ),
        AsyncSnapshot(hasError: true) => Center(
            child: Text('Ошибка: ${snapshot.error}'),
          ),
        AsyncSnapshot(hasData: true, data: final data!) => () {
            _allData = data;
            final spots = _getVisibleSpots();
            final values = spots.map((e) => e.y).toList();

            final maxValue =
                values.isEmpty ? 0 : values.reduce((a, b) => a > b ? a : b);
            final minValue =
                values.isEmpty ? 0 : values.reduce((a, b) => a < b ? a : b);

            return LineChart(
              LineChartData(
                maxY: maxValue * 1.1,
                minY: minValue * 0.9,
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
                    axisNameWidget: Text(widget.xAxisLabel),
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 32,
                    ),
                  ),
                  leftTitles: AxisTitles(
                    axisNameWidget: Text(widget.yAxisLabel),
                    sideTitles: SideTitles(
                      showTitles: true,
                      reservedSize: 64,
                    ),
                  ),
                ),
                lineBarsData: [
                  LineChartBarData(
                    barWidth: 0.5,
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
