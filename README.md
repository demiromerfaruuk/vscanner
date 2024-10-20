# 🌐 **vscanner - Web Güvenlik Tarayıcısı**

![vscanner logo](images/vscanner_logo.jpg)

vscanner, web uygulamalarının güvenliğini taramak için geliştirilmiş güçlü bir araçtır. ZAP (Zed Attack Proxy) ile entegre çalışarak, hedef URL'lerdeki güvenlik açıklarını tespit eder ve sonuçları PDF formatında raporlar.

---

## 🚀 **Özellikler**

- **🔍 Güvenlik Taraması:** Hedef URL'lerde kapsamlı güvenlik taraması yapar.
- **🌐 Açık Port Tespiti:** Hedef sistemdeki açık portları tespit eder.
- **📄 PDF Raporlama:** Tarama sonuçlarını profesyonel bir PDF raporu olarak indirmenizi sağlar.
- **📊 Gerçek Zamanlı Güncellemeler:** Tarama sürecinde anlık durum güncellemeleri alırsınız.

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

