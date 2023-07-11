import 'package:dowell_image_qr_code/routes/route_name.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
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
        child: Padding(
          padding: EdgeInsetsDirectional.fromSTEB(0, 40.h, 0, 0),
          child: Column(
            mainAxisSize: MainAxisSize.max,
            children: [
              Align(
                alignment: const AlignmentDirectional(0, 0),
                child: Padding(
                  padding: EdgeInsetsDirectional.fromSTEB(10.w, 0, 10.w, 50.h),
                  child: Row(
                    mainAxisSize: MainAxisSize.max,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    crossAxisAlignment: CrossAxisAlignment.center,
                    children: [
                      Text(
                        'Create Image QR Code',
                        style: TextStyle(
                          fontFamily: 'RobotoRegular',
                          color: Colors.black,
                          fontSize: 20.sp,
                          fontWeight: FontWeight.normal,
                        ),
                      ),
                      ClipRRect(
                        borderRadius: BorderRadius.circular(8.h),
                        child: Image.asset(
                          'assets/images/dowell_logo_image.png',
                          height: 60.h,
                          fit: BoxFit.cover,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.only(left: 40.w, right: 40.w),
                child: Text(
                  'Share your image in a secure way',
                  style: TextStyle(
                      color: Color.fromARGB(255, 26, 25, 25),
                      fontFamily: "RobotoMedium",
                      fontWeight: FontWeight.normal,
                      fontSize: 30.h),
                ),
              ),
              Align(
                alignment: const AlignmentDirectional(-1, 0),
                child: Padding(
                  padding: EdgeInsetsDirectional.fromSTEB(10.w, 25.h, 10.w, 0),
                  child: Row(
                    mainAxisSize: MainAxisSize.max,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(0, 0, 10.w, 0),
                        child: Icon(
                          Icons.arrow_right_outlined,
                          color: const Color(0xFF153310),
                          size: 40.h,
                        ),
                      ),
                      Column(
                        mainAxisSize: MainAxisSize.max,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Create QR Code for ',
                            style: TextStyle(
                                fontFamily: "RobotoMedium", fontSize: 16.sp),
                          ),
                          Text(
                            'your image',
                            style: TextStyle(
                                fontFamily: "RobotoMedium", fontSize: 16.sp),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsetsDirectional.fromSTEB(10.w, 20.h, 10.w, 0),
                child: Row(
                  mainAxisSize: MainAxisSize.max,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: EdgeInsetsDirectional.fromSTEB(0, 0, 10.w, 0),
                      child: Icon(
                        Icons.arrow_right_outlined,
                        color: const Color(0xFF153310),
                        size: 40.h,
                      ),
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.max,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Share QR Code of ',
                          style: TextStyle(
                              fontFamily: "RobotoMedium", fontSize: 16.sp),
                        ),
                        Text(
                          'your image with your friends',
                          style: TextStyle(
                              fontFamily: "RobotoMedium", fontSize: 16.sp),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Padding(
                padding: EdgeInsetsDirectional.fromSTEB(10.w, 20.h, 10.w, 0.h),
                child: Row(
                  mainAxisSize: MainAxisSize.max,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding:
                          EdgeInsetsDirectional.fromSTEB(0.w, 0.h, 10.w, 0.h),
                      child: Icon(
                        Icons.arrow_right_outlined,
                        color: const Color(0xFF153310),
                        size: 40.h,
                      ),
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.max,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Scan QR Code of the image',
                          style: TextStyle(
                              fontFamily: "RobotoMedium", fontSize: 16.sp),
                        ),
                        Text(
                          'to get the image',
                          style: TextStyle(
                              fontFamily: "RobotoMedium", fontSize: 16.sp),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Align(
                alignment: const AlignmentDirectional(-1, 0),
                child: GestureDetector(
                  onTap: () {
                    Get.toNamed(AppRoutes.CREATEQRCODE);
                  },
                  child: Padding(
                    padding:
                        EdgeInsetsDirectional.fromSTEB(20.w, 100.h, 20.w, 0.h),
                    child: Container(
                      width: 350.w,
                      height: 55.h,
                      decoration: BoxDecoration(
                        color: Color(0xFF4B39EF),
                        borderRadius: BorderRadius.circular(10.h),
                      ),
                      child: Align(
                        alignment: const AlignmentDirectional(0, 0),
                        child: Text(
                          'Create QR Code',
                          style: TextStyle(
                            fontFamily: 'RobotoMedium',
                            color: Colors.white,
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
