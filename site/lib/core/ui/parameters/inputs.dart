part of 'selector.dart';

class _ValueInput extends StatefulWidget {
  final ParameterModelValue parameter;
  final ValueChanged<double> onChanged;
  final ValueKey key;
  final double initialValue;

  const _ValueInput({
    required this.key,
    required this.initialValue,
    required this.parameter,
    required this.onChanged,
  });

  @override
  State<_ValueInput> createState() => _ValueInputState();
}

class _ValueInputState extends State<_ValueInput> {
  late final _controller = TextEditingController(
    text: widget.parameter.initialValue.toStringAsFixed(2),
  );
  late double _value = widget.parameter.initialValue;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(widget.parameter.title),
              if (widget.parameter.unit != null)
                Math.tex(
                  widget.parameter.unit!,
                  settings: const TexParserSettings(
                    strict: Strict.ignore, // Отключить строгий режим
                  ),
                ),
            ],
          ),
          Slider(
            value: _value,
            min: widget.parameter.minValue,
            max: widget.parameter.maxValue,
            divisions: widget.parameter.stepCount,
            onChanged: (newValue) {
              widget.onChanged(newValue);

              _value = newValue;
              _controller.text = newValue.toStringAsFixed(2);

              setState(() {});
            },
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              SizedBox(
                width: AppUISettings.selectorWidth -
                    AppUISettings.defaultPadding * 2,
                child: TextFormField(
                  key: widget.key,
                  controller: _controller,
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

                    widget.onChanged(newValue);

                    final newSliderValue = newValue.clamp(
                      widget.parameter.minValue,
                      widget.parameter.maxValue,
                    );
                    _value = newSliderValue;

                    // _controller.text = newValue.toStringAsFixed(2);

                    setState(() {});
                  },
                  decoration: const InputDecoration(
                    border: OutlineInputBorder(),
                    // contentPadding: EdgeInsets.symmetric(
                    //   horizontal: 8,
                    //   vertical: 8,
                    // ),
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

class _ToggleInput extends StatefulWidget {
  final ParameterModelToggle parameter;
  final ValueChanged<bool> onChanged;
  final ValueKey key;
  final bool initialValue;

  const _ToggleInput({
    required this.key,
    required this.initialValue,
    required this.parameter,
    required this.onChanged,
  });

  @override
  State<_ToggleInput> createState() => _ToggleInputState();
}

class _ToggleInputState extends State<_ToggleInput> {
  late bool _value = widget.parameter.initialValue;

  @override
  Widget build(BuildContext context) {
    return SwitchListTile(
      key: widget.key,
      title: Text(widget.parameter.title),
      value: _value,
      onChanged: (newValue) {
        widget.onChanged(newValue);

        _value = newValue;
        setState(() {});
      },
    );
  }
}
