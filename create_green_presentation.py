#!/usr/bin/env python3
"""
Create a PowerPoint presentation about Going Green at Work
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor

def add_title_slide(prs, title, subtitle):
    """Add title slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_shape = slide.shapes.title
    subtitle_shape = slide.placeholders[1]
    
    title_shape.text = title
    subtitle_shape.text = subtitle
    
    # Style the title
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(44)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(34, 139, 34)  # Forest green
    
    return slide

def add_content_slide(prs, title, content_points):
    """Add content slide with bullet points"""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title_shape = slide.shapes.title
    body_shape = slide.placeholders[1]
    
    title_shape.text = title
    title_frame = title_shape.text_frame
    title_frame.paragraphs[0].font.size = Pt(36)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(34, 139, 34)
    
    text_frame = body_shape.text_frame
    text_frame.clear()
    
    for point in content_points:
        p = text_frame.add_paragraph()
        p.text = point
        p.level = 0
        p.font.size = Pt(18)
        p.space_after = Pt(12)
    
    return slide

def add_two_column_slide(prs, title, left_content, right_content):
    """Add slide with two columns"""
    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank layout
    
    # Add title
    left = Inches(0.5)
    top = Inches(0.5)
    width = Inches(9)
    height = Inches(0.8)
    
    title_box = slide.shapes.add_textbox(left, top, width, height)
    title_frame = title_box.text_frame
    title_frame.text = title
    title_frame.paragraphs[0].font.size = Pt(36)
    title_frame.paragraphs[0].font.bold = True
    title_frame.paragraphs[0].font.color.rgb = RGBColor(34, 139, 34)
    
    # Left column
    left_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.25), Inches(5))
    left_frame = left_box.text_frame
    left_frame.word_wrap = True
    
    for item in left_content:
        p = left_frame.add_paragraph()
        p.text = item
        p.font.size = Pt(16)
        p.space_after = Pt(10)
    
    # Right column
    right_box = slide.shapes.add_textbox(Inches(5.25), Inches(1.5), Inches(4.25), Inches(5))
    right_frame = right_box.text_frame
    right_frame.word_wrap = True
    
    for item in right_content:
        p = right_frame.add_paragraph()
        p.text = item
        p.font.size = Pt(16)
        p.space_after = Pt(10)
    
    return slide

def create_presentation():
    """Create the complete presentation"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    # Slide 1: Title
    add_title_slide(
        prs,
        "Going Green at Work",
        "Strategies for a Sustainable Future"
    )
    
    # Slide 2: Why Go Green?
    add_content_slide(
        prs,
        "Why Go Green at Work?",
        [
            "🌍 Environmental Impact: Reduce carbon footprint and protect natural resources",
            "💰 Cost Savings: Lower energy bills and operational expenses",
            "👥 Employee Engagement: Boost morale and attract eco-conscious talent",
            "📈 Brand Reputation: Enhance corporate image and customer loyalty",
            "⚖️ Regulatory Compliance: Meet environmental standards and regulations",
            "🔮 Future-Proofing: Prepare for climate-related business risks"
        ]
    )
    
    # Slide 3: Energy Efficiency
    add_content_slide(
        prs,
        "Energy Efficiency Strategies",
        [
            "💡 Switch to LED lighting throughout the office",
            "🌡️ Install smart thermostats and optimize HVAC systems",
            "🔌 Use energy-efficient appliances and equipment",
            "☀️ Maximize natural lighting with window placement",
            "⚡ Implement motion sensors for lighting in low-traffic areas",
            "🔋 Encourage powering down devices at end of day",
            "📊 Conduct regular energy audits to identify waste"
        ]
    )
    
    # Slide 4: Waste Reduction
    add_content_slide(
        prs,
        "Waste Reduction & Recycling",
        [
            "♻️ Establish comprehensive recycling programs (paper, plastic, metal, e-waste)",
            "📄 Go paperless: Digital documents, e-signatures, cloud storage",
            "☕ Eliminate single-use items: Reusable cups, utensils, containers",
            "🗑️ Implement composting for organic waste",
            "🎁 Choose products with minimal or recyclable packaging",
            "💻 Donate or recycle old electronics responsibly",
            "📦 Reuse shipping materials and office supplies"
        ]
    )
    
    # Slide 5: Sustainable Transportation
    add_content_slide(
        prs,
        "Green Transportation Options",
        [
            "🚴 Bike-to-work programs with secure storage and showers",
            "🚌 Public transit subsidies and incentives",
            "🚗 Carpooling initiatives and ride-sharing platforms",
            "🏠 Remote work and flexible schedules to reduce commuting",
            "🔌 Electric vehicle charging stations in parking lots",
            "🚶 Walking meetings for nearby destinations",
            "✈️ Virtual meetings to reduce business travel"
        ]
    )
    
    # Slide 6: Water Conservation
    add_content_slide(
        prs,
        "Water Conservation Measures",
        [
            "🚰 Install low-flow faucets and toilets",
            "💧 Fix leaks promptly to prevent water waste",
            "🌱 Use drought-resistant landscaping (xeriscaping)",
            "💦 Implement rainwater harvesting systems",
            "⏰ Smart irrigation systems with weather sensors",
            "🧼 Use water-efficient dishwashers and appliances",
            "📢 Educate employees on water-saving practices"
        ]
    )
    
    # Slide 7: Sustainable Procurement
    add_content_slide(
        prs,
        "Green Purchasing & Procurement",
        [
            "🌿 Choose eco-friendly office supplies (recycled paper, non-toxic cleaners)",
            "🏷️ Partner with sustainable vendors and suppliers",
            "🌾 Source local products to reduce transportation emissions",
            "✅ Look for environmental certifications (Energy Star, Fair Trade, FSC)",
            "📦 Buy in bulk to reduce packaging waste",
            "♻️ Select products made from recycled or renewable materials",
            "🔄 Prioritize durability and repairability over disposability"
        ]
    )
    
    # Slide 8: Green Office Design
    add_content_slide(
        prs,
        "Sustainable Office Design",
        [
            "🪴 Incorporate indoor plants for air quality and aesthetics",
            "🏢 Use sustainable building materials (bamboo, reclaimed wood)",
            "🪟 Maximize natural ventilation and daylighting",
            "🎨 Choose low-VOC paints and finishes",
            "🪑 Select furniture made from sustainable materials",
            "🌡️ Improve insulation to reduce heating/cooling needs",
            "🏗️ Pursue green building certifications (LEED, BREEAM)"
        ]
    )
    
    # Slide 9: Employee Engagement
    add_content_slide(
        prs,
        "Engaging Employees in Sustainability",
        [
            "📚 Provide regular training on green practices",
            "🏆 Create green teams or sustainability committees",
            "🎯 Set measurable sustainability goals and track progress",
            "🎁 Recognize and reward eco-friendly behaviors",
            "💡 Encourage employee suggestions for improvements",
            "📱 Use gamification to make sustainability fun",
            "🌍 Organize volunteer events for environmental causes"
        ]
    )
    
    # Slide 10: Technology Solutions
    add_content_slide(
        prs,
        "Technology for Sustainability",
        [
            "☁️ Cloud computing to reduce on-premise server energy use",
            "📊 Energy management software for monitoring and optimization",
            "📱 Digital collaboration tools to reduce paper and travel",
            "🤖 AI and IoT for smart building management",
            "♻️ E-waste recycling programs for old technology",
            "💻 Virtual desktops to extend hardware lifespan",
            "📈 Sustainability reporting platforms for transparency"
        ]
    )
    
    # Slide 11: Measuring Success
    add_two_column_slide(
        prs,
        "Measuring & Reporting Progress",
        [
            "📊 Key Metrics to Track:",
            "• Energy consumption (kWh)",
            "• Water usage (gallons)",
            "• Waste diverted from landfills (%)",
            "• Carbon emissions (tons CO2e)",
            "• Recycling rates (%)",
            "• Employee participation rates",
            "• Cost savings achieved"
        ],
        [
            "📝 Reporting Best Practices:",
            "• Publish annual sustainability reports",
            "• Share progress with stakeholders",
            "• Benchmark against industry standards",
            "• Use third-party verification",
            "• Celebrate milestones publicly",
            "• Be transparent about challenges",
            "• Set ambitious future targets"
        ]
    )
    
    # Slide 12: Challenges & Solutions
    add_two_column_slide(
        prs,
        "Overcoming Common Challenges",
        [
            "⚠️ Common Obstacles:",
            "• Initial investment costs",
            "• Resistance to change",
            "• Lack of awareness",
            "• Competing priorities",
            "• Limited resources",
            "• Measuring ROI",
            "• Maintaining momentum"
        ],
        [
            "✅ Solutions:",
            "• Start small, scale gradually",
            "• Demonstrate cost savings",
            "• Provide education and training",
            "• Secure leadership buy-in",
            "• Leverage grants and incentives",
            "• Track and communicate wins",
            "• Make it part of company culture"
        ]
    )
    
    # Slide 13: Case Studies
    add_content_slide(
        prs,
        "Success Stories",
        [
            "🏢 Google: 100% renewable energy, carbon-neutral since 2007",
            "🌲 Patagonia: 1% for the Planet, extensive recycling programs",
            "☕ Starbucks: LEED-certified stores, ethically sourced coffee",
            "🚗 Tesla: Electric vehicles, solar energy solutions",
            "📦 IKEA: Sustainable materials, circular business model",
            "💻 Microsoft: Carbon negative by 2030 commitment",
            "🏭 Interface: Mission Zero - zero environmental footprint"
        ]
    )
    
    # Slide 14: Action Plan
    add_content_slide(
        prs,
        "Creating Your Action Plan",
        [
            "1️⃣ Conduct a sustainability audit of current practices",
            "2️⃣ Set clear, measurable goals with timelines",
            "3️⃣ Secure leadership commitment and budget allocation",
            "4️⃣ Form a green team with representatives from all departments",
            "5️⃣ Prioritize quick wins for early momentum",
            "6️⃣ Implement changes systematically, starting with high-impact areas",
            "7️⃣ Monitor progress, adjust strategies, and celebrate successes"
        ]
    )
    
    # Slide 15: Resources
    add_content_slide(
        prs,
        "Helpful Resources",
        [
            "🌐 EPA Green Business Resources (epa.gov/greenbusiness)",
            "⭐ Energy Star for Business (energystar.gov)",
            "🏢 U.S. Green Building Council (usgbc.org)",
            "♻️ Zero Waste International Alliance (zwia.org)",
            "🌍 UN Sustainable Development Goals (sdgs.un.org)",
            "📊 Global Reporting Initiative (globalreporting.org)",
            "💼 B Corporation Certification (bcorporation.net)"
        ]
    )
    
    # Slide 16: Conclusion
    add_content_slide(
        prs,
        "The Path Forward",
        [
            "🌱 Every small action contributes to meaningful change",
            "🤝 Sustainability is a journey, not a destination",
            "💪 Employee engagement is key to success",
            "📈 Green practices benefit both planet and profit",
            "🌍 Your workplace can be a catalyst for positive environmental impact",
            "🚀 Start today - the future depends on actions we take now",
            "✨ Together, we can create a sustainable workplace for generations to come"
        ]
    )
    
    # Slide 17: Thank You
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    left = Inches(1)
    top = Inches(2.5)
    width = Inches(8)
    height = Inches(2)
    
    thank_you_box = slide.shapes.add_textbox(left, top, width, height)
    text_frame = thank_you_box.text_frame
    text_frame.text = "Thank You!"
    text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    text_frame.paragraphs[0].font.size = Pt(54)
    text_frame.paragraphs[0].font.bold = True
    text_frame.paragraphs[0].font.color.rgb = RGBColor(34, 139, 34)
    
    # Add subtitle
    p = text_frame.add_paragraph()
    p.text = "Let's Build a Sustainable Future Together"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(28)
    p.font.color.rgb = RGBColor(60, 179, 113)
    p.space_before = Pt(20)
    
    # Save presentation
    filename = "Going_Green_at_Work_Presentation.pptx"
    prs.save(filename)
    print(f"✅ Presentation created successfully: {filename}")
    print(f"📊 Total slides: {len(prs.slides)}")
    return filename

if __name__ == "__main__":
    create_presentation()
