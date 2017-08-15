PYTHONIOENCODING="utf-8"
import numpy
from pandas import read_csv
import csv
import re
import pylab
from matplotlib import mlab
import sys
import io


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    bar = None
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()



def division(string_post):
    # принимает пост из вк в string формате и удаляет
    # ретвиты
    if string_post[0:2] == 'RT':
        string_post = string_post[2:]

    r = []        
    
    while string_post.find('@') != -1:
        if (string_post.find(' ', string_post.find('@'))) != -1:
            r.append(string_post.find(' ', string_post.find('@')))
        else:
            r.append(len(string_post))
        if (string_post.find(',', string_post.find('@'))) != -1:
            r.append(string_post.find(',', string_post.find('@')))
        else:
            r.append(len(string_post))
        if (string_post.find('\n', string_post.find('@'))) != -1:
            r.append(string_post.find('\n', string_post.find('@')))  
        else:
            r.append(len(string_post))
            
        string_post = string_post[:string_post.find('@')] + string_post[(min(r)):]
        r = []    

    
    while string_post.find('http:/') != -1:
        
        if (string_post.find(' ', string_post.find('http:/'))) != -1:
            r.append(string_post.find(' ', string_post.find('http:/')))
        else:
            r.append(len(string_post))
        if (string_post.find(',', string_post.find('http:/'))) != -1:
            r.append(string_post.find(',', string_post.find('http:/')))
        else:
            r.append(len(string_post))
        if (string_post.find('\n', string_post.find('http:/'))) != -1:
            r.append(string_post.find('\n', string_post.find('http:/')))  
        else:
            r.append(len(string_post))
  
        string_post=string_post[:string_post.find('http:/')]+string_post[(min(r)):]
        r = []
    
    string_post.replace('&lt;3', '')
    

    count_word = 0
    offset = 0

    for word in string_post:
        count_word = string_post.find(':')
        if count_word != -1:
            if (string_post.find(' ', count_word)) != -1:
                r.append(string_post.find(' ', count_word))
            else:
                r.append(len(string_post))

            if (string_post.find(',', count_word)) != -1:
                r.append(string_post.find(',', count_word))
            else:
                r.append(len(string_post))

            if (string_post.find('\n', count_word)) != -1:
                r.append(string_post.find('\n', count_word))
            else:
                r.append(len(string_post))

            string_post = string_post[:count_word]+string_post[(min(r)):]
            r = []


    # while string_post.find(':') != -1:
    #     if (string_post.find(' ', string_post.find(':'))) != -1:
    #         r.append(string_post.find(' ', string_post.find(':')))
    #     else:
    #         r.append(len(string_post))
    #
    #     if (string_post.find(',', string_post.find(':'))) != -1:
    #         r.append(string_post.find(',', string_post.find(':')))
    #     else:
    #         r.append(len(string_post))
    #
    #     if (string_post.find('\n', string_post.find(':'))) != -1:
    #         r.append(string_post.find('\n', string_post.find(':')))
    #     else:
    #         r.append(len(string_post))
    #
    #     string_post = string_post[:string_post.find(':')]+string_post[(min(r)):]
    #     r = []

  
    tr = 0
    q = []
    for i in range(len(string_post)):
        if ((string_post[i] == ' ') or (string_post[i] == ',') or \
            (string_post[i] == '.') or (string_post[i] == '—') or \
            (string_post[i] == '?')) and ((tr == ' ') or (tr == ',') or \
            (tr == '.') or (tr == '-') or (tr == '—') or (tr == '?')):
            q.append(i)
        tr = string_post[i]
    
    tr = 0
    for i in range(len(q)):
        string_post = string_post[:(q[i] - i)] + string_post[(q[i] + 1 - i):]
        tr += q[i]
    
    x = 0
    for i in range(len(string_post)):
        if string_post.find(' ',i) != -1:
            x = x + 1
            i += string_post.find(' ')
    
    i = 0
    x1 = []
    x2 = []

    for i in range(len(string_post)):
        if (string_post[i] == ' ') or (string_post[i] == ',') or (string_post[i] == '\n') or \
        (string_post[i] == '.') or (string_post[i] == '?') or (string_post[i] == '-') or (string_post[i] == ')'):
            x1.append(i)
    
    x1.insert(0,0)
    x1.append(len(string_post))
    for i in range(len(x1) - 1):
        if i == 0:
            x2.append(string_post[(x1[i]):(x1[i + 1])])
        else:
            x2.append(string_post[(x1[i] + 1):(x1[i + 1])])
    ix2 = 0

    for i in range(len(x2)):
        if x2[i - ix2] == '':
            x2 = x2[:(i - ix2)] + x2[(i + 1 - ix2):]
            ix2 += 1
    ix2 = 0
    for i in range(len(x2)):
        x2[i - ix2] = re.sub(r'[^\w\s]+|[\d]+', r'',x2[i-ix2]).strip()
        
        if x2[i - ix2] == '':
            x2 = x2[:i - ix2] + x2[i + 1 - ix2:]
            ix2 += 1
        x2[i - ix2] = x2[i - ix2].lower()    
 
    return x2 


def main():
    
    positive = read_csv('positive.csv', sep=';', skiprows=[0], header=None)    
    negative = read_csv('negative.csv', sep=';', skiprows=[0], header=None)
    #output_file = open("positive2_vec.csv", "wb")
    count_uniq = 0
    count_non_uniq = 0
    vec_post = []
    uniq_word = []
    dic_non_uniq = []
    #for i_t in positive:
        #for i in range(len(i_t)):
        
    resultFile = open('dic_non_uniq.csv', 'w', encoding='utf-8')
            
    for i_m in [positive, negative]:
        for i in range(len(i_m)):
            string_post= i_m[3][i]
            #print(string_post)
            vec_div_post = division(string_post)
            if(vec_div_post == []):
                print("#####################")
                continue
            #print(string_post,vec_div_post)
            for i_b in range(len(vec_div_post)):
                if vec_div_post[i_b] in uniq_word:
                #if dic_non_uniq.index(vec_div_post[i_b]):
                    #uniq_word.append(vec_div_post[i_b])
                    #print(i, count_uniq,vec_div_post[i_b])
                    count_uniq += 1
                else:
                    #razn_b.append(count_uniq)
                    resultFile.write((vec_div_post[i_b] + "\n"))
                    uniq_word.append(vec_div_post[i_b])
                    count_non_uniq += 1
                    #print(i,vec_div_post[i_b],count_non_uniq)
            dic_non_uniq.append(count_non_uniq)
            printProgressBar(i, len(i_m), prefix = 'Progress:', suffix = 'Complete', length = 50)
    #print(len(uniq_word),count_non_uniq,count_uniq)
    print(uniq_word)
    

# Write data to file

    ylist = dic_non_uniq
    #print(xlist,ylist)
    pylab.plot (ylist)
    pylab.show()
    r = 1
    for i_m in [positive,negative]:
        for i in range(len(i_m)):
            string_post = i_m[3][i]
            #print(string_post)
            vec_div_post = division(string_post)
            
            #print(string_post,vec_div_post)
            for i_b in range(len(vec_div_post)):
                vec_post.append(uniq_word.index(vec_div_post[i_b]))
            #print(vec_post)
            if r == 0:
                with open("positive2_vec.csv", "a", newline = "") as file:
                    #writer = csv.writer(file)
                    file.write(str(i) + "," + str(vec_post) + "," + "1\n")
                vec_post = []
            else:
                with open("negative2_vec.csv", "a", newline = "") as file:
                    #writer = csv.writer(file)
                    file.write(str(i) + "," + str(vec_post) + "," + "0\n")
                vec_post = []
        printProgressBar(i, len(i_m), prefix = 'Progress:', suffix = 'Complete', length = 50)
        r = 0
    #print(len(uniq_word),count_non_uniq,count_uniq)
    #print(uniq_word)
                

main()