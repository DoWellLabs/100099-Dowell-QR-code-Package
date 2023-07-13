import 'package:dio/dio.dart';
import 'package:dowell_image_qr_code/domain/models/image_qr_code_model.dart';
import 'package:dowell_image_qr_code/infrastructure/api/api_end_points.dart';

import '../../api/api_client.dart';

class ImageQRCodeRepository {
  final ApiClient apiClient;

  ImageQRCodeRepository({required this.apiClient});

  Future<Response> getQRCode({Map<String, dynamic>? queryParameters}) async {
    try {
      final response = await apiClient.get("${ApiEndPoints.BASE_URL}",
          queryParameters: queryParameters);
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> createQRCode(ImageQRCodeRequestModel qrCodeRequestModel,
      {Map<String, dynamic>? queryParameters}) async {
    try {
      Response response = await apiClient.post(
        "${ApiEndPoints.BASE_URL}/${ApiEndPoints.CREATE_QR_CODE_END_POINT}",
        qrCodeRequestModel,
        queryParameters: queryParameters,
      );
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> updateQRCode(Qrcodes qrcode,
      {Map<String, dynamic>? queryParameters}) async {
    try {
      final response = await apiClient.put(
          "${ApiEndPoints.BASE_URL}${ApiEndPoints.UPDATE_QR_CODE_END_POINT}${qrcode.qrcodeId}/",
          qrcode: qrcode,
          queryParameters: queryParameters);
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> deleteQRCode({Map<String, dynamic>? queryParameters}) async {
    try {
      final response = await apiClient.delete("${ApiEndPoints.BASE_URL}",
          queryParameters: queryParameters);
      return response;
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> downloadQRCode(String qrcodeName, String filePath) {
    try {
      final response = apiClient.downloadQRCode(
          "${ApiEndPoints.DOWNLOAD_QR_CODE_BASE_URL}$qrcodeName", filePath);
      return response;
    } catch (e) {
      rethrow;
    }
  }
}
