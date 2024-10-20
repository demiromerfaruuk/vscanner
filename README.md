# 🌐 **vscanner - Web Güvenlik Tarayıcısı**

![vscanner logo](images/vscanner_logo.jpg)

vscanner, web uygulamalarının güvenliğini taramak için geliştirilmiş güçlü bir araçtır. ZAP (Zed Attack Proxy) ile entegre çalışarak, hedef URL'lerdeki güvenlik açıklarını tespit eder ve sonuçları PDF formatında raporlar.

---

## 🚀 **Özellikler**

- **🔍 Kapsamlı Güvenlik Taraması:** Hedef URL'lerdeki potansiyel güvenlik açıklarını tespit etmek için ZAP'ın güçlü tarama motorunu kullanır.
- **🌐 Açık Port Tespiti:** Hedef sistemdeki açık portları belirleyerek, olası saldırı yüzeylerini analiz eder.
- **📄 Profesyonel PDF Raporlama:** Tarama sonuçlarını detaylı bir şekilde sunan, özelleştirilebilir PDF raporları oluşturur.
- **📊 Gerçek Zamanlı Durum Güncellemeleri:** Tarama sürecinde kullanıcıya anlık ilerleme ve durum güncellemeleri sağlar.
- **⚙️ Çoklu Protokol Desteği:** HTTP, HTTPS ve diğer protokoller üzerinden tarama yapabilme yeteneği.
- **🔔 Uyarı ve Risk Yönetimi:** Tespit edilen güvenlik açıklarını risk seviyelerine göre sıralar ve kullanıcıya detaylı bilgi sunar.
- **📈 Kullanıcı Dostu Arayüz:** Basit ve sezgisel bir arayüz ile kullanıcıların tarama işlemlerini kolayca gerçekleştirmesine olanak tanır.
- **🔒 Güvenlik ve Gizlilik:** Kullanıcı verilerini koruma ve güvenli bir tarama deneyimi sağlama amacıyla tasarlanmıştır.


---

## 📋 **Gereksinimler**

- **Python 3.x**
- **Flask**
- **Flask-SocketIO**
- **ZAPv2**
- **Nmap**
- **ReportLab**

---

## 🛠️ **Kurulum**

1. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install flask flask-socketio zapv2 python-nmap reportlab
   ```

2. ZAP'ı kurun ve çalıştırın. ZAP'ın API anahtarını ve adresini ayarlayın.

3. Uygulamayı başlatın:
   ```bash
   python app.py
   ```

4. Tarayıcınızda `http://127.0.0.1:5000` adresine gidin.

---

## 🖥️ **Kullanım**

1. Hedef URL'yi ve port numarasını girin.
2. **"Güvenlik Taraması Başlat"** butonuna tıklayın.
3. Tarama tamamlandığında sonuçları görüntüleyin ve PDF olarak indirin.

---

## 🤝 **Katkıda Bulunma**

Katkıda bulunmak isterseniz, lütfen bir pull request oluşturun veya sorunları bildirin. Her türlü katkı memnuniyetle karşılanır!

---

## 📄 **Lisans**

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

## 📞 **İletişim**

Herhangi bir sorunuz veya geri bildiriminiz varsa, lütfen [email@example.com](mailto:email@example.com) adresi üzerinden bizimle iletişime geçin.

---

**vscanner ile web güvenliğinizi artırın!** 🔒

![Security Image](images/results_scanning.jpg)

