import 'package:freezed_annotation/freezed_annotation.dart';

@freezed
class ParameterModel with _$ParameterModel {
  factory ParameterModel.value() = _ParameterModelValue;
  factory ParameterModel.toggle() = _ParameterModelToggle;
}
