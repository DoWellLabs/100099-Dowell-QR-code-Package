import 'dart:convert';

import 'package:dio/dio.dart';
import 'package:dowell_image_qr_code/domain/models/image_qr_code_model.dart';
import 'package:dowell_image_qr_code/infrastructure/api/api_end_points.dart';

class ApiClient {
  static late Dio _dio;

  ApiClient() {
    BaseOptions options = BaseOptions(
      connectTimeout: Duration(seconds: 30), // 60 seconds
      receiveTimeout: Duration(seconds: 30),
      headers: {"Cache-Control": "no-cache"},
      // 60 seconds
    );

    _dio = Dio(options);
  }
  //static final Dio _dio = Dio(); // Create a singleton instance of Dio

  Future<Response> get(String url,
      {Map<String, dynamic>? queryParameters}) async {
    try {
      var response = await _dio.get(url, queryParameters: queryParameters);
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> post(
      String url, ImageQRCodeRequestModel imageQRCodeRequestModel) async {
    print("...from api posting request");

    print(
        "... from api post methode.... imagepath is ${imageQRCodeRequestModel.imagePath}");

    FormData data = FormData.fromMap({
      "qrcode_type": "${imageQRCodeRequestModel.qrcode_type}",
      "link": "${imageQRCodeRequestModel.link}",
      "logo": imageQRCodeRequestModel.imagePath != null
          ? await MultipartFile.fromFile(
              imageQRCodeRequestModel.imagePath!.split("#").first,
              filename: imageQRCodeRequestModel.imagePath!.split("#").last)
          : null,
      "company_id": imageQRCodeRequestModel.company_id,
      "quantity": imageQRCodeRequestModel.quantity
    });
    try {
      var response = await _dio.post(url, data: data);

      print("...from api client... ${response.statusMessage}");

      // imageQRCodeRequestModel.qrcode_type = null;
      // imageQRCodeRequestModel.link = null;
      // imageQRCodeRequestModel.imagePath = null;
      // imageQRCodeRequestModel.company_id = null;
      // imageQRCodeRequestModel.quantity = null;
      // imageQRCodeRequestModel.qrcode_color = null;
      // imageQRCodeRequestModel.logo = null;
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> put(String url,
      {required Qrcodes qrcode, Map<String, dynamic>? queryParameters}) async {
    print(
        "...from api client put method qrcode type is... ${qrcode.qrcodeType}");
    print("...from api client put method... put url is $url");
    print("...from api client put method logo_url... ${qrcode.logoUrl}");
    print("...from api client put method link is... ${qrcode.link}");

    FormData data = FormData.fromMap({"link": qrcode.logoUrl});

    try {
      final response = await _dio.put(
          "${ApiEndPoints.BASE_URL}${ApiEndPoints.UPDATE_QR_CODE_END_POINT}${qrcode.qrcodeId}/",
          data: data);

      print(
          "...from api client put method respons... ${response.statusMessage}");

      return response;
    } catch (e) {
      print("...from api client put method catch... ${e.toString()}");
      rethrow;
    }
  }

  Future<Response> delete(String url,
      {Map<String, dynamic>? queryParameters}) async {
    try {
      final response = await _dio.delete(url, queryParameters: queryParameters);
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> downloadQRCode(String url, String filePath) async {
    try {
      final response = await _dio.download(url, filePath);
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Exception _handleError(dynamic error) {
    print("...error from api client... $error");
    if (error is DioException) {
      final dioException = error as DioException;
      String errorMessage;

      if (dioException.response != null) {
        // The request was made and the server responded with a status code
        final statusCode = dioException.response!.statusCode;
        final responseData = dioException.response!.data;

        if (statusCode == 400) {
          errorMessage = 'Bad request';
        } else if (statusCode == 401) {
          errorMessage = 'Unauthorized';
        } else if (statusCode == 404) {
          errorMessage = 'Not found';
        } else {
          errorMessage = 'Request failed with status code $statusCode';
        }
      } else {
        errorMessage = 'Network error occurred';
      }

      throw Exception('API Error: $errorMessage');
    } else {
      throw Exception('Unexpected error occurred.');
    }
  }
}
