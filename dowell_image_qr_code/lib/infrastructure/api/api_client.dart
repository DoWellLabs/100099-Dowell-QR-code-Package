import 'package:dio/dio.dart';
import 'package:dowell_image_qr_code/domain/models/image_qr_code_model.dart';
import 'package:dowell_image_qr_code/infrastructure/api/api_end_points.dart';

class ApiClient {
  static late Dio _dio;

  ApiClient() {
    BaseOptions options = BaseOptions(
      connectTimeout: Duration(seconds: 30),
      receiveTimeout: Duration(seconds: 30),
      headers: {"Cache-Control": "no-cache"},
    );

    _dio = Dio(options);
  }

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
      String url, ImageQRCodeRequestModel imageQRCodeRequestModel,
      {Map<String, dynamic>? queryParameters}) async {
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
      var response =
          await _dio.post(url, data: data, queryParameters: queryParameters);

      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> put(String url,
      {required Qrcodes qrcode, Map<String, dynamic>? queryParameters}) async {
    FormData data = FormData.fromMap({"link": qrcode.logoUrl});

    try {
      final response = await _dio.put(
          "${ApiEndPoints.BASE_URL}${ApiEndPoints.UPDATE_QR_CODE_END_POINT}${qrcode.qrcodeId}/",
          data: data);

      return response;
    } catch (e) {
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
}
