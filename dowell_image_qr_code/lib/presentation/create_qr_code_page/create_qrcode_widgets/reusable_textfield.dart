import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class reusableTextField extends StatelessWidget {
  final String label;
  final String hintText;
  final TextEditingController textEditingController;
  const reusableTextField({
    super.key,
    required this.label,
    required this.hintText,
    required this.textEditingController,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 350.w,
      margin: EdgeInsets.only(left: 10.w, right: 10.w, bottom: 10.h),
      padding:
          EdgeInsets.only(left: 10.w, right: 10.w, top: 10.h, bottom: 10.h),
      decoration: BoxDecoration(
          color: Colors.white, borderRadius: BorderRadius.circular(5.h)),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            label,
            style: const TextStyle(
                fontFamily: 'RobotoMedium', color: Colors.black),
          ),
          SizedBox(
            height: 5.h,
          ),
          TextField(
            controller: textEditingController,
            obscureText: false,
            decoration: InputDecoration(
                hintText: hintText,
                hintStyle: TextStyle(color: Colors.grey.withOpacity(0.5)),
                enabledBorder: OutlineInputBorder(
                  borderSide: const BorderSide(
                    color: Color(0xFFE2E2EC),
                    width: 2,
                  ),
                  borderRadius: BorderRadius.circular(8.h),
                ),
                focusedBorder: OutlineInputBorder(
                  borderSide: const BorderSide(
                    color: Color(0xFFE2E2EC),
                    width: 2,
                  ),
                  borderRadius: BorderRadius.circular(8.h),
                ),
                errorBorder: OutlineInputBorder(
                  borderSide: const BorderSide(
                    color: Colors.red,
                    width: 2,
                  ),
                  borderRadius: BorderRadius.circular(8.h),
                ),
                focusedErrorBorder: OutlineInputBorder(
                  borderSide: const BorderSide(
                    color: Colors.red,
                    width: 2,
                  ),
                  borderRadius: BorderRadius.circular(8.h),
                ),
                contentPadding: EdgeInsets.only(
                    left: 10.w, right: 10.w, top: 10.w, bottom: 10.w)),
          ),
          SizedBox(
            height: 5.h,
          )
        ],
      ),
    );
  }
}
