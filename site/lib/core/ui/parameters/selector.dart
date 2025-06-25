import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_math_fork/flutter_math.dart';

import '../../settings.dart';
import 'model.dart';

part 'inputs.dart';

class ParametersSelector extends StatefulWidget {
  const ParametersSelector({
    super.key,
    required this.parameters,
    required this.onApply,
  });

  final List<ParameterModel> parameters;
  final void Function(Map<String, dynamic> parameters) onApply;

  @override
  State<ParametersSelector> createState() => _ParametersSelectorState();
}

class _ParametersSelectorState extends State<ParametersSelector> {
  late Map<String, dynamic> _data =
      widget.parameters.fold<Map<String, dynamic>>(
    {},
    (acc, parameter) {
      return acc..[parameter.key] = parameter.initialValue;
    },
  );

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const SizedBox(
            height: AppUISettings.defaultPadding,
          ),
          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: AppUISettings.defaultPadding,
            ),
            child: Text(
              "Параметры",
              style: Theme.of(context).textTheme.titleLarge,
            ),
          ),
          const SizedBox(
            height: AppUISettings.defaultPadding,
          ),
          Expanded(
            child: ListView.separated(
              padding: EdgeInsets.symmetric(
                horizontal: AppUISettings.defaultPadding,
              ),
              itemCount: widget.parameters.length,
              separatorBuilder: (context, index) => Padding(
                padding: const EdgeInsets.symmetric(
                  vertical: AppUISettings.defaultPadding / 2,
                ),
                child: const Divider(),
              ),
              itemBuilder: (context, index) {
                final parameter = widget.parameters[index];

                return parameter.map(
                  value: (parameter) => _ValueInput(
                    parameter: parameter,
                    onChanged: (value) {
                      _data[parameter.key] = value;
                    },
                  ),
                  toggle: (parameter) => _ToggleInput(
                    parameter: parameter,
                    onChanged: (value) {
                      _data[parameter.key] = value;
                    },
                  ),
                );
              },
            ),
          ),
          const SizedBox(
            height: AppUISettings.defaultPadding,
          ),
          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: AppUISettings.defaultPadding,
            ),
            child: FilledButton.tonal(
              onPressed: () {
                widget.onApply(_data);
              },
              child: const Center(child: Text("Применить")),
            ),
          ),
          const SizedBox(
            height: AppUISettings.defaultPadding,
          ),
        ],
      ),
    );
  }
}
