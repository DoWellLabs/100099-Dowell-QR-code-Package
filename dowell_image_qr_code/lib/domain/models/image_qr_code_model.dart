import 'dart:io';

class QRCodeResponseModel {
  late String response;
  late List<Qrcodes> qrcodes;
  QRCodeResponseModel({required this.response, required this.qrcodes});

  QRCodeResponseModel.fromJson(Map<String, dynamic> json) {
    response = json['response'];
    if (json['qrcodes'] != null) {
      qrcodes = <Qrcodes>[];
      json['qrcodes'].forEach((v) {
        qrcodes.add(Qrcodes.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['response'] = response;
    if (qrcodes != null) {
      data['qrcodes'] = qrcodes.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Qrcodes {
  String? qrcodeId;
  int? logoSize;
  String? qrcodeColor;
  String? companyId;
  DateTime? createdBy;
  String? description;
  bool? isActive;
  String? qrcodeType;
  String? link;
  String? qrcodeImageUrl;
  String? logoUrl;

  Qrcodes(
      {this.qrcodeId,
      this.logoSize,
      this.qrcodeColor,
      this.companyId,
      this.createdBy,
      this.description,
      this.isActive,
      required this.qrcodeType,
      required this.link,
      this.qrcodeImageUrl,
      this.logoUrl});

  Qrcodes.fromJson(Map<String, dynamic> json) {
    qrcodeId = json['qrcode_id'];
    logoSize = json['logo_size'];
    qrcodeColor = json['qrcode_color'];
    companyId = json['company_id'];
    createdBy = json['created_by'];
    description = json['description'];
    isActive = json['is_active'];
    qrcodeType = json['qrcode_type'];
    link = json['link'];
    qrcodeImageUrl = json['qrcode_image_url'];
    logoUrl = json['logo_url'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['qrcode_id'] = qrcodeId;
    data['logo_size'] = logoSize;
    data['qrcode_color'] = qrcodeColor;
    data['company_id'] = companyId;
    data['created_by'] = createdBy;
    data['description'] = description;
    data['is_active'] = isActive;
    data['qrcode_type'] = qrcodeType;
    data['link'] = link;
    data['qrcode_image_url'] = qrcodeImageUrl;
    data['logo_url'] = logoUrl;
    return data;
  }
}

class ImageQRCodeRequestModel {
  String? company_id;
  String? qrcode_type;
  String? link;
  File? logo;
  String? qrcode_color;
  String? imagePath;

  int? quantity;

  ImageQRCodeRequestModel(
      {this.company_id,
      this.qrcode_type,
      this.link,
      this.logo,
      this.qrcode_color,
      this.quantity, this.imagePath});

  ImageQRCodeRequestModel.fromJson(Map<String, dynamic> json) {
    company_id = json['company_id'];
    qrcode_type = json['qrcode_type'];
    link = json['link'];
    logo = json['logo_url'];
    qrcode_color = json['qrcode_color'];
    quantity = json['quantity'];

  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = <String, dynamic>{};
    data['company_id'] = company_id;
    data['qrcode_type'] = qrcode_type;
    data['link'] = link;
    data['logo'] = logo;
    data['qrcode_color'] = qrcode_color;
    data['quantity'] = quantity;
    

    return data;
  }
}
