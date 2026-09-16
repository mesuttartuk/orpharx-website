# OrphaRx web sitesi

Türkçe ve İngilizce, mobil uyumlu 12 statik HTML sayfası. Framework, derleme veya paket kurulumu gerektirmez.

## Ön izleme

`index.html` İngilizce, `tr/index.html` Türkçe ana sayfadır. Dosyayı tarayıcıda açabilir veya bu klasörde `python -m http.server 8080` çalıştırıp `http://localhost:8080/tr/` adresini ziyaret edebilirsiniz.

## İçerik güncelleme

`content-source.json` iki dildeki metinleri içerir. Metinleri değiştirdikten sonra Python 3 ile bu klasörde `python generate.py` çalıştırın. HTML sayfaları yeniden oluşturulur. Tasarım `styles.css`, etkileşimler `app.js` içindedir. İngilizce metinler sağlanan belgeden derlenmiştir; Türkçe metinler bu çalışma kapsamında çevrilmiştir. Kurucu fotoğrafları, gerçek adres veya telefon eklenmemiştir. Logo kullanıcının sağladığı SVG dosyasıdır, değiştirilmemiştir.

## İletişim formu — mevcut durum

Alıcı: **fatmatartuk@gmail.com**. Ön izlemede otomatik gönderim kapalıdır. Form alan doğrulaması yapar, bilgileri korur ve e-posta uygulamasında doldurulmuş taslak açabilir. Bu işlem kendi başına e-posta göndermez; ziyaretçi e-posta uygulamasında gönderir. Uzun mesajların mailto desteği uygulamaya göre değişebilir.

Otomatik gönderim için opsiyonel PHP 8.1+ dosyası `api/contact.php` hazırlanmıştır. Statik HTML dosyaları herhangi bir statik sunucuda çalışır; bu PHP dosyası ise PHP çalıştırabilen hosting ve yapılandırılmış bir posta aktarım servisi gerektirir. Salt statik hosting seçilirse bu uç nokta bir sunucusuz işlev veya uygun form servisiyle değiştirilmelidir.

PHP kurulumunda:

1. Alan adı alındığında HTTPS kullanın ve sunucu posta aktarımını/SMTP relay'i yapılandırın. Alan adına ait gönderici adresi için SPF ve DKIM kayıtlarını kurun.
2. Sunucu ortamına `ORPHARX_MAIL_FROM=noreply@gercek-alan-adiniz`, `ORPHARX_SITE_ORIGIN=https://gercek-alan-adiniz` ve `ORPHARX_MAIL_ENABLED=1` değerlerini ekleyin. Örnek alan adını gerçek alan adıyla değiştirin. Anahtarları tarayıcı koduna koymayın.
3. `generate.py` içindeki `config['deliveryEnabled']=False` değerini `True` yapın. Her iki dilde `formStatus` metnini etkin gönderimi anlatacak şekilde güncelleyin; yeniden `python generate.py` çalıştırın.
4. Test mesajı gönderip alıcının gelen kutusuna ulaştığını doğrulayın. PHP `mail()` kabul yanıtı teslimat garantisi değildir. Gönderim hatası, zaman aşımı, zorunlu alanlar ve hız sınırını kontrol edin.
5. Formun gerçek veri işleme sürecine uygun kurumsal aydınlatma metnini yayından önce tamamlayın. Mevcut kısa kullanım açıklaması kapsamlı bir hukuki metin değildir.

Sunucu: sabit alıcı, sunucu tarafı doğrulama, Origin kontrolü, honeypot, 60 saniyelik IP bazlı gönderim sınırı ve güvenli başlıklar içerir. Hız sınırı tek sunucu içindir; çoklu sunucuda ortak depolama gerektirir. Bu ortamda PHP/mail sunucusu bulunmadığından gerçek e-posta teslimatı test edilmemiştir. Kullanıcı adına hiçbir test e-postası gönderilmemiştir.

## Dosyalar

- `index.html`, `about.html`, `focus.html`, `partnerships.html`, `founders.html`, `contact.html`: İngilizce sayfalar.
- `tr/`: Türkçe karşılıkları.
- `assets/`: yerel logo, özgün üretilmiş görsel ve yerel fontlar.
- `ASSET-LICENSES.md`: kaynak ve lisans kayıtları.
- `generate.py`, `content-source.json`: içerik yönetimi için kaynak dosyalar.

Yayımlama bu aşamada yapılmamıştır. Alan adı ve hosting seçildiğinde form bağlantısı, kurumsal iletişim bilgileri ve alan adına bağlı SEO etiketleri tamamlanabilir.

## Telefon alanı

Ülke seçimi Türkiye varsayılanıyla sunulur; ülke adları sayfanın diline göre gösterilir. Telefon isteğe bağlıdır; girildiğinde seçilen ülkenin numara planıyla doğrulanır. Yazarken biçimlendirilir, alandan çıkarken uluslararası gösterime çevrilir; e-posta ve form verisinde E.164 biçiminde gönderilir. Ülkeyle uyuşmayan ve eksik numaralar engellenir. Bu doğrulama numaranın tahsis edilmiş veya ulaşılabilir olduğunu kanıtlamaz. Kütüphane ve metadata yerel dosyadadır; numara planları değiştikçe güncellenmelidir. PHP uç noktası uluslararası sözdizimini kontrol eder; ülkeye özgü ayrıntılı doğrulama tarayıcıda çalışır.
