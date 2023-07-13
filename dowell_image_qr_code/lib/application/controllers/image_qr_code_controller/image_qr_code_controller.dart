import 'package:dio/dio.dart';
import 'package:dowell_image_qr_code/domain/models/api_response_model.dart';
import 'package:dowell_image_qr_code/domain/models/image_qr_code_model.dart';
import 'package:dowell_image_qr_code/infrastructure/api/api_end_points.dart';
import 'package:dowell_image_qr_code/infrastructure/api/api_exceptions.dart';
import 'package:flutter/foundation.dart';
import 'package:get/get.dart';
import 'package:share_plus/share_plus.dart';

import '../../../infrastructure/repositories/image_qr_code_repo/image_qr_code_repo.dart';

class QRCodeController extends GetxController {
  final ImageQRCodeRepository imageQRCodeRepository;

  QRCodeController({required this.imageQRCodeRepository});

  final _qrCodes = <Qrcodes>[].obs;
  final _updatedQrCodes = <Qrcodes>[].obs;

  List<Qrcodes> get updatedQrcode => _updatedQrCodes;

  List<Qrcodes> get qrcode => _qrCodes;

  RxBool _isSuccess = false.obs;
  RxBool get isSuccess => _isSuccess;

  RxBool _isLoading = false.obs;
  RxBool _isDownloading = false.obs;
  RxBool _isSharing = false.obs;
  RxBool get isSharing => _isSharing;
  RxBool get isDownloading => _isDownloading;
  RxBool get isLoading => _isLoading;

  Future<APIResponseModel> createQrcode(
      ImageQRCodeRequestModel qrCodeRequestModel) async {
    _isLoading.value = true;
    try {
      var response = await imageQRCodeRepository.createQRCode(
          qrCodeRequestModel,
          queryParameters: {'api_key': ApiEndPoints.API_KEY});

      if (response.statusCode == 201) {
        if (response.data["qrcodes"] != null) {
          _qrCodes.clear();
          response.data["qrcodes"].forEach((qrcode) {
            _qrCodes.add(Qrcodes.fromJson(qrcode));
          });

          return APIResponseModel(
              success: true, message: "Successfully Created QR Code");
        }

        // _qrCodes.add(Qrcodes.fromJson(response.data));
        _isLoading.value = false;
        return APIResponseModel(
            success: false, message: "Erro Creating QR Code");
      } else {
        _isSuccess.value = false;

        isLoading.value = false;
        return APIResponseModel(
            success: false,
            message: response.statusMessage ?? "Error creating QRCode");
      }
    } on DioException catch (e) {
      var error = ApiException.fromDioError(e);
      _isLoading.value = false;
      return APIResponseModel(success: false, message: error.errorMessage);
    }
  }

  Future<APIResponseModel> getQrCodes(
      Map<String, dynamic>? queryParameters) async {
    try {
      var response = await imageQRCodeRepository.getQRCode(
          queryParameters: queryParameters);

      if (response.statusCode == 200) {
        if (kDebugMode) {
          print("success");
        }

        return APIResponseModel(
            success: true, message: "Successfully Got QR Code");
      } else {
        return APIResponseModel(
            success: false,
            message: response.statusMessage ?? "Error Getting QRCode");
      }
    } on DioException catch (e) {
      var error = ApiException.fromDioError(e);

      return APIResponseModel(success: false, message: error.errorMessage);
    }
  }

  // update qrcode by id
  Future<APIResponseModel> updateQrCode(Qrcodes qrcode) async {
    _isLoading.value = true;
    try {
      var response = await imageQRCodeRepository.updateQRCode(qrcode,
          queryParameters: {'api_key': ApiEndPoints.API_KEY});

      if (response.statusCode == 200) {
        _qrCodes.clear();

        if (response.data["response"] != null) {
          var qrCode = response.data["response"];

          _qrCodes.add(Qrcodes.fromJson(qrCode));

          _isLoading.value = false;

          _isSuccess.value = true;
          return APIResponseModel(
              success: true, message: "Successfully Updated QR Code");
        }
        _isLoading.value = false;

        return APIResponseModel(
            success: false, message: "Error Updating QR Code");
      } else {
        _isSuccess.value = false;

        _isLoading.value = false;
        return APIResponseModel(
            success: false,
            message: response.statusMessage ?? "Error Updating QRCode");
      }
    } on DioException catch (e) {
      _isLoading.value = false;
      var error = ApiException.fromDioError(e);
      return APIResponseModel(success: false, message: error.errorMessage);
    }
  }

  Future<APIResponseModel> downloadQRCode(
      String qrcodeName, String filePath) async {
    _isSuccess.value = false;
    _isDownloading.value = true;
    try {
      var response =
          await imageQRCodeRepository.downloadQRCode(qrcodeName, filePath);

      if (response.statusCode == 200) {
        _isSuccess.value = true;
        _isDownloading.value = false;

        return APIResponseModel(
            success: true, message: "Successfully Downloaded QR Code");
      } else {
        _isDownloading.value = false;
        return APIResponseModel(
            success: false,
            message: response.statusMessage ?? "Error Downloading QRCode");
      }
    } on DioException catch (e) {
      _isDownloading.value = false;
      var error = ApiException.fromDioError(e);
      return APIResponseModel(success: false, message: error.errorMessage);
    }
  }

  Future<APIResponseModel> shareQRCode(
      String qrcodeName, String filePath) async {
    _isSuccess.value = false;
    _isSharing.value = true;
    try {
      var response =
          await imageQRCodeRepository.downloadQRCode(qrcodeName, filePath);

      if (response.statusCode == 200) {
        _isSuccess.value = true;
        var shareResult = await Share.shareXFiles(
          [XFile(filePath)],
          text: 'QR Code Image',
        );
        if (shareResult.status == ShareResultStatus.success) {
          _isSharing.value = false;

          return APIResponseModel(
              success: true, message: "Successfully Shared QR Code");
        } else {
          _isSharing.value = false;
          return APIResponseModel(
              success: false,
              message: response.statusMessage ?? "Error Sharing QRCode");
        }
      } else {
        _isSharing.value = false;
        return APIResponseModel(
            success: false,
            message: response.statusMessage ?? "Error Sharing QRCode");
      }
    } on DioException catch (e) {
      _isSharing.value = false;

      var error = ApiException.fromDioError(e);
      return APIResponseModel(success: false, message: error.errorMessage);
    }
  }
}
