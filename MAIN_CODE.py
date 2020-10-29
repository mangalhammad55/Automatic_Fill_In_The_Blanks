
"""
Created on Sun Oct 25 13:47:49 2020

@author:Mangal Prasad Hammad (NITK)
"""

#FINAL CODE 

import cv2 
import math
from PIL import Image
import pytesseract 
from fitbert import FitBert



#PLEASE SPECIFY THE IMAGE HERE
img = cv2.imread('nitk_1.jpg')
img2= Image.open('nitk_1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
 
ret,thresh = cv2.threshold(gray,127,255,1) 
 
contours,h = cv2.findContours(thresh,1,2) 

for cnt in contours: 
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True) 
    if len(approx)==4: 
        min1 = 0
        min2 = 0
        max1 = 0
        max2 = 0
        min_dis = 9999999
        max_dis = 0
            
        for i in approx:
            
            
            dis = math.sqrt(i[0][0]**2+i[0][1]**2)
            
            if dis<min_dis:
                min_dis=dis
                min1=i[0][0]
                min2=i[0][1]
            
            if dis>max_dis:
                max_dis=dis
                max1=i[0][0]
                max2=i[0][1]
        
        area=math.sqrt((approx[0][0][0]-approx[1][0][0])**2 +(approx[0][0][1]-approx[1][0][1])**2)
        area=area*math.sqrt((approx[1][0][0]-approx[2][0][0])**2 +(approx[1][0][1]-approx[2][0][1])**2)
        
        if area>100000:
            crop_img = img2.crop((min1,min2,max1,max2))
            crop_img.save("cropped_img.jpg")
            print("IMAGE CROPPED")
            
            
#EXTRACTION OF ANSWERS FROM CROPPED IMAGE


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


img = cv2.imread("cropped_img.jpg") 


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 


ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10)) 


dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 


contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
												cv2.CHAIN_APPROX_NONE) 


im2 = img.copy() 


file = open("options.txt", "w+") 
file.write("") 
file.close() 

for cnt in contours: 
	x, y, w, h = cv2.boundingRect(cnt) 
	
	
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
	
	
	cropped = im2[y:y + h, x:x + w] 
	
	
	file = open("options.txt", "a") 
	
	 
	text = pytesseract.image_to_string(cropped) 
	    
	
	file.write(text) 
	file.write("\n") 
	
	file.close 
    

#EXTRACTING OPTIONS IN A LIST
    
lines = open('options.txt').read().splitlines()
filter_object = filter(lambda x:x != "",lines)
new_lines = list(filter_object)
filter_object = filter(lambda x:x != " ",new_lines)
opts = list(filter_object)

print("OPTIONS EXTRACTED")

#EXTRACTING QUESTIONS FROM THE IMAGE

# Read image from which text needs to be extracted 

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


img = cv2.imread("nitk_1.jpg") 


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 


ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV) 

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18)) 


dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1) 


contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, 
												cv2.CHAIN_APPROX_NONE) 


im2 = img.copy() 


file = open("questions.txt", "w+") 
file.write("") 
file.close() 

for cnt in contours: 
	x, y, w, h = cv2.boundingRect(cnt) 
	
	
	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2) 
	
	
	cropped = im2[y:y + h, x:x + w] 
	
	
	file = open("questions.txt", "a") 
	
	 
	text = pytesseract.image_to_string(cropped) 
	    
	
	file.write(text) 
	file.write("\n") 
	
	file.close 
    
    
#EXTRACTING QUESTIONS IN A LIST
    
ques = []
lines = open('questions.txt').read().splitlines()
filter_object = filter(lambda x:x != "",lines)
new_lines = list(filter_object)
filter_object = filter(lambda x:x != " ",new_lines)
questions = list(filter_object)


for i in range(len(questions)):
    temp = ""
    questions[i] = questions[i].replace('|','I',1)
    if questions[i][0].isdigit():
        temp = questions[i]
        if (i+1)<len(questions):
            temp = temp + " ***mask*** "
        if questions[i+1][0].isalpha():
            temp = temp + questions[i+1]
    if temp != "":
        ques.append(temp)
        
ques.reverse()
print("QUESTIONS EXTRACTED")

print(ques)
print(opts)


file = open("answers.txt", "w+") 
file.write("") 
file.close() 

#FILLING THE BLANKS USING FITBERT

file = open("answers.txt", "w+") 
file.write("") 
file.close() 

fb = FitBert()

for sentence in ques:
    masked_string = sentence
    options = opts
    filled_in = fb.fitb(masked_string, options=options)
    file = open("answers.txt", "a") 
    file.write(filled_in) 
    file.write("\n") 
    file.close()
    
    
