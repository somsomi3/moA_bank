# import fontforge

# # 새 폰트 생성
# font = fontforge.font()
# font.fontname = "CustomFont"
# font.fullname = "Custom Font Example"
# font.familyname = "CustomFontFamily"

# # 글자 추가 (예: "A"를 추가)
# glyph = font.createChar(ord("A"))
# glyph.width = 1000
# pen = glyph.glyphPen()
# pen.moveTo((100, 100))
# pen.lineTo((500, 900))
# pen.lineTo((900, 100))
# pen.closePath()
# glyph.autoHint()

# # 저장
# font.generate("custom_font.ttf")
# print("custom_font.ttf has been created!")
