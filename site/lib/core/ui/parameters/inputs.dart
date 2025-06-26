part of 'selector.dart';

class _ValueInput extends StatelessWidget {
  final ParameterModelValue parameter;
  final ValueChanged<double> onChanged;
  final double currentValue;

  const _ValueInput({
    super.key,
    required this.currentValue,
    required this.parameter,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final controller = TextEditingController(
      text: currentValue.toStringAsFixed(2),
    );

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(parameter.title),
              ),
              if (parameter.unit != null)
                Math.tex(
                  parameter.unit!,
                  settings: const TexParserSettings(
                    strict: Strict.ignore, // Отключить строгий режим
                  ),
                ),
            ],
          ),
          Slider(
            value: currentValue,
            min: parameter.minValue,
            max: parameter.maxValue,
            divisions: parameter.stepCount,
            onChanged: onChanged,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              SizedBox(
                width: AppUISettings.selectorWidth -
                    AppUISettings.defaultPadding * 2,
                child: TextFormField(
                  
                  controller: controller,
                  keyboardType: const TextInputType.numberWithOptions(
                    decimal: true,
                  ),
                  inputFormatters: [
                    FilteringTextInputFormatter.allow(
                      RegExp(r'^\d+\.?\d{0,2}'),
                    ),
                  ],
                  onChanged: (str) {
                    final newValue = double.tryParse(str);

                    if (newValue == null) {
                      return;
                    }

                    final clampedValue = newValue.clamp(
                      parameter.minValue,
                      parameter.maxValue,
                    );

                    onChanged(clampedValue);
                  },
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

class _ToggleInput extends StatelessWidget {
  final ParameterModelToggle parameter;
  final ValueChanged<bool> onChanged;

  final bool currentValue;

  const _ToggleInput({
    super.key,
    required this.currentValue,
    required this.parameter,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return SwitchListTile(
      title: Text(parameter.title),
      value: currentValue,
      onChanged: onChanged,
    );
  }
}
