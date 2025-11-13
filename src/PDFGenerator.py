"""
Módulo para generar reportes forenses en PDF
"""
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class PDFGenerator:
    """Clase para generar reportes forenses en PDF"""
    
    def __init__(self, output_dir: str = "."):
        """
        Inicializa el generador de PDF
        
        Args:
            output_dir: Directorio donde guardar los PDFs
        """
        self.output_dir = output_dir
        
        # Crear directorio si no existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Estilos
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Crea estilos personalizados para el PDF"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
        
        # Alerta (para hallazgos críticos)
        self.styles.add(ParagraphStyle(
            name='Alert',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.red,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        # Warning (para hallazgos medios)
        self.styles.add(ParagraphStyle(
            name='Warning',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.orange,
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
    
    def generate_forensic_report(
        self,
        analysis_data: Dict[str, Any],
        task_name: str,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Genera un reporte forense en PDF
        
        Args:
            analysis_data: Datos del análisis de la IA
            task_name: Nombre de la tarea ejecutada
            output_filename: Nombre del archivo de salida (opcional)
            
        Returns:
            Ruta al archivo PDF generado
        """
        # Generar nombre de archivo si no se proporciona
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"reporte_forense_{timestamp}.pdf"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Crear documento PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Contenedor de elementos
        story = []
        
        # Encabezado del reporte
        story.extend(self._create_header(task_name))
        
        # Resumen ejecutivo
        if 'summary_short' in analysis_data and analysis_data['summary_short']:
            story.extend(self._create_summary_section(analysis_data['summary_short']))
        
        # Análisis estructurado
        if 'analysis' in analysis_data and analysis_data['analysis']:
            story.extend(self._create_analysis_section(analysis_data['analysis']))
        
        # Hallazgos detallados
        if 'analysis' in analysis_data and 'findings' in analysis_data['analysis']:
            story.extend(self._create_findings_section(analysis_data['analysis']['findings']))
        
        # Recomendaciones
        if 'analysis' in analysis_data and 'recommendations' in analysis_data['analysis']:
            story.extend(self._create_recommendations_section(
                analysis_data['analysis']['recommendations']
            ))
        
        # Estadísticas
        if 'analysis' in analysis_data and 'statistics' in analysis_data['analysis']:
            story.extend(self._create_statistics_section(
                analysis_data['analysis']['statistics']
            ))
        
        # Pie de página con información legal
        story.extend(self._create_footer())
        
        # Construir PDF
        doc.build(story)
        
        return output_path
    
    def _create_header(self, task_name: str) -> List:
        """Crea el encabezado del reporte"""
        elements = []
        
        # Título
        title = Paragraph("Reporte de Análisis Forense", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Información del reporte
        info_data = [
            ['Tarea:', task_name],
            ['Fecha:', datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            ['Herramienta:', 'AutoForense v1.0'],
            ['Sistema:', 'Windows']
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8e8e8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_summary_section(self, summary: str) -> List:
        """Crea la sección de resumen ejecutivo"""
        elements = []
        
        heading = Paragraph("Resumen Ejecutivo", self.styles['CustomHeading'])
        elements.append(heading)
        
        summary_text = Paragraph(summary, self.styles['CustomBody'])
        elements.append(summary_text)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_analysis_section(self, analysis: Dict[str, Any]) -> List:
        """Crea la sección de análisis general"""
        elements = []
        
        if 'summary' in analysis:
            heading = Paragraph("Análisis General", self.styles['CustomHeading'])
            elements.append(heading)
            
            summary_text = Paragraph(analysis['summary'], self.styles['CustomBody'])
            elements.append(summary_text)
            elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_findings_section(self, findings: List[Dict[str, Any]]) -> List:
        """Crea la sección de hallazgos"""
        elements = []
        
        if not findings:
            return elements
        
        heading = Paragraph("Hallazgos Detectados", self.styles['CustomHeading'])
        elements.append(heading)
        
        for idx, finding in enumerate(findings, 1):
            # Determinar estilo según el nivel de riesgo
            risk_level = finding.get('risk_level', 'low').lower()
            confidence = finding.get('confidence', 'low').lower()
            
            # Título del hallazgo
            finding_title = f"<b>Hallazgo {idx}: {finding.get('title', 'Sin título')}</b>"
            if risk_level == 'high':
                finding_title = f'<font color="red">{finding_title}</font>'
            elif risk_level == 'medium':
                finding_title = f'<font color="orange">{finding_title}</font>'
            else:
                finding_title = f'<font color="blue">{finding_title}</font>'
            
            elements.append(Paragraph(finding_title, self.styles['CustomBody']))
            
            # Información del hallazgo
            info_lines = []
            info_lines.append(f"<b>Nivel de Riesgo:</b> {risk_level.upper()}")
            info_lines.append(f"<b>Confianza:</b> {confidence.upper()}")
            
            if 'description' in finding:
                info_lines.append(f"<b>Descripción:</b> {finding['description']}")
            
            if 'evidence' in finding:
                info_lines.append(f"<b>Evidencia:</b> {finding['evidence']}")
            
            for line in info_lines:
                elements.append(Paragraph(line, self.styles['CustomBody']))
            
            elements.append(Spacer(1, 12))
        
        return elements
    
    def _create_recommendations_section(self, recommendations: List[str]) -> List:
        """Crea la sección de recomendaciones"""
        elements = []
        
        if not recommendations:
            return elements
        
        heading = Paragraph("Recomendaciones", self.styles['CustomHeading'])
        elements.append(heading)
        
        for idx, rec in enumerate(recommendations, 1):
            rec_text = f"<b>{idx}.</b> {rec}"
            elements.append(Paragraph(rec_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_statistics_section(self, statistics: Dict[str, Any]) -> List:
        """Crea la sección de estadísticas"""
        elements = []
        
        if not statistics:
            return elements
        
        heading = Paragraph("Estadísticas del Análisis", self.styles['CustomHeading'])
        elements.append(heading)
        
        stats_data = [['Métrica', 'Valor']]
        for key, value in statistics.items():
            # Formatear el nombre de la métrica
            metric_name = key.replace('_', ' ').title()
            stats_data.append([metric_name, str(value)])
        
        stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(stats_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_footer(self) -> List:
        """Crea el pie de página con información legal"""
        elements = []
        
        elements.append(PageBreak())
        
        heading = Paragraph("Declaración Legal", self.styles['CustomHeading'])
        elements.append(heading)
        
        legal_text = """
        AutoForense se proporciona "tal cual", sin garantías de ningún tipo. 
        Su uso es bajo su exclusiva responsabilidad. Ni el autor ni los distribuidores 
        serán responsables por daños directos, indirectos, incidentales, consecuentes 
        o de cualquier otra índole derivados del uso o mal uso del software. 
        AutoForense no sustituye asesoría profesional forense ni legal; el usuario 
        debe verificar el cumplimiento de todas las leyes y regulaciones aplicables.
        <br/><br/>
        Este reporte fue generado automáticamente por AutoForense y debe ser revisado 
        por un profesional calificado antes de tomar cualquier acción basada en sus 
        hallazgos.
        """
        
        elements.append(Paragraph(legal_text, self.styles['CustomBody']))
        
        return elements
    
    def generate_multiple_tasks_report(
        self,
        tasks_analyses: Dict[str, Dict[str, Any]],
        consolidated_analysis: Optional[Dict[str, Any]] = None,
        output_filename: Optional[str] = None
    ) -> str:
        """
        Genera un reporte consolidado de múltiples tareas
        
        Args:
            tasks_analyses: Dict con análisis de cada tarea
            consolidated_analysis: Análisis consolidado opcional
            output_filename: Nombre del archivo de salida
            
        Returns:
            Ruta al archivo PDF generado
        """
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"reporte_forense_consolidado_{timestamp}.pdf"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Encabezado
        story.extend(self._create_header("Análisis Forense Consolidado"))
        
        # Si hay análisis consolidado, mostrarlo primero
        if consolidated_analysis:
            if 'summary_short' in consolidated_analysis:
                story.extend(self._create_summary_section(
                    consolidated_analysis['summary_short']
                ))
            
            if 'analysis' in consolidated_analysis:
                story.extend(self._create_analysis_section(
                    consolidated_analysis['analysis']
                ))
                
                if 'findings' in consolidated_analysis['analysis']:
                    story.extend(self._create_findings_section(
                        consolidated_analysis['analysis']['findings']
                    ))
                
                if 'recommendations' in consolidated_analysis['analysis']:
                    story.extend(self._create_recommendations_section(
                        consolidated_analysis['analysis']['recommendations']
                    ))
        
        # Análisis por tarea
        story.append(PageBreak())
        heading = Paragraph("Análisis Detallado por Tarea", self.styles['CustomHeading'])
        story.append(heading)
        story.append(Spacer(1, 12))
        
        for task_name, analysis in tasks_analyses.items():
            task_heading = Paragraph(f"Tarea: {task_name}", self.styles['CustomHeading'])
            story.append(task_heading)
            
            if 'summary_short' in analysis:
                story.append(Paragraph(analysis['summary_short'], self.styles['CustomBody']))
            
            if 'analysis' in analysis and 'findings' in analysis['analysis']:
                findings = analysis['analysis']['findings']
                if findings:
                    story.append(Paragraph(
                        f"<b>Hallazgos encontrados:</b> {len(findings)}",
                        self.styles['CustomBody']
                    ))
            
            story.append(Spacer(1, 20))
        
        # Pie de página
        story.extend(self._create_footer())
        
        doc.build(story)
        
        return output_path
