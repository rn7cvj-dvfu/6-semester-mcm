import 'names.dart';
import 'router.dart';

final class AppNavigator {
  static void openLabs() => router.goNamed(RouteNames.labs);

  static void openLab(int labNumber) {
    if (labNumber < 1 || labNumber > 6) {
      throw ArgumentError("Lab number must be between 1 and 6");
    }
    router.pushReplacementNamed(labNumber.toString());
  }
}
