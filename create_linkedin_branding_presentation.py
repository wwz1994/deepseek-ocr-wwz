#!/usr/bin/env python3
"""
Script to create a French presentation about LinkedIn Personal Branding
for Digital Marketing students
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

def create_presentation():
    # Create presentation object
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Define LinkedIn brand colors
    LINKEDIN_BLUE = RGBColor(0, 119, 181)
    DARK_GRAY = RGBColor(40, 40, 40)
    LIGHT_GRAY = RGBColor(245, 245, 245)
    WHITE = RGBColor(255, 255, 255)
    
    # Slide 1: Title Slide
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank layout
    
    # Add background color
    background = slide1.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = LINKEDIN_BLUE
    
    # Title
    title_box = slide1.shapes.add_textbox(Inches(1), Inches(2.5), Inches(8), Inches(1))
    title_frame = title_box.text_frame
    title_frame.text = "Personal Branding sur LinkedIn"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(54)
    title_para.font.bold = True
    title_para.font.color.rgb = WHITE
    title_para.alignment = PP_ALIGN.CENTER
    
    # Subtitle
    subtitle_box = slide1.shapes.add_textbox(Inches(1), Inches(3.8), Inches(8), Inches(0.8))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.text = "Guide Pratique pour Étudiants en Marketing Digital"
    subtitle_para = subtitle_frame.paragraphs[0]
    subtitle_para.font.size = Pt(24)
    subtitle_para.font.color.rgb = WHITE
    subtitle_para.alignment = PP_ALIGN.CENTER
    
    # Slide 2: Pourquoi LinkedIn?
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide2.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "Pourquoi LinkedIn est Essentiel?"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = LINKEDIN_BLUE
    
    # Content
    content_box = slide2.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    points = [
        "🌐 Plus de 900 millions d'utilisateurs dans le monde",
        "💼 Le réseau professionnel n°1 pour le marketing digital",
        "🎯 80% des leads B2B proviennent de LinkedIn",
        "📈 Visibilité auprès des recruteurs et entreprises",
        "🤝 Opportunités de networking et de collaboration",
        "📚 Plateforme d'apprentissage et de veille sectorielle"
    ]
    
    for point in points:
        p = content_frame.add_paragraph()
        p.text = point
        p.font.size = Pt(22)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(12)
        p.level = 0
    
    # Slide 3: Les Piliers du Personal Branding
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide3.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "Les 4 Piliers du Personal Branding"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = LINKEDIN_BLUE
    
    # Four pillars in boxes
    pillars = [
        ("1. IDENTITÉ", "Qui êtes-vous?\nVos valeurs et expertise"),
        ("2. VISIBILITÉ", "Être vu et reconnu\npar votre audience"),
        ("3. CRÉDIBILITÉ", "Prouver votre expertise\navec du contenu de qualité"),
        ("4. RÉSEAU", "Construire des relations\nauthentiques et durables")
    ]
    
    x_positions = [0.8, 5.3, 0.8, 5.3]
    y_positions = [2, 2, 4.5, 4.5]
    
    for i, (title, desc) in enumerate(pillars):
        # Box background
        box = slide3.shapes.add_shape(
            1,  # Rectangle
            Inches(x_positions[i]),
            Inches(y_positions[i]),
            Inches(3.8),
            Inches(2)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = LINKEDIN_BLUE
        box.line.width = Pt(2)
        
        # Title
        text_frame = box.text_frame
        text_frame.clear()
        p1 = text_frame.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = LINKEDIN_BLUE
        p1.alignment = PP_ALIGN.CENTER
        
        # Description
        p2 = text_frame.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(14)
        p2.font.color.rgb = DARK_GRAY
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(8)
    
    # Slide 4: Optimiser Votre Profil
    slide4 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide4.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "Optimiser Votre Profil LinkedIn"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = LINKEDIN_BLUE
    
    # Content
    content_box = slide4.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5.2))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    sections = [
        ("📸 Photo Professionnelle", "Visage visible, souriant, fond neutre"),
        ("🎨 Bannière Personnalisée", "Reflète votre domaine d'expertise en marketing digital"),
        ("✍️ Titre Accrocheur", "Pas seulement votre poste, mais votre valeur ajoutée"),
        ("📝 Résumé Impactant", "Votre histoire, compétences et objectifs en 3-5 paragraphes"),
        ("🎓 Expériences & Formation", "Détaillées avec résultats mesurables"),
        ("💡 Compétences & Recommandations", "Minimum 10 compétences validées par votre réseau")
    ]
    
    for section_title, section_desc in sections:
        p = content_frame.add_paragraph()
        p.text = section_title
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = LINKEDIN_BLUE
        p.space_before = Pt(10)
        
        p2 = content_frame.add_paragraph()
        p2.text = section_desc
        p2.font.size = Pt(16)
        p2.font.color.rgb = DARK_GRAY
        p2.level = 1
    
    # Slide 5: Stratégie de Contenu
    slide5 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide5.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "Créer du Contenu qui Engage"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = LINKEDIN_BLUE
    
    # Left column - Types de contenu
    left_box = slide5.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(4), Inches(5))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True
    
    p = left_frame.paragraphs[0]
    p.text = "Types de Contenu:"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = LINKEDIN_BLUE
    
    content_types = [
        "📊 Études de cas",
        "💭 Réflexions personnelles",
        "📰 Actualités du secteur",
        "🎓 Conseils pratiques",
        "🎥 Vidéos courtes",
        "📈 Infographies"
    ]
    
    for content_type in content_types:
        p = left_frame.add_paragraph()
        p.text = content_type
        p.font.size = Pt(18)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(8)
    
    # Right column - Best practices
    right_box = slide5.shapes.add_textbox(Inches(5.2), Inches(1.8), Inches(4), Inches(5))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True
    
    p = right_frame.paragraphs[0]
    p.text = "Bonnes Pratiques:"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = LINKEDIN_BLUE
    
    best_practices = [
        "✅ Publier 2-3 fois/semaine",
        "✅ Utiliser des hashtags (3-5)",
        "✅ Poser des questions",
        "✅ Partager des visuels",
        "✅ Commenter d'autres posts",
        "✅ Être authentique"
    ]
    
    for practice in best_practices:
        p = right_frame.add_paragraph()
        p.text = practice
        p.font.size = Pt(18)
        p.font.color.rgb = DARK_GRAY
        p.space_before = Pt(8)
    
    # Slide 6: Développer Votre Réseau
    slide6 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide6.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "Développer Votre Réseau Stratégiquement"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = LINKEDIN_BLUE
    
    # Content
    content_box = slide6.shapes.add_textbox(Inches(1), Inches(1.8), Inches(8), Inches(5))
    content_frame = content_box.text_frame
    content_frame.word_wrap = True
    
    networking_tips = [
        ("🎯 Cibler les Bonnes Personnes", 
         "Professionnels du marketing digital, recruteurs, alumni, leaders d'opinion"),
        ("💬 Personnaliser Vos Invitations", 
         "Expliquez pourquoi vous souhaitez vous connecter"),
        ("🤝 Engager Authentiquement", 
         "Commenter, partager, féliciter - créer de vraies interactions"),
        ("👥 Rejoindre des Groupes", 
         "Groupes de marketing digital, communautés d'étudiants"),
        ("📅 Participer aux Événements", 
         "Webinaires, conférences LinkedIn Live"),
        ("🔄 Donner Avant de Recevoir", 
         "Aider les autres, partager des opportunités")
    ]
    
    for tip_title, tip_desc in networking_tips:
        p = content_frame.add_paragraph()
        p.text = tip_title
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = LINKEDIN_BLUE
        p.space_before = Pt(12)
        
        p2 = content_frame.add_paragraph()
        p2.text = tip_desc
        p2.font.size = Pt(16)
        p2.font.color.rgb = DARK_GRAY
        p2.level = 1
    
    # Slide 7: Plan d'Action
    slide7 = prs.slides.add_slide(prs.slide_layouts[6])
    
    # Title
    title_box = slide7.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.text = "Votre Plan d'Action - 30 Jours"
    title_para = title_frame.paragraphs[0]
    title_para.font.size = Pt(40)
    title_para.font.bold = True
    title_para.font.color.rgb = LINKEDIN_BLUE
    
    # Timeline boxes
    weeks = [
        ("Semaine 1", [
            "Optimiser votre profil complet",
            "Ajouter 50 connexions pertinentes"
        ]),
        ("Semaine 2", [
            "Publier votre premier post",
            "Commenter 10 publications/jour"
        ]),
        ("Semaine 3", [
            "Rejoindre 5 groupes professionnels",
            "Publier 2-3 contenus originaux"
        ]),
        ("Semaine 4", [
            "Analyser vos statistiques",
            "Ajuster votre stratégie"
        ])
    ]
    
    y_pos = 1.8
    for week_title, tasks in weeks:
        # Week box
        box = slide7.shapes.add_shape(
            1,  # Rectangle
            Inches(1),
            Inches(y_pos),
            Inches(8),
            Inches(1.2)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = LIGHT_GRAY
        box.line.color.rgb = LINKEDIN_BLUE
        box.line.width = Pt(2)
        
        text_frame = box.text_frame
        text_frame.clear()
        text_frame.margin_left = Inches(0.2)
        text_frame.margin_top = Inches(0.1)
        
        # Week title
        p1 = text_frame.paragraphs[0]
        p1.text = week_title
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = LINKEDIN_BLUE
        
        # Tasks
        for task in tasks:
            p = text_frame.add_paragraph()
            p.text = f"• {task}"
            p.font.size = Pt(16)
            p.font.color.rgb = DARK_GRAY
            p.level = 1
        
        y_pos += 1.35
    
    # Save presentation
    output_file = "/vercel/sandbox/linkedin_branding_french_presentation.pptx"
    prs.save(output_file)
    print(f"✅ Présentation créée avec succès: {output_file}")
    print(f"📊 7 diapositives sur le Personal Branding LinkedIn en français")
    return output_file

if __name__ == "__main__":
    create_presentation()
