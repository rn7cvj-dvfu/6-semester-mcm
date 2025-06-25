// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of '../../../../core/ui/parameters/model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models');

/// @nodoc
mixin _$ParameterModel {
  String get key => throw _privateConstructorUsedError;
  String get title => throw _privateConstructorUsedError;
  Object get initialValue => throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)
        value,
    required TResult Function(String title, String key, bool initialValue)
        toggle,
  }) =>
      throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)?
        value,
    TResult? Function(String title, String key, bool initialValue)? toggle,
  }) =>
      throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)?
        value,
    TResult Function(String title, String key, bool initialValue)? toggle,
    required TResult orElse(),
  }) =>
      throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(ParameterModelValue value) value,
    required TResult Function(ParameterModelToggle value) toggle,
  }) =>
      throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(ParameterModelValue value)? value,
    TResult? Function(ParameterModelToggle value)? toggle,
  }) =>
      throw _privateConstructorUsedError;
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(ParameterModelValue value)? value,
    TResult Function(ParameterModelToggle value)? toggle,
    required TResult orElse(),
  }) =>
      throw _privateConstructorUsedError;

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $ParameterModelCopyWith<ParameterModel> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $ParameterModelCopyWith<$Res> {
  factory $ParameterModelCopyWith(
          ParameterModel value, $Res Function(ParameterModel) then) =
      _$ParameterModelCopyWithImpl<$Res, ParameterModel>;
  @useResult
  $Res call({String key, String title});
}

/// @nodoc
class _$ParameterModelCopyWithImpl<$Res, $Val extends ParameterModel>
    implements $ParameterModelCopyWith<$Res> {
  _$ParameterModelCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? key = null,
    Object? title = null,
  }) {
    return _then(_value.copyWith(
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$ParameterModelValueImplCopyWith<$Res>
    implements $ParameterModelCopyWith<$Res> {
  factory _$$ParameterModelValueImplCopyWith(_$ParameterModelValueImpl value,
          $Res Function(_$ParameterModelValueImpl) then) =
      __$$ParameterModelValueImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String key,
      String title,
      String? unit,
      double initialValue,
      double minValue,
      double maxValue,
      int? stepCount});
}

/// @nodoc
class __$$ParameterModelValueImplCopyWithImpl<$Res>
    extends _$ParameterModelCopyWithImpl<$Res, _$ParameterModelValueImpl>
    implements _$$ParameterModelValueImplCopyWith<$Res> {
  __$$ParameterModelValueImplCopyWithImpl(_$ParameterModelValueImpl _value,
      $Res Function(_$ParameterModelValueImpl) _then)
      : super(_value, _then);

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? key = null,
    Object? title = null,
    Object? unit = freezed,
    Object? initialValue = null,
    Object? minValue = null,
    Object? maxValue = null,
    Object? stepCount = freezed,
  }) {
    return _then(_$ParameterModelValueImpl(
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      unit: freezed == unit
          ? _value.unit
          : unit // ignore: cast_nullable_to_non_nullable
              as String?,
      initialValue: null == initialValue
          ? _value.initialValue
          : initialValue // ignore: cast_nullable_to_non_nullable
              as double,
      minValue: null == minValue
          ? _value.minValue
          : minValue // ignore: cast_nullable_to_non_nullable
              as double,
      maxValue: null == maxValue
          ? _value.maxValue
          : maxValue // ignore: cast_nullable_to_non_nullable
              as double,
      stepCount: freezed == stepCount
          ? _value.stepCount
          : stepCount // ignore: cast_nullable_to_non_nullable
              as int?,
    ));
  }
}

/// @nodoc

class _$ParameterModelValueImpl implements ParameterModelValue {
  _$ParameterModelValueImpl(
      {required this.key,
      required this.title,
      this.unit,
      required this.initialValue,
      required this.minValue,
      required this.maxValue,
      this.stepCount});

  @override
  final String key;
  @override
  final String title;
  @override
  final String? unit;
  @override
  final double initialValue;
  @override
  final double minValue;
  @override
  final double maxValue;
  @override
  final int? stepCount;

  @override
  String toString() {
    return 'ParameterModel.value(key: $key, title: $title, unit: $unit, initialValue: $initialValue, minValue: $minValue, maxValue: $maxValue, stepCount: $stepCount)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ParameterModelValueImpl &&
            (identical(other.key, key) || other.key == key) &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.unit, unit) || other.unit == unit) &&
            (identical(other.initialValue, initialValue) ||
                other.initialValue == initialValue) &&
            (identical(other.minValue, minValue) ||
                other.minValue == minValue) &&
            (identical(other.maxValue, maxValue) ||
                other.maxValue == maxValue) &&
            (identical(other.stepCount, stepCount) ||
                other.stepCount == stepCount));
  }

  @override
  int get hashCode => Object.hash(runtimeType, key, title, unit, initialValue,
      minValue, maxValue, stepCount);

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ParameterModelValueImplCopyWith<_$ParameterModelValueImpl> get copyWith =>
      __$$ParameterModelValueImplCopyWithImpl<_$ParameterModelValueImpl>(
          this, _$identity);

  @override
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)
        value,
    required TResult Function(String title, String key, bool initialValue)
        toggle,
  }) {
    return value(key, title, unit, initialValue, minValue, maxValue, stepCount);
  }

  @override
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)?
        value,
    TResult? Function(String title, String key, bool initialValue)? toggle,
  }) {
    return value?.call(
        key, title, unit, initialValue, minValue, maxValue, stepCount);
  }

  @override
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)?
        value,
    TResult Function(String title, String key, bool initialValue)? toggle,
    required TResult orElse(),
  }) {
    if (value != null) {
      return value(
          key, title, unit, initialValue, minValue, maxValue, stepCount);
    }
    return orElse();
  }

  @override
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(ParameterModelValue value) value,
    required TResult Function(ParameterModelToggle value) toggle,
  }) {
    return value(this);
  }

  @override
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(ParameterModelValue value)? value,
    TResult? Function(ParameterModelToggle value)? toggle,
  }) {
    return value?.call(this);
  }

  @override
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(ParameterModelValue value)? value,
    TResult Function(ParameterModelToggle value)? toggle,
    required TResult orElse(),
  }) {
    if (value != null) {
      return value(this);
    }
    return orElse();
  }
}

abstract class ParameterModelValue implements ParameterModel {
  factory ParameterModelValue(
      {required final String key,
      required final String title,
      final String? unit,
      required final double initialValue,
      required final double minValue,
      required final double maxValue,
      final int? stepCount}) = _$ParameterModelValueImpl;

  @override
  String get key;
  @override
  String get title;
  String? get unit;
  @override
  double get initialValue;
  double get minValue;
  double get maxValue;
  int? get stepCount;

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ParameterModelValueImplCopyWith<_$ParameterModelValueImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class _$$ParameterModelToggleImplCopyWith<$Res>
    implements $ParameterModelCopyWith<$Res> {
  factory _$$ParameterModelToggleImplCopyWith(_$ParameterModelToggleImpl value,
          $Res Function(_$ParameterModelToggleImpl) then) =
      __$$ParameterModelToggleImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({String title, String key, bool initialValue});
}

/// @nodoc
class __$$ParameterModelToggleImplCopyWithImpl<$Res>
    extends _$ParameterModelCopyWithImpl<$Res, _$ParameterModelToggleImpl>
    implements _$$ParameterModelToggleImplCopyWith<$Res> {
  __$$ParameterModelToggleImplCopyWithImpl(_$ParameterModelToggleImpl _value,
      $Res Function(_$ParameterModelToggleImpl) _then)
      : super(_value, _then);

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? title = null,
    Object? key = null,
    Object? initialValue = null,
  }) {
    return _then(_$ParameterModelToggleImpl(
      title: null == title
          ? _value.title
          : title // ignore: cast_nullable_to_non_nullable
              as String,
      key: null == key
          ? _value.key
          : key // ignore: cast_nullable_to_non_nullable
              as String,
      initialValue: null == initialValue
          ? _value.initialValue
          : initialValue // ignore: cast_nullable_to_non_nullable
              as bool,
    ));
  }
}

/// @nodoc

class _$ParameterModelToggleImpl implements ParameterModelToggle {
  _$ParameterModelToggleImpl(
      {required this.title, required this.key, this.initialValue = true});

  @override
  final String title;
  @override
  final String key;
  @override
  @JsonKey()
  final bool initialValue;

  @override
  String toString() {
    return 'ParameterModel.toggle(title: $title, key: $key, initialValue: $initialValue)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$ParameterModelToggleImpl &&
            (identical(other.title, title) || other.title == title) &&
            (identical(other.key, key) || other.key == key) &&
            (identical(other.initialValue, initialValue) ||
                other.initialValue == initialValue));
  }

  @override
  int get hashCode => Object.hash(runtimeType, title, key, initialValue);

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$ParameterModelToggleImplCopyWith<_$ParameterModelToggleImpl>
      get copyWith =>
          __$$ParameterModelToggleImplCopyWithImpl<_$ParameterModelToggleImpl>(
              this, _$identity);

  @override
  @optionalTypeArgs
  TResult when<TResult extends Object?>({
    required TResult Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)
        value,
    required TResult Function(String title, String key, bool initialValue)
        toggle,
  }) {
    return toggle(title, key, initialValue);
  }

  @override
  @optionalTypeArgs
  TResult? whenOrNull<TResult extends Object?>({
    TResult? Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)?
        value,
    TResult? Function(String title, String key, bool initialValue)? toggle,
  }) {
    return toggle?.call(title, key, initialValue);
  }

  @override
  @optionalTypeArgs
  TResult maybeWhen<TResult extends Object?>({
    TResult Function(
            String key,
            String title,
            String? unit,
            double initialValue,
            double minValue,
            double maxValue,
            int? stepCount)?
        value,
    TResult Function(String title, String key, bool initialValue)? toggle,
    required TResult orElse(),
  }) {
    if (toggle != null) {
      return toggle(title, key, initialValue);
    }
    return orElse();
  }

  @override
  @optionalTypeArgs
  TResult map<TResult extends Object?>({
    required TResult Function(ParameterModelValue value) value,
    required TResult Function(ParameterModelToggle value) toggle,
  }) {
    return toggle(this);
  }

  @override
  @optionalTypeArgs
  TResult? mapOrNull<TResult extends Object?>({
    TResult? Function(ParameterModelValue value)? value,
    TResult? Function(ParameterModelToggle value)? toggle,
  }) {
    return toggle?.call(this);
  }

  @override
  @optionalTypeArgs
  TResult maybeMap<TResult extends Object?>({
    TResult Function(ParameterModelValue value)? value,
    TResult Function(ParameterModelToggle value)? toggle,
    required TResult orElse(),
  }) {
    if (toggle != null) {
      return toggle(this);
    }
    return orElse();
  }
}

abstract class ParameterModelToggle implements ParameterModel {
  factory ParameterModelToggle(
      {required final String title,
      required final String key,
      final bool initialValue}) = _$ParameterModelToggleImpl;

  @override
  String get title;
  @override
  String get key;
  @override
  bool get initialValue;

  /// Create a copy of ParameterModel
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$ParameterModelToggleImplCopyWith<_$ParameterModelToggleImpl>
      get copyWith => throw _privateConstructorUsedError;
}
