import 'package:dowell_image_qr_code/presentation/welcome/welcome_state.dart';
import 'package:dowell_image_qr_code/routes/route_name.dart';
import 'package:get/get.dart';

class WelcomeController extends GetxController {
  WelcomeController();

  final String logotitle1 = "Dowell";
  final String logotitle2 = "Image QR Code";

  WelcomeState state =
      WelcomeState(); // used for navigation, transition, routing to new page
  @override
  void onReady() {
    super.onReady();

    Future.delayed(const Duration(seconds: 5),
        (() => Get.offAllNamed(AppRoutes.HOMEPAGE)));
  }
}
