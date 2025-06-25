import 'dart:math';

import 'package:flutter/material.dart';

import '../../core/settings.dart';
import '../../core/ui/back_button.dart';
import '../../core/ui/chart/single.dart';
import '../../core/ui/excel.dart';
import '../../core/ui/parameters/model.dart';
import '../../core/ui/parameters/selector.dart';
import '../../navigation/navigator.dart';

class Lab1 extends StatefulWidget {
  const Lab1({super.key});

  @override
  State<Lab1> createState() => _Lab1State();
}

class _Lab1State extends State<Lab1> {
  final _initialParameters = [
    ParameterModel.value(
      key: 'P',
      title: 'Мощность (P)',
      unit: r'Вт',
      minValue: 50,
      maxValue: 200,
      initialValue: 100,
    ),
    ParameterModel.value(
      key: 'm',
      title: 'Масса (m)',
      unit: r'кг',
      minValue: 0.1,
      maxValue: 1.0,
      initialValue: 0.3,
    ),
    ParameterModel.value(
      key: 'c',
      title: 'Удельная теплоемкость (c)',
      unit: r'\frac{Дж}{кг \cdot К}',
      minValue: 300,
      maxValue: 1000,
      initialValue: 500,
    ),
    ParameterModel.value(
      key: 'A',
      title: 'Площадь теплообмена (A)',
      unit: r'м^2',
      minValue: 0.005,
      maxValue: 0.05,
      initialValue: 0.01,
    ),
    ParameterModel.value(
      key: 'k',
      title: 'Коэфф. теплообмена (k)',
      unit: r'\frac{Вт}{м^2 \cdot К}',
      minValue: 5,
      maxValue: 20,
      initialValue: 10,
    ),
    ParameterModel.value(
      key: 'T0_C',
      title: 'Начальная t°',
      unit: r'°C',
      minValue: 10,
      maxValue: 40,
      initialValue: 20,
    ),
    ParameterModel.value(
      key: 'T_env_C',
      title: 't° среды',
      unit: r'°C',
      minValue: 10,
      maxValue: 40,
      initialValue: 20,
    ),
    ParameterModel.value(
      key: 'time',
      title: 'Время симуляции',
      unit: r'сек',
      minValue: 600,
      maxValue: 4800,
      initialValue: 2400,
    ),
    ParameterModel.toggle(
      key: 'use_thermostat',
      title: "Использовать терморегулятор",
      initialValue: true,
    ),
    ParameterModel.value(
      key: 'T_min_C',
      title: 'Мин. t° терморегулятора',
      unit: r'°C',
      minValue: 50,
      maxValue: 80,
      initialValue: 70,
    ),
    ParameterModel.value(
      key: 'T_max_C',
      title: 'Макс. t° терморегулятора',
      unit: r'°C',
      minValue: 90,
      maxValue: 120,
      initialValue: 100,
    ),
  ];

  Future<List<(double, double)>> _fetchData = Future.value([]);

  Future<List<double>> _simulate(Map<String, dynamic> params) async {
    const sigma = 5.67e-8; // Постоянная Стефана-Больцмана
    const T_k_0 = 273.13; // 0°C в Кельвинах

    final P = params['P']! as double;
    final m = params['m']! as double;
    final c = params['c']! as double;
    final A = params['A']! as double;
    final k = params['k']! as double;
    final useThermostat = params['use_thermostat']! as bool;
    final T_min_C = params['T_min_C']! as double;
    final T_max_C = params['T_max_C']! as double;
    final T0_C = params['T0_C']! as double;
    final T_env_C = params['T_env_C']! as double;
    final time = params['time']! as double;
    const dt = 0.1;
    const eta = 0.9;

    final T_min = T_min_C + T_k_0;
    final T_max = T_max_C + T_k_0;
    final T0 = T0_C + T_k_0;
    final T_env = T_env_C + T_k_0;

    final n_steps = (time / dt).round();
    final T = List<double>.filled(n_steps, 0);
    T[0] = T0;
    bool heating = true;

    bool thermostatControl(double currentT, bool isHeating) {
      if (isHeating && currentT >= T_max) {
        return false;
      }
      if (!isHeating && currentT <= T_min) {
        return true;
      }
      return isHeating;
    }

    for (int i = 1; i < n_steps; i++) {
      final current_T = T[i - 1];

      heating = thermostatControl(current_T, heating);
      final thermostat_effect = heating ? 1 : 0;

      final q_gen = P * eta * dt * (useThermostat ? thermostat_effect : 1);
      final q_conv = k * A * (current_T - T_env) * dt;
      final q_rad = sigma * A * (pow(current_T, 4) - pow(T_env, 4)) * dt;

      final delta_U = q_gen - q_conv - q_rad;
      final dT = delta_U / (m * c);
      T[i] = current_T + dT;
    }

    return T.map((temp) => temp - T_k_0).toList();
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
                            col1_name: 'Время (сек)',
                            col2_name: 'Температура (°C)',
                            fileName: 'lab1',
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
                          "График температуры от времени",
                          style: Theme.of(context).textTheme.titleLarge,
                        ),
                        const SizedBox(height: AppUISettings.defaultPadding),
                        Expanded(
                          child: SingleChart(
                            xAxisLabel: 'Время (сек)',
                            yAxisLabel: 'Температура (°C)',
                            fetchData: _fetchData,
                            angleThreshold: 0.009,
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
