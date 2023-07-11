import 'package:flutter/material.dart';
import 'package:get/get.dart';

void showCustomSnackBar(String message,
    {bool isError = true,
    String title = "Error",
    Color backgroundColor = Colors.redAccent,
    Color textColor = Colors.white}) {
  Get.snackbar(
    title,
    message,
    duration: const Duration(seconds: 5),
    titleText: Text(
      title,
      style: TextStyle(color: textColor, overflow: TextOverflow.ellipsis),
    ),
    messageText: Text(
      message,
      style: TextStyle(color: textColor, overflow: TextOverflow.ellipsis),
    ),
    colorText: Colors.white,
    snackPosition: SnackPosition.TOP,
    backgroundColor: backgroundColor,
  );
}
