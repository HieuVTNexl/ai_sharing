# from turtle import left
import cv2
import time
import numpy as np

class CV2Effect():

    def __init__(self, fadeSteps=5, warningBlinkTime=0.5):
        self.fadeSteps = fadeSteps
        self.crrFadeStep = fadeSteps
        self.warningBlinkTime = warningBlinkTime
        self.previousWarning = 0
        self.isShowWarning = True

    def rectangle(self, img, startPoint, endPoint, color, thickess, lineRatio=0.1):

        left, top       = startPoint
        right, bottom   = endPoint

        verticalLength     = bottom - top
        horizontalLength   = right - left

        boxHorizontalLength = int(horizontalLength * lineRatio)
        boxVerticalLength   = int(verticalLength   * lineRatio)

        img = cv2.line(img, (left,top), (left+boxHorizontalLength,top), color, thickess)
        img = cv2.line(img, (left,top), (left,top+boxVerticalLength), color, thickess)

        img = cv2.line(img, (left+horizontalLength,top), (left+horizontalLength-boxHorizontalLength,top), color, thickess)
        img = cv2.line(img, (left+horizontalLength,top), (left+horizontalLength,top+boxVerticalLength), color, thickess)
        
        img = cv2.line(img, (left,bottom), (left,bottom-boxVerticalLength), color, thickess)
        img = cv2.line(img, (left,bottom), (left+boxHorizontalLength,bottom), color, thickess)

        img = cv2.line(img, (right,bottom), (right-boxHorizontalLength,bottom), color, thickess)
        img = cv2.line(img, (right,bottom), (right,bottom-boxVerticalLength), color, thickess)
        
        return img

    def putText(self, img, text, startPoint, endPoint, color, fontScale=0.8, thickness=2, font = cv2.FONT_HERSHEY_SIMPLEX):
        left, top       = startPoint
        right, bottom   = endPoint

        textSize = cv2.getTextSize(text, font, fontScale, thickness)[0]

        textWidth  = textSize[0]
        textHeight = textSize[1]

        textX = left + ((right-left - textWidth) // 2)
        textY = top  - 10

        # Fill text with rectangle
        # img = cv2.rectangle(img, (left,top-textHeight-15), (right,top), (255,0,0), -1)

        img = cv2.putText(img, text, (textX, textY), font, fontScale, color, 2, cv2.LINE_AA)
        return img

    def putTextInRect(self, img, text, startPoint, endPoint, color, fontScale=0.8, thickness=2, font = cv2.FONT_HERSHEY_SIMPLEX):
        left, top       = startPoint
        right, bottom   = endPoint

        textSize = cv2.getTextSize(text, font, fontScale, thickness)[0]

        textWidth  = textSize[0]
        textHeight = textSize[1]

        textX = left + ((right-left - textWidth)  // 2)
        textY = top  + ((bottom-top - textHeight) // 2) + 10

        img = cv2.putText(img, text, (textX, textY), font, fontScale, color, 2, cv2.LINE_AA)
        return img

    def rectangleWithText(self, img, text, startPoint, endPoint, color, thickess, lineRatio=0.1):
        img = self.rectangle(img, startPoint, endPoint, color, thickess, lineRatio)
        img = self.putText(img, text, startPoint, endPoint, color)
        return img

    def rectangleWithTextFade(self, img, text, startPoint, endPoint, color, thickess, lineRatio=0.1):
        tempImg = img.copy()

        left, top       = startPoint
        right, bottom   = endPoint

        left   = left   - int(left * (self.crrFadeStep/10))
        top    = top    - int(top * (self.crrFadeStep/10))
        right  = right  + int(right * (self.crrFadeStep/10))
        bottom = bottom + int(bottom * (self.crrFadeStep/10))

        tempImg = self.rectangle(tempImg, (left,top), (right,bottom), color, thickess, lineRatio)
        tempImg = self.putText(tempImg, text, (left,top), (right,bottom), color) 

        # Reset step
        self.crrFadeStep -= 1
        if self.crrFadeStep < 0:
            self.crrFadeStep = self.fadeSteps
            
        return tempImg

    def rectangleFade(self, img, startPoint, endPoint, color, thickess, lineRatio=0.1):
        tempImg = img.copy()

        left, top       = startPoint
        right, bottom   = endPoint

        left   = left   - int(left * (self.crrFadeStep/10))
        top    = top    - int(top * (self.crrFadeStep/10))
        right  = right  + int(right * (self.crrFadeStep/10))
        bottom = bottom + int(bottom * (self.crrFadeStep/10))

        tempImg = self.rectangle(tempImg, (left,top), (right,bottom), color, thickess, lineRatio)

        # Reset step
        self.crrFadeStep -= 1
        if self.crrFadeStep < 0:
            self.crrFadeStep = self.fadeSteps

        return tempImg

    def warningRectangle(self, text, src, leftTop, rightBottom, radius=1, color=(51, 51, 51), thickness=-1, lineType=cv2.LINE_AA):

        crrTime = time.time()
        if crrTime - self.previousWarning > self.warningBlinkTime:
            self.previousWarning = time.time()
            self.isShowWarning = not self.isShowWarning

        if not self.isShowWarning:
            return src

        rightBottom = tuple(reversed(rightBottom))

        p1 = leftTop
        p2 = (rightBottom[1], leftTop[1])
        p3 = (rightBottom[1], rightBottom[0])
        p4 = (leftTop[0], rightBottom[0])

        height = abs(rightBottom[0] - leftTop[1])

        if radius > 1:
            radius = 1

        cornerRadius = int(radius * (height/2))

        if thickness < 0:

            #big rect
            leftTopMainRect = (int(p1[0] + cornerRadius), int(p1[1]))
            rightBottomMainRect = (int(p3[0] - cornerRadius), int(p3[1]))

            leftTopRectLeft = (p1[0], p1[1] + cornerRadius)
            rightBottomRectLeft = (p4[0] + cornerRadius, p4[1] - cornerRadius)

            leftTopRectRght = (p2[0] - cornerRadius, p2[1] + cornerRadius)
            rightBottomRectRight = (p3[0], p3[1] - cornerRadius)

            allRects = [
            [leftTopMainRect, rightBottomMainRect], 
            [leftTopRectLeft, rightBottomRectLeft], 
            [leftTopRectRght, rightBottomRectRight]]

            [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in allRects]

        # draw straight lines
        cv2.line(src, (p1[0] + cornerRadius, p1[1]), (p2[0] - cornerRadius, p2[1]), color, abs(thickness), lineType)
        cv2.line(src, (p2[0], p2[1] + cornerRadius), (p3[0], p3[1] - cornerRadius), color, abs(thickness), lineType)
        cv2.line(src, (p3[0] - cornerRadius, p4[1]), (p4[0] + cornerRadius, p3[1]), color, abs(thickness), lineType)
        cv2.line(src, (p4[0], p4[1] - cornerRadius), (p1[0], p1[1] + cornerRadius), color, abs(thickness), lineType)

        # draw arcs
        cv2.ellipse(src, (p1[0] + cornerRadius, p1[1] + cornerRadius), (cornerRadius, cornerRadius), 180.0, 0, 90, color ,thickness, lineType)
        cv2.ellipse(src, (p2[0] - cornerRadius, p2[1] + cornerRadius), (cornerRadius, cornerRadius), 270.0, 0, 90, color , thickness, lineType)
        cv2.ellipse(src, (p3[0] - cornerRadius, p3[1] - cornerRadius), (cornerRadius, cornerRadius), 0.0, 0, 90,   color , thickness, lineType)
        cv2.ellipse(src, (p4[0] + cornerRadius, p4[1] - cornerRadius), (cornerRadius, cornerRadius), 90.0, 0, 90,  color , thickness, lineType)

        src = self.putTextInRect(src, text, leftTop, tuple(reversed(rightBottom)), (12, 22, 255) )
        return src



    def roundedRectangle(self, src, leftTop, rightBottom, radius=1, color=(51, 51, 51), thickness=-1, lineType=cv2.LINE_AA):

        rightBottom = tuple(reversed(rightBottom))

        p1 = leftTop
        p2 = (rightBottom[1], leftTop[1])
        p3 = (rightBottom[1], rightBottom[0])
        p4 = (leftTop[0], rightBottom[0])

        height = abs(rightBottom[0] - leftTop[1])

        if radius > 1:
            radius = 1

        cornerRadius = int(radius * (height/2))

        if thickness < 0:

            #big rect
            leftTopMainRect = (int(p1[0] + cornerRadius), int(p1[1]))
            rightBottomMainRect = (int(p3[0] - cornerRadius), int(p3[1]))

            leftTopRectLeft = (p1[0], p1[1] + cornerRadius)
            rightBottomRectLeft = (p4[0] + cornerRadius, p4[1] - cornerRadius)

            leftTopRectRght = (p2[0] - cornerRadius, p2[1] + cornerRadius)
            rightBottomRectRight = (p3[0], p3[1] - cornerRadius)

            allRects = [
            [leftTopMainRect, rightBottomMainRect], 
            [leftTopRectLeft, rightBottomRectLeft], 
            [leftTopRectRght, rightBottomRectRight]]

            [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in allRects]

        # draw straight lines
        cv2.line(src, (p1[0] + cornerRadius, p1[1]), (p2[0] - cornerRadius, p2[1]), color, abs(thickness), lineType)
        cv2.line(src, (p2[0], p2[1] + cornerRadius), (p3[0], p3[1] - cornerRadius), color, abs(thickness), lineType)
        cv2.line(src, (p3[0] - cornerRadius, p4[1]), (p4[0] + cornerRadius, p3[1]), color, abs(thickness), lineType)
        cv2.line(src, (p4[0], p4[1] - cornerRadius), (p1[0], p1[1] + cornerRadius), color, abs(thickness), lineType)

        cv2.ellipse(src, (p1[0] + cornerRadius, p1[1] + cornerRadius), (cornerRadius, cornerRadius), 180.0, 0, 90, color ,thickness, lineType)
        cv2.ellipse(src, (p3[0] - cornerRadius, p3[1] - cornerRadius), (cornerRadius, cornerRadius), 0.0, 0, 90,   color , thickness, lineType)
        cv2.ellipse(src, (p2[0] - cornerRadius, p2[1] + cornerRadius), (cornerRadius, cornerRadius), 270.0, 0, 90, color , thickness, lineType)
        cv2.ellipse(src, (p4[0] + cornerRadius, p4[1] - cornerRadius), (cornerRadius, cornerRadius), 90.0, 0, 90,  color , thickness, lineType)

        return src




if __name__ == "__main__":

    # cv2Effect = CV2Effect(fadeSteps=5, warningBlinkTime=0.8)
    
    # img = cv2.imread("img.jpg")

    img = np.zeros([720,1280,3],dtype=np.uint8)

    # Rectangle
    # cv2Effect = CV2Effect()
    # img = cv2Effect.rectangle(img, (100,100), (300,300), (255,0,0), 2)
    # cv2.imshow("Result", img)
    # cv2.waitKey(0)

    # Rectangle with text
    cv2Effect = CV2Effect()
    img = cv2Effect.rectangleWithText(img,"Test Text" , (100,100), (300,300), (255,0,0), 2)
    cv2.imshow("Result", img)
    cv2.waitKey(0)

    # Fade
    # for i in range(5):
    #     img = cv2.imread("img.jpg")
    #     img = cv2Effect.rectangleFade(img, (100,100), (200,200), (255,0,0), 2)
    #     cv2.imshow("Result", img)
    #     cv2.waitKey(1000)

    # Fade with text
    # for i in range(5):
    #     img = cv2.imread("img.jpg")
    #     img = cv2Effect.rectangleWithTextFade(img, "Test Text", (100,100), (200,200), (255,0,0), 2)
    #     cv2.imshow("Result", img)
    #     cv2.waitKey(1000)

    # Warning round rectangle
    # for i in range(1000):
    #     img = np.zeros([720,1280,3],dtype=np.uint8)
    #     img = cv2Effect.warningRectangle("Test Warning Message", img, (100, 200),(500, 300), radius=0.7)
    #     cv2.imshow("Result", img)
    #     cv2.waitKey(100)

    # Show info with modern rectangle
    # cv2Effect = CV2Effect(fadeSteps=5, warningBlinkTime=0.8)
    # for i in range(1000):
    #     img = np.zeros([720,1280,3],dtype=np.uint8)
    #     img = cv2Effect.roundedRectangle(img, (10, 10),(300, 200), radius=0.3)
    #     cv2.imshow("Result", img)
    #     cv2.waitKey(100)

