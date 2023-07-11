import 'package:dowell_image_qr_code/presentation/create_qr_code_page/create_qr_code_page.dart';
import 'package:dowell_image_qr_code/presentation/qr_generated_page/qr_generated_page.dart';
import 'package:dowell_image_qr_code/presentation/homepage/homepage.dart';
import 'package:dowell_image_qr_code/presentation/welcome/welcome_index.dart';

import 'package:dowell_image_qr_code/routes/route_name.dart';
import 'package:dowell_image_qr_code/routes/routes_observers.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

class AppPages {
  static const SPLASH = AppRoutes.SPLASH;
  static final RouteObserver<Route> observer = RouteObservers();
  static List<String> history = [];
  static final List<GetPage> routes = [
    GetPage(
        name: AppRoutes.SPLASH,
        page: () => WelcomePage(),
        transition: Transition.fadeIn,
        binding: WelcomeBinding()),
    GetPage(
        name: AppRoutes.HOMEPAGE,
        page: () => const HomePage(),
        transition: Transition.fadeIn),
    GetPage(
        name: AppRoutes.CREATEQRCODE,
        page: () => const CreatQRCodePage(),
        transition: Transition.fadeIn),
    GetPage(
        name: AppRoutes.QRCODEGENERATED,
        page: () => const QrCodeGeneratedPage(),
        transition: Transition.fadeIn),
  ];
}
