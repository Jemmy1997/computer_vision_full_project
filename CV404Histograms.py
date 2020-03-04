def histogram(img):
    row, col = img.shape
    histo = {}
    for i in range(row):
        for j in range(col):
            histo[img[i, j]] = histo.get(img[i, j], 0)+1

    sortedHisto = sorted(histo.items())          
    return histo,sortedHisto

def equalization(img):
    equalized_img = img
    histo,sortedHisto = histogram(img)
    row = img.shape[0]
    col =img.shape[1]
    total_num = row*col 
    lvl =255
    pdf = {}
    cdf = {}
    roundoff={}
    equalized={}
    for i in range(len(sortedHisto)):
        pdf[sortedHisto[i][0]] = sortedHisto[i][1]/total_num
    for j in range(len(pdf)):
        if j ==0:
            cdf[sortedHisto[0][0]] = pdf[sortedHisto[0][0]]
        else:    
            cdf[sortedHisto[j][0]] =  cdf[sortedHisto[j-1][0]]  + pdf[sortedHisto[j][0]] 
    roundoff = cdf
    for key in roundoff:
        roundoff[key] = round(roundoff[key]*lvl)
        equalized[roundoff[key]] = equalized.get(roundoff[key],0)+ histo[key]

    for i in range(row):
        for j in range(col):
                equalized_img[i,j] = roundoff[equalized_img[i,j]]

    return equalized_img