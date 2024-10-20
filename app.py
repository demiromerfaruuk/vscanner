from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from zapv2 import ZAPv2
import time
import requests
import logging
import nmap
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping
from datetime import datetime
from urllib.parse import urlparse, urlunparse
import threading
from flask_socketio import SocketIO
import json
import subprocess

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Loglama yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ZAP bağlantı ayarları
ZAP_API_KEY = '75intbacd6brpl8g34pioch7nb'
ZAP_ADDRESS = '127.0.0.1'
ZAP_PORT = 8080
ZAP_PROXY = f'http://{ZAP_ADDRESS}:{ZAP_PORT}'

# Türkçe karakter desteği için font ekleme
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
addMapping('DejaVuSans', 0, 0, 'DejaVuSans')

def is_zap_running():
    try:
        response = requests.get(f'{ZAP_PROXY}/JSON/core/view/version/', 
                                params={'apikey': ZAP_API_KEY}, 
                                timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def start_zap():
    zap_command = [
        '/usr/share/zaproxy/zap.sh',
        '-daemon',
        '-host', '0.0.0.0',
        '-port', '8080',
        '-config', f'api.key={ZAP_API_KEY}'
    ]
    subprocess.Popen(zap_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def scan_open_ports(target_domain):
    nm = nmap.PortScanner()
    nm.scan(target_domain, arguments='-p 21,22,23,25,53,80,110,143,443,3306,5432,6379,27017,3389,445,389,636,88,161,123,137-139,1433,1521,5900,9200,5601,5672,2181,9092,2375-2376')
    
    open_ports = []
    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            lport = nm[host][proto].keys()
            for port in lport:
                if nm[host][proto][port]['state'] == 'open':
                    open_ports.append({
                        'port': port,
                        'protocol': proto,
                        'service': nm[host][proto][port]['name'],
                        'state': nm[host][proto][port]['state']
                    })
    
    return open_ports

def truncate_text(text, max_length=200):
    return (text[:max_length] + '...') if len(text) > max_length else text

def normalize_url(url, port):
    parsed = urlparse(url)
    
    if not parsed.scheme:
        parsed = parsed._replace(scheme='http')
    
    if not parsed.netloc and parsed.path:
        parsed = parsed._replace(netloc=parsed.path.strip('/'), path='')
    
    if not parsed.port and port not in ['80', '443']:
        netloc = f"{parsed.netloc}:{port}"
        parsed = parsed._replace(netloc=netloc)
    
    if port == '443' and parsed.scheme == 'http':
        parsed = parsed._replace(scheme='https')
    
    return urlunparse(parsed)

def sort_alerts(alerts):
    risk_order = {'High': 4, 'Medium': 3, 'Low': 2, 'Informational': 1}
    return sorted(alerts, key=lambda x: risk_order.get(x['risk'], 0), reverse=True)

def create_pdf(alerts, target_url, scan_port, open_ports):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), 
                            rightMargin=0.5*inch, leftMargin=0.5*inch, 
                            topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Small', fontName='DejaVuSans', fontSize=8, leading=10))
    styles.add(ParagraphStyle(name='Header', fontName='DejaVuSans', fontSize=16, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name='SubHeader', fontName='DejaVuSans', fontSize=12, alignment=1, spaceAfter=8))
    styles.add(ParagraphStyle(name='RiskHigh', fontName='DejaVuSans', fontSize=8, textColor=colors.red))
    styles.add(ParagraphStyle(name='RiskMedium', fontName='DejaVuSans', fontSize=8, textColor=colors.orange))
    styles.add(ParagraphStyle(name='RiskLow', fontName='DejaVuSans', fontSize=8, textColor=colors.green))
    styles.add(ParagraphStyle(name='RiskInfo', fontName='DejaVuSans', fontSize=8, textColor=colors.blue))

    elements.append(Paragraph(f"Tarama Sonuçları: {target_url}", styles['Header']))
    elements.append(Paragraph(f"Tarama Portu: {scan_port}", styles['SubHeader']))
    
    # Açık portları ekleme
    elements.append(Paragraph("Açık Portlar:", styles['SubHeader']))
    for port in open_ports:
        elements.append(Paragraph(f"Port: {port['port']}, Protokol: {port['protocol']}, Servis: {port['service']}, Durum: {port['state']}", styles['Small']))
    elements.append(Spacer(1, 0.25*inch))
    
    # Toplam sonuç sayılarını ekleme
    total_alerts = len(alerts)
    high_risk_alerts = sum(1 for alert in alerts if alert.get('risk') == 'High')
    medium_risk_alerts = sum(1 for alert in alerts if alert.get('risk') == 'Medium')
    low_risk_alerts = sum(1 for alert in alerts if alert.get('risk') == 'Low')
    informational_alerts = sum(1 for alert in alerts if alert.get('risk') == 'Informational')
    
    elements.append(Paragraph(f"Toplam Uyarı Sayısı: {total_alerts}", styles['SubHeader']))
    elements.append(Paragraph(f"Yüksek Risk: {high_risk_alerts}", styles['RiskHigh']))
    elements.append(Paragraph(f"Orta Risk: {medium_risk_alerts}", styles['RiskMedium']))
    elements.append(Paragraph(f"Düşük Risk: {low_risk_alerts}", styles['RiskLow']))
    elements.append(Paragraph(f"Bilgilendirme: {informational_alerts}", styles['RiskInfo']))
    elements.append(Spacer(1, 0.25*inch))
    
    data = [['Risk Seviyesi', 'Uyarı', 'URL', 'Açıklama']]
    for alert in alerts:
        risk_style = 'RiskHigh' if alert.get('risk') == 'High' else \
                     'RiskMedium' if alert.get('risk') == 'Medium' else \
                     'RiskLow' if alert.get('risk') == 'Low' else \
                     'RiskInfo'
        data.append([
            Paragraph(alert.get('risk', ''), styles[risk_style]),
            Paragraph(alert.get('alert', ''), styles['Small']),
            Paragraph(truncate_text(alert.get('url', '')), styles['Small']),
            Paragraph(truncate_text(alert.get('description', '')), styles['Small'])
        ])

    table = Table(data, colWidths=[1*inch, 2*inch, 3*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4a4a4a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f2f2f2')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'DejaVuSans'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))

    elements.append(table)
    doc.build(elements)
    return buffer.getvalue()

def run_zap_scan(target_url, scan_port):
    try:
        zap = ZAPv2(apikey=ZAP_API_KEY, proxies={'http': ZAP_PROXY, 'https': ZAP_PROXY})
        
        zap.spider.set_option_thread_count(10)
        zap.spider.set_option_max_depth(5)
        zap.ascan.set_option_thread_per_host(5)
        zap.ascan.set_option_max_rule_duration_in_mins(5)
        
        logger.info(f"Starting spider scan for {target_url}")
        spider_scan_id = zap.spider.scan(target_url)
        
        while int(zap.spider.status(spider_scan_id)) < 100:
            progress = zap.spider.status(spider_scan_id)
            logger.info(f"Spider progress: {progress}%")
            socketio.emit('scan_progress', {'progress': progress}, namespace='/')
            time.sleep(2)
        
        logger.info("Starting active scan")
        ascan_scan_id = zap.ascan.scan(target_url)
        
        while int(zap.ascan.status(ascan_scan_id)) < 100:
            progress = zap.ascan.status(ascan_scan_id)
            logger.info(f"Active scan progress: {progress}%")
            socketio.emit('scan_progress', {'progress': progress}, namespace='/')
            time.sleep(2)
        
        logger.info("Retrieving alerts")
        alerts = sort_alerts(zap.core.alerts())
        
        # Port tarama işlemini gerçekleştir
        domain = urlparse(target_url).netloc
        open_ports = scan_open_ports(domain)
        
        pdf = create_pdf(alerts, target_url, scan_port, open_ports)
        
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"{domain}_{current_time}.pdf"
        
        with open(pdf_filename, 'wb') as f:
            f.write(pdf)
        
        logger.info("Scan completed successfully")
        alerts_json = json.dumps(alerts)
        open_ports_json = json.dumps(open_ports)
        socketio.emit('scan_complete', {
            'alerts': alerts_json,
            'open_ports': open_ports_json,
            'pdf_filename': pdf_filename
        }, namespace='/')
    except Exception as e:
        logger.error(f"An error occurred during the scan: {str(e)}")
        socketio.emit('scan_error', {'error': str(e)}, namespace='/')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target_url = request.form['url']
        scan_port = request.form.get('port', '80')
        target_url = normalize_url(target_url, scan_port)
        
        if not is_zap_running():
            logger.error("ZAP is not running or not accessible")
            return jsonify({"error": "ZAP is not running or not accessible"}), 500

        thread = threading.Thread(target=run_zap_scan, args=(target_url, scan_port))
        thread.start()
        
        return render_template('scanning.html', target_url=target_url)
    
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')

@app.route('/scan_results', methods=['GET', 'POST'])
def scan_results():
    if request.method == 'POST':
        alerts = request.form.get('alerts')
        pdf_filename = request.form.get('pdf_filename')
    else:
        alerts = request.args.get('alerts')
        pdf_filename = request.args.get('pdf_filename')
    
    logger.info(f"Received pdf_filename: {pdf_filename}")
    
    if alerts:
        logger.info(f"Received alerts: {alerts[:100]}...")  # İlk 100 karakteri logla
        try:
            alerts = json.loads(alerts)
        except json.JSONDecodeError:
            logger.error("Failed to decode alerts JSON")
            alerts = []
    else:
        alerts = []
    
    return render_template('results.html', alerts=alerts, pdf_available=bool(pdf_filename), pdf_filename=pdf_filename)

@app.route('/download_pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    try:
        return send_file(
            filename,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"An error occurred while downloading PDF: {str(e)}")
        return jsonify({"error": "PDF indirilirken bir hata oluştu"}), 500

if __name__ == '__main__':
    if not is_zap_running():
        start_zap()
        time.sleep(5)  # ZAP'ın başlaması için biraz bekle
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)