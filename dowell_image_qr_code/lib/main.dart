import 'package:dowell_image_qr_code/routes/route_name.dart';
import 'package:dowell_image_qr_code/routes/route_pages.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

import 'dependency/dependency.dart' as dependency;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await dependency.init();

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});


  @override
  Widget build(BuildContext context) {
    return ScreenUtilInit(
      designSize: const Size(390, 844),
      builder: (BuildContext context, Widget? child) {
        return GetMaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'Dowell Image QR Code',
          initialRoute: AppRoutes.SPLASH,
          getPages: AppPages.routes,
        );
      },
    );
  }
}
