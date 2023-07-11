import 'dart:io';

import 'package:dowell_image_qr_code/application/controllers/image_qr_code_controller/image_qr_code_controller.dart';
import 'package:dowell_image_qr_code/domain/models/image_qr_code_model.dart';
import 'package:dowell_image_qr_code/infrastructure/api/api_end_points.dart';
import 'package:dowell_image_qr_code/presentation/widgets/common/custom_snackbar.dart';
import 'package:dowell_image_qr_code/routes/route_name.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:path_provider/path_provider.dart';

class QrCodeGeneratedPage extends StatefulWidget {
  const QrCodeGeneratedPage({Key? key}) : super(key: key);

  @override
  _QrCodeGeneratedPageState createState() => _QrCodeGeneratedPageState();
}

class _QrCodeGeneratedPageState extends State<QrCodeGeneratedPage> {
  void handleSharing(
    QRCodeController controller,
  ) async {
    print("Sharing");
    Directory directory = await getApplicationDocumentsDirectory();
    String filePath = directory.path;
    var response = await controller.shareQRCode(
        controller.qrcode[0].qrcodeImageUrl!.split("/").last,
        "${filePath}qrcode_image.${controller.qrcode[0].qrcodeImageUrl!.split("/").last.split(".").last}");
    print("response.success is ${response.success}");
    if (response.success) {
      showCustomSnackBar(response.message,
          backgroundColor: Colors.white,
          textColor: Colors.black,
          isError: false,
          title: "Success");
    } else {
      showCustomSnackBar(response.message);
    }
  }

  void handleDownloading(QRCodeController controller) async {
    print("downloading");

    Directory directory = await getApplicationDocumentsDirectory();
    String filePath = directory.path;
    var response = await controller.downloadQRCode(
        controller.qrcode[0].qrcodeImageUrl!.split("/").last,
        "${filePath}qrcode_image.${controller.qrcode[0].qrcodeImageUrl!.split("/").last.split(".").last}");
    print("response.success is : ${response.success}");
    if (response.success) {
      showCustomSnackBar(response.message,
          backgroundColor: Colors.white,
          textColor: Colors.black,
          isError: false,
          title: "Success");
    } else {
      showCustomSnackBar(response.message);
    }
  }

  void handleUpdate(QRCodeController qrCodeController) async {
    print("updating");
    var response =
        await qrCodeController.updateQrCode(qrCodeController.qrcode[0]);
    if (response.success) {
      showCustomSnackBar(response.message,
          backgroundColor: Colors.white,
          textColor: Colors.black,
          isError: false,
          title: "Success");
    } else {
      showCustomSnackBar(response.message);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: GetBuilder<QRCodeController>(builder: (_controller) {
        Qrcodes qrcode = _controller.qrcode[0];

        return Obx(() {
          return Container(
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
                      padding:
                          EdgeInsetsDirectional.fromSTEB(10.w, 0, 10.w, 30.h),
                      child: Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Get.toNamed(AppRoutes.CREATEQRCODE);
                            },
                            child: Icon(
                              Icons.arrow_back,
                              color: const Color(0xFF1C6012),
                              size: 30.h,
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
                  Text(
                    'Successfully Generated QR\n Code for your image',
                    style: TextStyle(
                      fontFamily: 'RobotoMedium',
                      color: Colors.black,
                      fontSize: 20.sp,
                    ),
                  ),
                  Padding(
                    padding: EdgeInsetsDirectional.fromSTEB(0, 20.h, 0, 0),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(15.h),
                      child: Image.network(
                        ApiEndPoints.DOWNLOAD_QR_CODE_BASE_URL +
                            qrcode.qrcodeImageUrl!.split("/").last,
                        width: 300.w,
                        height: 300.w,
                        fit: BoxFit.cover,
                        loadingBuilder: (context, child, loadingProgress) {
                          if (loadingProgress == null) return child;
                          return Center(
                            child: Container(
                              width: 300.w,
                              height: 300.w,
                              decoration: BoxDecoration(
                                color: Colors.grey.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(15.h),
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                  ),
                  GestureDetector(
                    onTap: () {
                      handleDownloading(_controller);
                    },
                    child: Align(
                      alignment: const AlignmentDirectional(-1, 0),
                      child: Padding(
                        padding: EdgeInsetsDirectional.fromSTEB(
                            40.w, 50.h, 40.w, 20.h),
                        child: Container(
                          width: MediaQuery.of(context).size.width,
                          height: 55.h,
                          decoration: BoxDecoration(
                            color: const Color(0xFF4B39EF),
                            borderRadius: BorderRadius.circular(5.h),
                          ),
                          child: Align(
                            alignment: const AlignmentDirectional(0, 0),
                            child: Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                _controller.isDownloading.value
                                    ? const CircularProgressIndicator(
                                        color: Colors.white,
                                      )
                                    : Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.center,
                                        children: [
                                          Icon(
                                            Icons.download,
                                            color: Colors.white,
                                            size: 24.sp,
                                          ),
                                          SizedBox(
                                            width: 5.w,
                                          ),
                                          const Text(
                                            'Download QR Code',
                                            style: TextStyle(
                                              fontFamily: 'RobotoMedium',
                                              color: Colors.white,
                                            ),
                                          ),
                                        ],
                                      ),
                              ],
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                  GestureDetector(
                    onTap: () {
                      handleSharing(_controller);
                    },
                    child: Align(
                      alignment: const AlignmentDirectional(-1, 0),
                      child: Padding(
                        padding:
                            EdgeInsetsDirectional.fromSTEB(40.w, 0, 40.w, 20.h),
                        child: Container(
                          width: MediaQuery.of(context).size.width,
                          height: 55.h,
                          decoration: BoxDecoration(
                            color: const Color(0xFF4B39EF),
                            borderRadius: BorderRadius.circular(5.h),
                          ),
                          child: Align(
                            alignment: const AlignmentDirectional(0, 0),
                            child: _controller.isSharing.value
                                ? const CircularProgressIndicator(
                                    color: Colors.white,
                                  )
                                : Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        Icons.share,
                                        color: Colors.white,
                                        size: 24.sp,
                                      ),
                                      SizedBox(
                                        width: 5.w,
                                      ),
                                      const Text(
                                        'Share QR Code',
                                        style: TextStyle(
                                          fontFamily: 'RobotoMedium',
                                          color: Colors.white,
                                        ),
                                      ),
                                    ],
                                  ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        });
      }),
    );
  }
}
