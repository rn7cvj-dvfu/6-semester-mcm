import 'dart:math' as math;

import 'package:fl_chart/fl_chart.dart';

final class ChartUtils {
  static double _calculateAngle(
    (double, double) p1,
    (double, double) p2,
    (double, double) p3,
  ) {
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

  static List<(double, double)> simplifyByAngle(
    List<(double, double)> data, [
    double threshold = 0.01,
  ]) {
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

  static List<FlSpot> getVisibleSpots(
    List<(double, double)>? allData, [
    double? angleThreshold = 0.01,
  ]) {
    if (angleThreshold != null && angleThreshold > 0) {
      return simplifyByAngle(allData ?? [], angleThreshold)
          .map((e) => FlSpot(e.$1, e.$2))
          .toList();
    }

    return allData?.map((e) => FlSpot(e.$1, e.$2)).toList() ?? [];
  }
}
