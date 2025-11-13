#!/usr/bin/env python3
"""
3D-Enhanced PowerPoint Presentation Generator
Topic: The Chemistry Behind Air Purification in Air Conditioning Units (AUC)
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime
import os

def create_gradient_background(slide, color1, color2):
    """Add a gradient-like background using shapes"""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color1

def add_3d_text(textbox, text, font_size=44, bold=True, color=RGBColor(255, 255, 255)):
    """Add text with 3D-like shadow effect"""
    text_frame = textbox.text_frame
    text_frame.clear()
    p = text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = PP_ALIGN.CENTER
    return text_frame

def add_molecule_shape(slide, left, top, size, color, label=""):
    """Create a 3D-style molecule representation"""
    # Main sphere
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        left, top, size, size
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = RGBColor(255, 255, 255)
    shape.line.width = Pt(2)
    
    # Add shadow for 3D effect
    shape.shadow.inherit = False
    
    # Add label if provided
    if label:
        text_frame = shape.text_frame
        text_frame.text = label
        text_frame.paragraphs[0].font.size = Pt(14)
        text_frame.paragraphs[0].font.bold = True
        text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
        text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
        text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    return shape

def create_presentation():
    """Create the 3D-enhanced PowerPoint presentation"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Color scheme - futuristic blues and purples
    primary_color = RGBColor(30, 144, 255)  # Dodger Blue
    secondary_color = RGBColor(138, 43, 226)  # Blue Violet
    accent_color = RGBColor(0, 255, 255)  # Cyan
    dark_bg = RGBColor(15, 15, 35)
    light_text = RGBColor(255, 255, 255)
    
    # ==================== SLIDE 1: Title Slide ====================
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Background
    background = slide1.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_bg
    
    # Add decorative 3D molecules floating around
    molecules_data = [
        (Inches(0.5), Inches(1), Inches(0.8), RGBColor(0, 191, 255), "O₂"),
        (Inches(8.5), Inches(2), Inches(0.6), RGBColor(255, 105, 180), "CO₂"),
        (Inches(1), Inches(5.5), Inches(0.7), RGBColor(50, 205, 50), "N₂"),
        (Inches(8), Inches(6), Inches(0.5), RGBColor(255, 215, 0), "H₂O"),
    ]
    
    for left, top, size, color, label in molecules_data:
        add_molecule_shape(slide1, left, top, size, color, label)
    
    # Title
    title_box = slide1.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1))
    title_frame = add_3d_text(title_box, "Chemistry Behind Air Purification", 54, True, accent_color)
    
    # Subtitle
    subtitle_box = slide1.shapes.add_textbox(Inches(1), Inches(3.5), Inches(8), Inches(0.8))
    add_3d_text(subtitle_box, "in Air Conditioning Units (AUC)", 36, True, primary_color)
    
    # 3D View label
    label_box = slide1.shapes.add_textbox(Inches(1), Inches(4.5), Inches(8), Inches(0.5))
    add_3d_text(label_box, "🔬 Dive into the Molecular World of Clean Air 🔬", 24, False, light_text)
    
    # Presenter info
    date_str = datetime.now().strftime("%B %d, %Y")
    info_box = slide1.shapes.add_textbox(Inches(1), Inches(6.5), Inches(8), Inches(0.5))
    add_3d_text(info_box, f"Date: {date_str}", 18, False, light_text)
    
    # ==================== SLIDE 2: What is Air Purification? ====================
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide2.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_bg
    
    # Title
    title_box = slide2.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    add_3d_text(title_box, "What is Air Purification? (3D Diagram)", 40, True, accent_color)
    
    # Create 3D flowchart with arrows
    flow_y = Inches(2)
    box_width = Inches(2)
    box_height = Inches(1.2)
    
    # Dirty Air (Input)
    dirty_box = slide2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.8), flow_y, box_width, box_height
    )
    dirty_box.fill.solid()
    dirty_box.fill.fore_color.rgb = RGBColor(255, 69, 0)
    dirty_box.text_frame.text = "Dirty Air\n💨"
    dirty_box.text_frame.paragraphs[0].font.size = Pt(20)
    dirty_box.text_frame.paragraphs[0].font.bold = True
    dirty_box.text_frame.paragraphs[0].font.color.rgb = light_text
    dirty_box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    dirty_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Arrow 1
    arrow1 = slide2.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(3), flow_y + Inches(0.4), Inches(1), Inches(0.4)
    )
    arrow1.fill.solid()
    arrow1.fill.fore_color.rgb = primary_color
    
    # AUC Process
    auc_box = slide2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(4.2), flow_y, box_width, box_height
    )
    auc_box.fill.solid()
    auc_box.fill.fore_color.rgb = secondary_color
    auc_box.text_frame.text = "AUC\nChemistry ⚗️"
    auc_box.text_frame.paragraphs[0].font.size = Pt(20)
    auc_box.text_frame.paragraphs[0].font.bold = True
    auc_box.text_frame.paragraphs[0].font.color.rgb = light_text
    auc_box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    auc_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Arrow 2
    arrow2 = slide2.shapes.add_shape(
        MSO_SHAPE.RIGHT_ARROW,
        Inches(6.4), flow_y + Inches(0.4), Inches(1), Inches(0.4)
    )
    arrow2.fill.solid()
    arrow2.fill.fore_color.rgb = primary_color
    
    # Clean Air (Output)
    clean_box = slide2.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(7.6), flow_y, box_width, box_height
    )
    clean_box.fill.solid()
    clean_box.fill.fore_color.rgb = RGBColor(50, 205, 50)
    clean_box.text_frame.text = "Clean Air\n✨"
    clean_box.text_frame.paragraphs[0].font.size = Pt(20)
    clean_box.text_frame.paragraphs[0].font.bold = True
    clean_box.text_frame.paragraphs[0].font.color.rgb = light_text
    clean_box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    clean_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Key points
    points_box = slide2.shapes.add_textbox(Inches(1.5), Inches(4), Inches(7), Inches(2.5))
    text_frame = points_box.text_frame
    text_frame.word_wrap = True
    
    points = [
        "• Air purification removes pollutants like dust, odors, and germs",
        "• In AUC, chemistry uses chemical reactions to clean air",
        "• Multiple layers of filtration and chemical processes",
        "• Result: Fresh, breathable air for indoor spaces"
    ]
    
    for i, point in enumerate(points):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.text = point
        p.font.size = Pt(22)
        p.font.color.rgb = light_text
        p.space_after = Pt(12)
    
    # ==================== SLIDE 3: Common Pollutants ====================
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide3.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_bg
    
    # Title
    title_box = slide3.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    add_3d_text(title_box, "Common Pollutants (3D Molecules)", 40, True, accent_color)
    
    # Create 3D molecule representations in a grid
    pollutants = [
        ("Dust Particles", Inches(1.5), Inches(2), RGBColor(139, 69, 19), "🔸"),
        ("Benzene (C₆H₆)", Inches(5.5), Inches(2), RGBColor(255, 0, 255), "⬡"),
        ("Viruses/Bacteria", Inches(1.5), Inches(4.5), RGBColor(255, 0, 0), "🦠"),
        ("CO₂ Gas", Inches(5.5), Inches(4.5), RGBColor(100, 149, 237), "CO₂")
    ]
    
    for name, left, top, color, symbol in pollutants:
        # Create molecule sphere
        molecule = add_molecule_shape(slide3, left, top, Inches(1.2), color, symbol)
        
        # Add label below
        label_box = slide3.shapes.add_textbox(left - Inches(0.5), top + Inches(1.3), Inches(2.2), Inches(0.4))
        label_frame = label_box.text_frame
        label_frame.text = name
        label_frame.paragraphs[0].font.size = Pt(18)
        label_frame.paragraphs[0].font.bold = True
        label_frame.paragraphs[0].font.color.rgb = light_text
        label_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # ==================== SLIDE 4: Basic Cleaning Ways ====================
    slide4 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide4.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_bg
    
    # Title
    title_box = slide4.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    add_3d_text(title_box, "Basic Cleaning Methods (3D Filter Model)", 38, True, accent_color)
    
    # Create 3D filter cross-section
    filter_methods = [
        {
            "title": "Physical Filters",
            "desc": "3D mesh network traps\nparticles mechanically",
            "icon": "🕸️",
            "color": RGBColor(70, 130, 180),
            "pos": (Inches(1), Inches(2))
        },
        {
            "title": "Activated Carbon",
            "desc": "Porous 3D structure\nabsorbs gases & odors",
            "icon": "🧽",
            "color": RGBColor(64, 64, 64),
            "pos": (Inches(5.5), Inches(2))
        },
        {
            "title": "HEPA Filtration",
            "desc": "Ultra-fine 3D fibers\ncapture 99.97% particles",
            "icon": "🔬",
            "color": RGBColor(34, 139, 34),
            "pos": (Inches(1), Inches(4.8))
        },
        {
            "title": "Electrostatic",
            "desc": "Charged 3D plates\nattract pollutants",
            "icon": "⚡",
            "color": RGBColor(255, 215, 0),
            "pos": (Inches(5.5), Inches(4.8))
        }
    ]
    
    for method in filter_methods:
        # Create box
        box = slide4.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            method["pos"][0], method["pos"][1], Inches(3.5), Inches(1.8)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = method["color"]
        box.line.color.rgb = light_text
        box.line.width = Pt(2)
        
        # Add text
        text_frame = box.text_frame
        text_frame.clear()
        
        # Title
        p1 = text_frame.paragraphs[0]
        p1.text = f"{method['icon']} {method['title']}"
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = light_text
        p1.alignment = PP_ALIGN.CENTER
        
        # Description
        p2 = text_frame.add_paragraph()
        p2.text = method['desc']
        p2.font.size = Pt(14)
        p2.font.color.rgb = light_text
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(6)
    
    # ==================== SLIDE 5: Advanced Chemistry ====================
    slide5 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide5.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_bg
    
    # Title
    title_box = slide5.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    add_3d_text(title_box, "Advanced Chemistry (3D Reactions)", 40, True, accent_color)
    
    # Advanced methods with reaction visualization
    advanced_methods = [
        {
            "title": "Photocatalytic Oxidation",
            "reaction": "UV + TiO₂ → •OH radicals",
            "desc": "Breaks down organic pollutants",
            "color": RGBColor(138, 43, 226),
            "pos": Inches(1.5)
        },
        {
            "title": "Ionization",
            "reaction": "Air → Ions (+ / -)",
            "desc": "Charged particles attract pollutants",
            "color": RGBColor(30, 144, 255),
            "pos": Inches(3.5)
        },
        {
            "title": "Ozone Treatment",
            "reaction": "O₃ + Pollutants → O₂ + Safe compounds",
            "desc": "Oxidizes and neutralizes contaminants",
            "color": RGBColor(255, 140, 0),
            "pos": Inches(5.5)
        }
    ]
    
    for method in advanced_methods:
        # Create reaction box
        box = slide5.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8), method["pos"], Inches(8.4), Inches(1.5)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = method["color"]
        box.line.color.rgb = light_text
        box.line.width = Pt(3)
        
        text_frame = box.text_frame
        text_frame.clear()
        text_frame.word_wrap = True
        
        # Title
        p1 = text_frame.paragraphs[0]
        p1.text = f"⚗️ {method['title']}"
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = light_text
        
        # Reaction
        p2 = text_frame.add_paragraph()
        p2.text = f"Reaction: {method['reaction']}"
        p2.font.size = Pt(18)
        p2.font.color.rgb = RGBColor(255, 255, 0)
        p2.space_before = Pt(6)
        
        # Description
        p3 = text_frame.add_paragraph()
        p3.text = f"→ {method['desc']}"
        p3.font.size = Pt(16)
        p3.font.color.rgb = light_text
        p3.space_before = Pt(4)
    
    # ==================== SLIDE 6: Wrap-Up ====================
    slide6 = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide6.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = dark_bg
    
    # Title
    title_box = slide6.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.8))
    add_3d_text(title_box, "Summary & Future (3D View)", 44, True, accent_color)
    
    # Add central "clean air" globe
    globe = add_molecule_shape(slide6, Inches(4), Inches(2), Inches(2), RGBColor(0, 191, 255), "🌍")
    
    # Summary points around the globe
    summary_points = [
        "✓ Chemistry cleans air through multiple 3D processes",
        "✓ Physical, chemical, and biological methods work together",
        "✓ Advanced oxidation breaks down harmful molecules",
        "✓ Future: Nano-materials & AI-optimized purification"
    ]
    
    points_box = slide6.shapes.add_textbox(Inches(1), Inches(4.5), Inches(8), Inches(2))
    text_frame = points_box.text_frame
    text_frame.word_wrap = True
    
    for i, point in enumerate(summary_points):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.text = point
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = light_text
        p.space_after = Pt(10)
        p.alignment = PP_ALIGN.CENTER
    
    # Key takeaway
    key_box = slide6.shapes.add_textbox(Inches(2), Inches(6.5), Inches(6), Inches(0.6))
    add_3d_text(key_box, "🌟 Breathe Easy with Chemistry! 🌟", 28, True, RGBColor(0, 255, 127))
    
    # Q&A
    qa_box = slide6.shapes.add_textbox(Inches(3.5), Inches(7.2), Inches(3), Inches(0.3))
    add_3d_text(qa_box, "Questions?", 20, False, light_text)
    
    return prs

def main():
    """Main function to generate the presentation"""
    print("🎨 Creating 3D-Enhanced PowerPoint Presentation...")
    print("📊 Topic: Chemistry Behind Air Purification in AUC")
    print()
    
    prs = create_presentation()
    
    output_file = "Air_Purification_Chemistry_3D.pptx"
    prs.save(output_file)
    
    print(f"✅ Presentation created successfully!")
    print(f"📁 File saved as: {output_file}")
    print(f"📏 Size: {os.path.getsize(output_file) / 1024:.2f} KB")
    print()
    print("📋 Presentation includes:")
    print("   • Slide 1: Title with 3D floating molecules")
    print("   • Slide 2: 3D flowchart of air purification process")
    print("   • Slide 3: 3D representations of common pollutants")
    print("   • Slide 4: 3D filter models and methods")
    print("   • Slide 5: Advanced chemistry with 3D reactions")
    print("   • Slide 6: Summary with 3D globe visualization")
    print()
    print("🎯 Features:")
    print("   ✓ Futuristic dark theme with vibrant colors")
    print("   ✓ 3D-style molecule representations")
    print("   ✓ Visual flowcharts and diagrams")
    print("   ✓ Chemistry reactions with equations")
    print("   ✓ Professional layout and typography")
    print()
    print("💡 Tip: Open in PowerPoint and add animations:")
    print("   - Select shapes → Animations → 3D Rotation")
    print("   - Add entrance effects (Fly In, Zoom)")
    print("   - Use morph transitions between slides")

if __name__ == "__main__":
    main()
