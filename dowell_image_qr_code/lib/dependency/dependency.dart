import 'package:dowell_image_qr_code/infrastructure/api/api_client.dart';
import 'package:get/get.dart';

import '../application/controllers/image_qr_code_controller/image_qr_code_controller.dart';
import '../infrastructure/repositories/image_qr_code_repo/image_qr_code_repo.dart';

Future<void> init() async {
  // api client
  Get.lazyPut(() => ApiClient());



  //repository
  Get.lazyPut(() => ImageQRCodeRepository(apiClient: Get.find()));

  

  // controller
  Get.lazyPut(() => QRCodeController(imageQRCodeRepository: Get.find()));
}
