import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 800, "INFORME EJECUTIVO DE ARQUITECTURA WEB, CACHÉ Y ALTA DISPONIBILIDAD")
            self.drawRightString(541, 800, "ASIR - PRODUCCIÓN AWS")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 792, 541, 792)

        # Footer
        self.setFont("Helvetica", 8)
        self.drawString(54, 35, "Confidencial | Autor: Jose Vizuete (eljoviz.servepics.com)")
        self.drawRightString(541, 35, f"Página {self._pageNumber} de {page_count}")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 541, 48)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e3a8a')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#0f172a')
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("INFORME DE ARQUITECTURA WEB DE ALTA DISPONIBILIDAD", title_style))
    story.append(Paragraph("<b>Auditoría de Rendimiento (ab), Aceleración en RAM (Varnish), Seguridad Perimetral y DNS Failover</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceBefore=2, spaceAfter=10))

    # Meta Info Box
    meta_data = [
        [Paragraph("<b>Entorno:</b> AWS Cloud (Debian 13 Trixie)", table_cell_style), Paragraph("<b>Dominio Oficial:</b> eljoviz.servepics.com", table_cell_style)],
        [Paragraph("<b>Autor:</b> Jose Vizuete (Administrador de Sistemas)", table_cell_style), Paragraph("<b>Destinatario:</b> Dirección Técnica / Profesorado ASIR", table_cell_style)],
        [Paragraph("<b>Fecha de Entrega:</b> 18 de Noviembre de 2026", table_cell_style), Paragraph("<b>Estado:</b> Producción Validada (100% Operativa)", table_cell_style)]
    ]
    t_meta = Table(meta_data, colWidths=[240, 247])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))

    # Section 1
    story.append(Paragraph("1. Resumen Ejecutivo y Diagnóstico", h1_style))
    story.append(Paragraph(
        "En la arquitectura tradicional monolítica de servidor único, <b>Apache 2.4</b> colapsa bajo picos de concurrencia masiva debido al agotamiento de hilos de trabajo (<i>workers</i>) y a la sobrecarga criptográfica de TLS en cada petición. Asimismo, la presencia de una única máquina introduce un <b>Punto Único de Fallo (SPOF)</b> que deja el servicio totalmente inoperativo ante caídas.",
        body_style
    ))
    story.append(Paragraph(
        "Para solventar estas deficiencias de forma profesional, se ha diseñado e implementado una <b>arquitectura desacoplada en dos niveles (Tier Edge / Tier Backend)</b> en instancias independientes de AWS, interconectadas mediante red privada segura y protegidas con cortafuegos perimetral.",
        body_style
    ))

    # Section 2: Catálogo de Servicios
    story.append(Paragraph("2. Catálogo de Servicios Implementados", h1_style))
    story.append(Paragraph(
        "A continuación se describe el rol técnico y la justificación de cada componente integrado en la infraestructura:",
        body_style
    ))

    servicios_data = [
        [Paragraph("Servicio", table_header_style), Paragraph("Instancia / Puerto", table_header_style), Paragraph("Función Técnica y Justificación Empresarial", table_header_style)],
        [Paragraph("<b>Varnish Cache 7.7</b>", table_cell_bold), Paragraph("Instancia 1 (Frontend)<br/>Puerto 6081 (RAM)", table_cell_style), Paragraph("Acelerador HTTP en memoria. Absorbe miles de peticiones sin tocar disco ni consultar a Apache (Cache HIT). Configurado con <b>Grace Mode</b> para seguir sirviendo la web si Apache cae.", table_cell_style)],
        [Paragraph("<b>Nginx 1.26</b>", table_cell_bold), Paragraph("Instancia 1 (Frontend)<br/>Puertos 80 y 443", table_cell_style), Paragraph("Terminador TLS perimetral de alto rendimiento. Gestiona el protocolo <b>HTTP/2</b> (multiplexación) y aplica cabeceras de seguridad militar (HSTS, Anti-Clickjacking).", table_cell_style)],
        [Paragraph("<b>Apache 2.4</b>", table_cell_bold), Paragraph("Instancia 2 (Backend)<br/>Puerto 80 / 443", table_cell_style), Paragraph("Servidor web de aplicaciones. Aloja los archivos del sitio. Opera aislado en la red interna para garantizar la integridad del contenido.", table_cell_style)],
        [Paragraph("<b>nftables</b>", table_cell_bold), Paragraph("Ambas Instancias<br/>Kernel de Linux", table_cell_style), Paragraph("Cortafuegos de filtrado de paquetes. En Backend, <b>bloquea todo acceso exterior</b> y solo autoriza tráfico HTTP proveniente de la IP privada de Varnish (172.31.40.241).", table_cell_style)],
        [Paragraph("<b>Certbot / Let's Encrypt</b>", table_cell_bold), Paragraph("Automatizado<br/>TLS v1.3", table_cell_style), Paragraph("Gestión del ciclo de vida del certificado criptográfico oficial, asegurando cifrado punto a punto y candado verde válido para el dominio público.", table_cell_style)],
        [Paragraph("<b>DNS Failover Watchdog</b>", table_cell_bold), Paragraph("Instancia 2 (Backend)<br/>Systemd Service", table_cell_style), Paragraph("Demonio centinela que monitoriza la salud de Varnish cada 5s. Si Varnish muere, conmuta automáticamente el DNS de No-IP a Apache para evitar caídas del servicio.", table_cell_style)]
    ]

    t_servicios = Table(servicios_data, colWidths=[105, 115, 267])
    t_servicios.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e40af')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_servicios)
    story.append(Spacer(1, 10))

    # Page Break for Charts & Data
    story.append(PageBreak())

    # Section 3: Benchmark & Charts
    story.append(Paragraph("3. Resultados Empíricos de Pruebas de Carga (ApacheBench)", h1_style))
    story.append(Paragraph(
        "Se sometieron ambos entornos a pruebas de estrés idénticas simulando tráfico masivo desde la red de clientes (1.000 usuarios concurrentes / 5.000 peticiones totales):",
        body_style
    ))

    benchmark_data = [
        [Paragraph("Métrica de Rendimiento", table_header_style), Paragraph("Apache a Pelo (Sin Caché)", table_header_style), Paragraph("Nginx + Varnish (RAM)", table_header_style), Paragraph("Impacto / Mejora", table_header_style)],
        [Paragraph("<b>Peticiones por Segundo (RPS)</b>", table_cell_bold), Paragraph("573,73 req/s", table_cell_style), Paragraph("<b>1.281,79 req/s</b>", table_cell_bold), Paragraph("<b>+123,4% (x2.2 veces más veloz)</b>", table_cell_bold)],
        [Paragraph("<b>Tiempo Total de Ejecución</b>", table_cell_bold), Paragraph("8,715 segundos", table_cell_style), Paragraph("<b>3,901 segundos</b>", table_cell_bold), Paragraph("<b>Reducción del 55,2% en tiempo</b>", table_cell_style)],
        [Paragraph("<b>Peticiones Fallidas (Errores)</b>", table_cell_bold), Paragraph("<font color='#dc2626'><b>223 fallos (Saturación)</b></font>", table_cell_style), Paragraph("<font color='#16a34a'><b>0 fallos (100% Éxito)</b></font>", table_cell_bold), Paragraph("<b>Estabilidad absoluta (0% pérdidas)</b>", table_cell_style)],
        [Paragraph("<b>Latencia Peor Cliente (p100)</b>", table_cell_bold), Paragraph("8.476 ms (8,5 segundos)", table_cell_style), Paragraph("<b>3.677 ms (3,6 segundos)</b>", table_cell_bold), Paragraph("<b>Reducción del 56,6% en colas</b>", table_cell_style)],
        [Paragraph("<b>Rendimiento con Keep-Alive (-k)</b>", table_cell_bold), Paragraph("303 req/s", table_cell_style), Paragraph("<b>1.459 req/s</b>", table_cell_bold), Paragraph("<b>p80 atendido en 163 ms</b>", table_cell_bold)]
    ]

    t_bench = Table(benchmark_data, colWidths=[130, 115, 115, 127])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # Inserción de gráficos
    img1_path = "/home/2asird/.gemini/antigravity/scratch/infraestructura-web-alta-disponibilidad/img/grafico1_rendimiento.png"
    img2_path = "/home/2asird/.gemini/antigravity/scratch/infraestructura-web-alta-disponibilidad/img/grafico2_estabilidad.png"

    if os.path.exists(img1_path):
        story.append(Image(img1_path, width=440, height=210))
        story.append(Spacer(1, 6))

    if os.path.exists(img2_path):
        story.append(Image(img2_path, width=440, height=185))
        story.append(Spacer(1, 8))

    # Section 4: Conclusiones
    story.append(Paragraph("4. Dictamen Técnico de Seguridad y Resiliencia", h1_style))
    story.append(Paragraph(
        "<b>1. Eliminación de Colapsos por Estrés:</b> Bajo 1.000 clientes concurrentes, Apache agota sus 150 hilos, acumulando más de 200 peticiones truncadas. Varnish resuelve el 100% de las solicitudes desde memoria sin degradar el backend.<br/>"
        "<b>2. Resiliencia ante Desastres (Failover & Grace Mode):</b> Si el backend falla, Varnish activa <i>Grace Mode</i> manteniendo la web viva durante 1 hora. Si Varnish cae, el demonio centinela redirige el dominio automáticamente a Apache.<br/>"
        "<b>3. Blindaje Criptográfico (A+):</b> La integración de HSTS y HTTP/2 garantiza el máximo nivel de protección según los estándares de ciberseguridad del CCN-CERT.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generado correctamente en:", filename)

if __name__ == '__main__':
    out_pdf = "/home/2asird/.gemini/antigravity/scratch/infraestructura-web-alta-disponibilidad/Informe_Alta_Disponibilidad_Varnish_Apache.pdf"
    build_pdf(out_pdf)
