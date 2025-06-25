import 'dart:math';

import 'package:flutter/material.dart';

import '../../core/settings.dart';
import '../../core/ui/back_button.dart';
import '../../core/ui/chart/single.dart';
import '../../core/ui/excel.dart';
import '../../core/ui/parameters/model.dart';
import '../../core/ui/parameters/selector.dart';
import '../../navigation/navigator.dart';

class Lab2 extends StatefulWidget {
  const Lab2({super.key});

  @override
  State<Lab2> createState() => _Lab1State();
}

class _Lab1State extends State<Lab2> {
  final _initialParameters = [
    ParameterModel.value(
      key: 'L',
      title: 'Длина нити (L)',
      unit: r'Вт',
      minValue: 0.1,
      maxValue: 5,
      initialValue: 1,
    ),
    ParameterModel.value(
      key: 'm',
      title: 'Масса (m)',
      unit: r'кг',
      minValue: 0.1,
      maxValue: 10,
      initialValue: 1,
    ),
    ParameterModel.value(
      key: 'theta_o',
      title: 'Начальное отклонение (θ₀)',
      unit: r'рад',
      minValue: -pi / 2,
      maxValue: pi / 2,
      initialValue: pi / 4,
    ),
    ParameterModel.value(
      key: 'omega_small',
      title: 'Угловая скорость в начальный момент времени',
      unit: r'\frac{м}{с}',
      minValue: 0,
      maxValue: 10,
      initialValue: 1,
    ),
    ParameterModel.value(
      key: 'k',
      title: 'Коэфф. трения (k)',
      minValue: 1,
      maxValue: 5,
      initialValue: 1,
    ),
    ParameterModel.value(
      key: 'omega',
      title: 'Частота вынужденных колебаний',
      unit: r'\frac{рад}{сек}',
      minValue: 10,
      maxValue: 40,
      initialValue: 20,
    ),
    ParameterModel.value(
      key: 'A',
      title: 'Амплитуда вынужденных колебаний',
      unit: r'\frac{Н}{м}',
      minValue: 0,
      maxValue: 10,
      initialValue: 0,
    ),
    ParameterModel.value(
      key: 'time',
      title: 'Время симуляции',
      unit: r'сек',
      minValue: 10,
      maxValue: 3000,
      initialValue: 15,
    ),
  ];

  Future<List<(double, double)>> _fetchData = Future.value([]);

  Future<List<double>> _simulate(Map<String, dynamic> params) async {
    final double L = params['L']?.toDouble() ?? 1.0;
    final double m = params['m']?.toDouble() ?? 1.0;
    final double theta0 = params['theta_o']?.toDouble() ?? pi / 4;
    final double omega0 = params['omega_small']?.toDouble() ?? 0.0;
    final double k = params['k']?.toDouble() ?? 1.0;
    final double omegaExt = params['omega']?.toDouble() ?? 20.0;
    final double A = params['A']?.toDouble() ?? 0.0;
    final double time = params['time']?.toDouble() ?? 2400.0;

    const double g = 9.81;
    const int nSteps = 10000;
    final double dt = time / nSteps;

    final double alpha = A / (m * L * L);
    final double beta = k / (m * L * L);
    final double gamma = g / L;

    List<double> y = [theta0, omega0];
    final List<double> result = [];

    for (int i = 0; i <= nSteps; i++) {
      final double t = i * dt;
      result.add(y[0]);

      if (i < nSteps) {
        final List<double> k1 =
            _pendulumDerivatives(t, y, alpha, beta, gamma, omegaExt);
        final List<double> k2 = _pendulumDerivatives(
            t + dt / 2,
            [y[0] + k1[0] * dt / 2, y[1] + k1[1] * dt / 2],
            alpha,
            beta,
            gamma,
            omegaExt);
        final List<double> k3 = _pendulumDerivatives(
            t + dt / 2,
            [y[0] + k2[0] * dt / 2, y[1] + k2[1] * dt / 2],
            alpha,
            beta,
            gamma,
            omegaExt);
        final List<double> k4 = _pendulumDerivatives(
            t + dt,
            [y[0] + k3[0] * dt, y[1] + k3[1] * dt],
            alpha,
            beta,
            gamma,
            omegaExt);

        y[0] += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]);
        y[1] += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]);
      }
    }

    return result;
  }

  List<double> _pendulumDerivatives(
    double t,
    List<double> y,
    double alpha,
    double beta,
    double gamma,
    double omegaExt,
  ) {
    final double theta = y[0];
    final double omega = y[1];

    final double dthetaDt = omega;
    final double domegaDt =
        -beta * omega - gamma * sin(theta) + alpha * cos(omegaExt * t);

    return [dthetaDt, domegaDt];
  }

  Future<List<(double, double)>> _foldData(
    List<double> data,
    double dt,
  ) async {
    final n = data.length;
    final result = <(double, double)>[];

    for (int i = 0; i < n; i++) {
      final time = i * dt;
      final temperature = data[i];
      result.add((time, temperature));
    }

    return result;
  }

  @override
  Widget build(BuildContext context) {
    return Material(
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppUISettings.defaultPadding),
          child: Row(
            children: [
              SizedBox(
                width: 324,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Row(
                      children: [
                        AppBackButton(
                          onTap: AppNavigator.openLabs,
                        ),
                        SizedBox(width: AppUISettings.defaultPadding),
                        Expanded(
                          child: ExcelButton(
                            fetchData: _fetchData,
                            col1Name: 'Время (сек)',
                            col2Name: 'Температура (°C)',
                            fileName: 'lab2',
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: AppUISettings.defaultPadding),
                    Expanded(
                      child: ParametersSelector(
                        parameters: _initialParameters,
                        onApply: (params) {
                          _fetchData = _simulate(params).then(
                            (data) => _foldData(data, 0.1),
                          );
                          setState(() {});
                        },
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: AppUISettings.defaultPadding),
              Expanded(
                child: Card(
                  margin: EdgeInsets.zero,
                  child: Padding(
                    padding: const EdgeInsets.all(AppUISettings.defaultPadding),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          "График угла от времени",
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        const SizedBox(height: AppUISettings.defaultPadding),
                        Expanded(
                          child: SingleChart(
                            xAxisLabel: 'Время (сек)',
                            yAxisLabel: 'Угол theta (рад)',
                            fetchData: _fetchData,
                            angleThreshold: 0.01,
                          ),
                        )
                      ],
                    ),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
