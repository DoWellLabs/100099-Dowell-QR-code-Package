import 'dart:io';

import 'package:dowell_image_qr_code/application/controllers/image_qr_code_controller/image_qr_code_controller.dart';
import 'package:dowell_image_qr_code/presentation/widgets/common/custom_snackbar.dart';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:get/get.dart';
import 'package:google_ml_kit/google_ml_kit.dart';
import 'package:image_picker/image_picker.dart';

import '../../domain/models/image_qr_code_model.dart';
import '../../routes/route_name.dart';

class CreatQRCodePage extends StatefulWidget {
  const CreatQRCodePage({Key? key}) : super(key: key);

  @override
  State<CreatQRCodePage> createState() => _CreatQRCodePageState();
}

class _CreatQRCodePageState extends State<CreatQRCodePage> {
  List qrcodeTypes = ["Link"];
  String selecteditems = "Link";
  File file = File("");

  final TextEditingController qrcodeColorController = TextEditingController();
  final TextEditingController linkController = TextEditingController();
  bool _isValidImage = false;

  String? _fileName;

  File? _selectedImage;
  String? _filePath;

  String? _message;

  @override
  Widget build(BuildContext context) {
    void createQRCode(QRCodeController qrCodeController) async {
      if (selecteditems.isEmpty) {
        showCustomSnackBar("QR Code Type is required", title: "QR Code Type");
      } else if (_selectedImage == null) {
        showCustomSnackBar("Please select an image", title: "Image");
      } else if (!_isValidImage) {
        showCustomSnackBar(
            "Please select a valid image that has a single human face",
            title: "Invalid Image");
      } else {
       
        ImageQRCodeRequestModel imageQRCodeRequestModel =
            ImageQRCodeRequestModel(
          qrcode_type: selecteditems,
          qrcode_color: qrcodeColorController.text,
          link: "http://dowell.com/qrcode_generator",
          company_id: "My Company",
          logo: _selectedImage,
          imagePath: _filePath != null ? "$_filePath#$_fileName" : null,
          quantity: 1,
        );

        var createResponse =
            await qrCodeController.createQrcode(imageQRCodeRequestModel);

        if (createResponse.success) {
          

          qrcodeColorController.clear();
          linkController.clear();

          var updateResponse =
              await qrCodeController.updateQrCode(qrCodeController.qrcode[0]);

          if (updateResponse.success) {
          

            showCustomSnackBar("Successfully Created QR Code",
                backgroundColor: Colors.white,
                textColor: Colors.black,
                isError: false,
                title: "Success");
            Get.toNamed(AppRoutes.QRCODEGENERATED);
          } else {
            
            showCustomSnackBar(updateResponse.message);
          }
        } else {
         
          showCustomSnackBar(createResponse.message);
        }
      }
    }

    Future<void> _processImage(String imagePath) async {
      final inputImage = InputImage.fromFilePath(imagePath);
      final faceDetector = GoogleMlKit.vision.faceDetector();
      final faces = await faceDetector.processImage(inputImage);

      try {
        if (faces.length != 1) {
          // No or more than one face detected

         
          setState(() {
            _isValidImage = false;
          });

          showCustomSnackBar('Please select an image with a single human face.',
              title: "Invalid Image: ");

          return;
        }

        // The image is valid with a single human face
        // Proceed with further operations

        setState(() {
          _isValidImage = true;
        });
      } catch (e) {
      
        setState(() {
          _isValidImage = false;
        });
      } finally {
        faceDetector.close();
      }
    }

    Future<void> _pickImage() async {
      final imagePicker = ImagePicker();
      final pickedImage =
          await imagePicker.pickImage(source: ImageSource.gallery);
      if (pickedImage != null) {
        setState(() {
          _selectedImage = File(pickedImage.path);
          _fileName = pickedImage.path.split("/").last;
          _message = _fileName;
          _filePath = pickedImage.path;
        });
        _processImage(pickedImage.path);
      } else {
        showCustomSnackBar('No image selected.');
      }
    }

    return Scaffold(
      body: GetBuilder<QRCodeController>(builder: (_controller) {
        return Obx(() {
          return Container(
            width: 390.w,
            height: 844.h,
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
                          EdgeInsetsDirectional.fromSTEB(10, 0, 10.w, 50.h),
                      child: Row(
                        mainAxisSize: MainAxisSize.max,
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          GestureDetector(
                            onTap: () {
                              Get.toNamed(AppRoutes.HOMEPAGE);
                            },
                            child: const Icon(
                              Icons.arrow_back,
                              color: Color(0xFF1C6012),
                              size: 30,
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
                  Expanded(
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          // dropdownButton
                          Container(
                            width: 350.w,
                            margin: EdgeInsets.only(bottom: 10.h),
                            padding: EdgeInsets.only(
                                left: 10.w,
                                right: 10.w,
                                top: 10.h,
                                bottom: 10.h),
                            decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(5.h)),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                const Text(
                                  'Select QR Code Type',
                                  style: TextStyle(
                                      fontFamily: 'RobotoMedium',
                                      color: Colors.black),
                                ),
                                SizedBox(
                                  height: 5.h,
                                ),
                                Container(
                                  decoration: BoxDecoration(
                                      border: Border.all(
                                          color: Colors.grey.withOpacity(0.5),
                                          width: 1),
                                      borderRadius: BorderRadius.circular(5.h)),
                                  padding:
                                      EdgeInsets.only(left: 10.w, right: 10.w),
                                  child: DropdownButtonFormField(
                                    decoration: const InputDecoration(
                                        border: InputBorder.none),
                                    icon: const Icon(Icons.arrow_drop_down),
                                    iconSize: 30.h,
                                    dropdownColor: Colors.white,
                                    isExpanded: true,
                                    style: TextStyle(
                                        color: Colors.black, fontSize: 16.sp),
                                    onChanged: (value) {
                                      selecteditems = value.toString();
                                      setState(() {
                                        selecteditems;
                                      });
                                    },
                                    // onSaved: (newValue) {
                                    //   selecteditems = newValue.toString();
                                    // },
                                    value: selecteditems,
                                    alignment: AlignmentDirectional.centerStart,
                                    hint: const Text(
                                      'Select QR Code Type',
                                      style: TextStyle(
                                          fontFamily: 'RobotoMedium',
                                          color: Colors.black),
                                    ),
                                    items: qrcodeTypes.map((item) {
                                      return DropdownMenuItem(
                                        value: item,
                                        child: Text(item),
                                      );
                                    }).toList(),
                                  ),
                                ),
                              ],
                            ),
                          ),

                          Container(
                            width: 350.w,
                            margin: EdgeInsets.only(
                                left: 10.w, right: 10.w, bottom: 10.h),
                            padding: EdgeInsets.only(
                                left: 10.w,
                                right: 10.w,
                                top: 10.h,
                                bottom: 10.h),
                            decoration: BoxDecoration(
                                color: Colors.white,
                                borderRadius: BorderRadius.circular(5.h)),
                            child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    children: [
                                      const Text(
                                        "Pick Image",
                                        style: TextStyle(
                                            fontFamily: 'RobotoMedium',
                                            color: Colors.black),
                                      ),
                                      SizedBox(
                                        width: 5.w,
                                      ),
                                      Text(
                                          "(The Image should contain a single human face)",
                                          style: TextStyle(
                                            fontFamily: 'RobotoRegular',
                                            color: Colors.red,
                                            fontWeight: FontWeight.bold,
                                            fontSize: 10.sp,
                                          )),
                                    ],
                                  ),
                                  Container(
                                    width: 350.w,
                                    margin: EdgeInsets.only(
                                        bottom: 10.h, top: 10.h),
                                    decoration: BoxDecoration(
                                        color: Colors.white,
                                        border: Border.all(
                                          color: Colors.grey.withOpacity(0.5),
                                          width: 1,
                                        ),
                                        borderRadius:
                                            BorderRadius.circular(5.h)),
                                    child: TextButton(
                                      onPressed: () {
                                        _pickImage();
                                      },
                                      child: Row(
                                        mainAxisAlignment:
                                            MainAxisAlignment.start,
                                        children: [
                                          Icon(
                                            Icons.upload_file,
                                            color: Colors.black,
                                            size: 30.h,
                                          ),
                                          SizedBox(
                                            width: 5.w,
                                          ),
                                          const Text(
                                            "Pick Image",
                                            style: TextStyle(
                                                fontFamily: 'RobotoRegular',
                                                color: Colors.black),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ),
                                  if (_selectedImage != null)
                                    Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.center,
                                      children: [
                                        Container(
                                            padding: EdgeInsets.only(
                                                left: 20, right: 20),
                                            width: 300.w,
                                            height: 300.w,
                                            child: Center(
                                                child: Image.file(
                                              _selectedImage!,
                                              fit: BoxFit.cover,
                                            ))),
                                      ],
                                    ),
                                  Text(
                                    _message ?? 'No File Selected',
                                    style: const TextStyle(
                                        fontFamily: 'RobotoRegular',
                                        color: Colors.black),
                                  ),
                                ]),
                          ),

                          // reusableTextField(
                          //   hintText: 'Enter link',
                          //   label: 'Link',
                          //   textEditingController: linkController,
                          // ),

                          // reusableTextField(
                          //   hintText: 'Enter QR Code Color',
                          //   label: 'QR Code Color',
                          //   textEditingController: qrcodeColorController,
                          // ),
                          GestureDetector(
                            onTap: () {
                              createQRCode(_controller);
                            },
                            child: Container(
                              width: 350.w,
                              height: 55.h,
                              margin: EdgeInsets.only(
                                  top: 10.h,
                                  left: 10.w,
                                  right: 10.w,
                                  bottom: 30.h),
                              decoration: BoxDecoration(
                                color: const Color(0xFF4B39EF),
                                borderRadius: BorderRadius.circular(5.h),
                              ),
                              child: Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                crossAxisAlignment: CrossAxisAlignment.center,
                                children: [
                                  _controller.isLoading.value
                                      ? const CircularProgressIndicator()
                                      : const Text(
                                          'Generate QR Code',
                                          style: TextStyle(
                                            fontFamily: 'RobotoMedium',
                                            color: Colors.white,
                                          ),
                                        ),
                                ],
                              ),
                            ),
                          ),
                        ],
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
