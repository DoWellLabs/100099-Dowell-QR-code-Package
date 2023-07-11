import 'package:dowell_image_qr_code/presentation/welcome/welcome_controller.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

class WelcomePage extends GetView<WelcomeController> {
  const WelcomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // backgroundColor: FlutterFlowTheme.of(context).primaryBackground,
      body: Container(
        width: MediaQuery.of(context).size.width,
        height: MediaQuery.of(context).size.height * 1,
        decoration: const BoxDecoration(
           gradient: LinearGradient(
            colors: [Color(0xFF39D2C0), Color(0xFF95E1D6)],
            stops: [0, 1],
            begin: AlignmentDirectional(0, -1),
            end: AlignmentDirectional(0, 1),
          ),
        ),
        child: Stack(
          children: [
            Align(
              alignment: Alignment.center,
              child: Padding(
                padding: const EdgeInsets.only(bottom: 55),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(8.h),
                  child: Image.asset(
                    'assets/images/dowell_logo_image.png',
                    width: 200.w,
                    fit: BoxFit.cover,
                  ),
                ),
              ),
            ),
            Positioned(
              top: 470.h,
              left: 100.w,
              child: Text(
                controller.logotitle1,
                style: TextStyle(
                  fontFamily: 'RobotoMedium',
                  color: const Color(0xFFBFBDBD),
                  fontSize: 30.sp,
                  //fontWeight: FontWeight.bold,
                ),
              ),
            ),
            Positioned(
              top: 505.h,
              left: 100.w,
              child: Text(
                controller.logotitle2,
                style: TextStyle(
                  fontFamily: 'RobotoMedium',
                  color: const Color(0xFF153310),
                  fontSize: 30.sp,
                  // fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
      ),
    );
    ;
  }
}
