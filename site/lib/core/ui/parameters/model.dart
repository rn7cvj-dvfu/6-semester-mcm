import 'package:freezed_annotation/freezed_annotation.dart';

part '../../../.gen/core/ui/parameters/model.freezed.dart';

@freezed
class ParameterModel with _$ParameterModel {
  factory ParameterModel.value({
    required String key,
    required String title,
    String? unit,
    required double initialValue,
    required double minValue,
    required double maxValue,
    int? stepCount,
  }) = ParameterModelValue;

  factory ParameterModel.toggle({
    required String title,
    required String key,
    @Default(true) bool initialValue,
  }) = ParameterModelToggle;
}
