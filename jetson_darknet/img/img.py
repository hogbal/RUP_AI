import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def create_img(text, font_size, fh):
    img = Image.open("src/alltalk_bg.png")
    
    font = ImageFont.truetype("src/1534704.ttf", font_size, encoding="UTF-8")
    draw = ImageDraw.Draw(img)
    text_size = font.getsize(text)
    
    width, heigth = img.size
    
    org = ((width-text_size[0])//2, int(heigth*fh))
    draw.text(org,text,font=font,fill=(0,0,0))
    img = np.array(img)
    
    return img

def create_phone_img(img, text, font_size, notice=False, color=(0,0,0)):
    img = Image.fromarray(img)
  
    font = ImageFont.truetype("src/1534704.ttf", font_size, encoding="UTF-8")
    draw = ImageDraw.Draw(img)
    text_size = font.getsize(text)
    
    width, heigth = img.size
    
    org=((width - text_size[0])//2,int(heigth*0.75))
    draw.text(org,text,font=font,fill=color)
    
    if(notice):
        text = "다시 입력해주세요!"
        font = ImageFont.truetype("src/1534704.ttf", font_size//3, encoding="UTF-8")
        draw = ImageDraw.Draw(img)
        text_size = font.getsize(text)
        
        width, heigth = img.size
        
        org=((width - text_size[0])//2,int(heigth*0.85))
        draw.text(org,text,font=font,fill=(0,0,255))
    
    img = np.array(img)
    
    return img

def create_info_img(text1, text2, font_size):
    img = Image.open("src/alltalk_bg.png")
    
    font = ImageFont.truetype("src/1534704.ttf", font_size, encoding="UTF-8")
    draw = ImageDraw.Draw(img)
    text_size1 = font.getsize(text1)
    text_size2 = font.getsize(text2)
    
    width, heigth = img.size
    
    org1=((width - text_size1[0])//2,int(heigth*0.65))
    draw.text(org1,text1,font=font,fill=(0,0,0))
    
    org2=((width - text_size2[0])//2,int(heigth*0.8))
    draw.text(org2,text2,font=font,fill=(0,0,0))
    
    img = np.array(img)
    
    return img

def create_result_img(num, font_size):
    img = Image.open("src/alltalk_bg.png")
    
    text1 = "감사합니다."
    text2 = f"환경보호 참여자 수 {num}명"
    
    font = ImageFont.truetype("src/1534704.ttf", font_size, encoding="UTF-8")
    draw = ImageDraw.Draw(img)
    text_size1 = font.getsize(text1)
    text_size2 = font.getsize(text2)
    
    width, heigth = img.size
    
    org1=((width - text_size1[0])//2,int(heigth*0.65))
    draw.text(org1,text1,font=font,fill=(0,0,0))
    
    org2=((width - text_size2[0])//2,int(heigth*0.8))
    draw.text(org2,text2,font=font,fill=(0,0,0))
    
    img = np.array(img)
    
    return img