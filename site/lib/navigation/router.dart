import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import '../pages/labs.dart';
import '../pages/labs/1.dart';
import 'names.dart';

final GlobalKey<NavigatorState> rootNavigatorKey = GlobalKey<NavigatorState>();

GoRouter router = GoRouter(
  initialLocation: RouteNames.labs,
  routerNeglect: true,
  navigatorKey: rootNavigatorKey,
  routes: [
    GoRoute(
      name: RouteNames.labs,
      path: RouteNames.labs,
      builder: (context, state) => LabsPage(),
      routes: [
        GoRoute(
          name: RouteNames.first,
          path: RouteNames.first,
          builder: (context, state) => const Lab1(),
        )
      ],
    ),
  ],
);
