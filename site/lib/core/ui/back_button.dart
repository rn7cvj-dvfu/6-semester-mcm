import 'package:flutter/material.dart';

import '../settings.dart';

class AppBackButton extends StatelessWidget {
  final VoidCallback onTap;

  const AppBackButton({super.key, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(AppUISettings.defaultPadding),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.arrow_back_ios_new),
              const SizedBox(width: 8.0),
              Text(
                "Назад",
                style: Theme.of(context).textTheme.titleMedium,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
