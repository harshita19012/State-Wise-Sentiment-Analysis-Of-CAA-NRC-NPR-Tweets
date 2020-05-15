#!/usr/bin/env python
# coding: utf-8

# ## Import Libraries

# In[1]:


import pandas as pd
import emoji
import numpy as np
import re
from nltk.stem import WordNetLemmatizer
import csv


# In[2]:


lemmatizer = WordNetLemmatizer()


# ## Load Data

# In[3]:


Data = pd.read_excel("D:/Information Retrieval/Project/IR_data.xlsx")
print(Data.shape)
print(Data.columns)


# In[4]:


Data['Tweet'].value_counts().to_numpy()
print(Data.shape)


# In[5]:


emojis = ["\U0001F600","\U0001F603","\U0001F604","\U0001F601","\U0001F606","\U0001F605","\U0001F923","\U0001F602","\U0001F642",
          "\U0001F643","\U0001F609","\U0001F60A","\U0001F607","\U0001F970","\U0001F60D","\U0001F929", "\U0001F618" "\U0001F617",
          "\U0001F61A","\U0001F619","\U0001F60B","\U0001F61B","\U0001F61C","\U0001F92A","\U0001F61D","\U0001F911","\U0001F917",
         "\U0001F92D","\U0001F92B","\U0001F914","\U0001F910","\U0001F928","\U0001F610","\U0001F611","\U0001F636","\U00001F60F",
          "\U0001F612","\U0001F644","\U0001F62C","\U0001F925","\U0001F60C","\U0001F614","\U0001F62A","\U0001F924","\U0001F634",
          "\U0001F637","\U0001F912","\U0001F915","\U0001F922"]


# ## Remove References

# In[6]:


def remove_references(Data):
    for k in range(len(Data)):
    
        x = Data.iloc[k,3]
        words = x.split()
        for word in words:
            if(word[0] == "@"):
                Data.iloc[k,3] = Data.iloc[k, 3].replace(word, "")
    
    return Data
        

Data = remove_references(Data)
Data = Data.to_numpy()
#print(type(Data))
#print(Data.shape)


# ## Special Characters

# In[7]:


special_characters = {
    "Ã¢â‚¬Â¦":"", "â‚¬":"€", "â€š":"‚", "â€ž":"„", "â€¦":"…", "Ë†":"ˆ","â€¹":"‹", "â€˜":"‘", "â€™":"’", "â€œ":"“", "â€":"”",
    "â€¢":"•", "â€“":"–", "â€”":"—", "Ëœ":"˜", "â„¢":"™","â€º":"›", "Å“":"œ", "Å’":"Œ", "Å¾":"ž", "Å¸":"Ÿ","Å¡":"š",
    "Å½":"Ž", "Â¡":"¡", "Â¢":"¢", "Â£":"£","Â¤":"¤", "Â¥":"¥", "Â¦":"¦", "Â§":"§", "Â¨":"¨","Â©":"©", "Âª":"ª", 
    "Â«":"«", "Â¬":"¬", "Â®":"®","Â¯":"¯", "Â°":"°", "Â±":"±", "Â²":"²", "Â³":"³","Â´":"´", "Âµ":"µ", "Â¶":"¶",
    "Â·":"·", "Â¸":"¸","Â¹":"¹", "Âº":"º", "Â»":"»", "Â¼":"¼", "Â½":"½","Â¾":"¾", "Â¿":"¿", "Ã€":"À", "Ã‚":"Â",
    "Ãƒ":"Ã","Ã„":"Ä", "Ã…":"Å", "Ã†":"Æ", "Ã‡":"Ç", "Ãˆ":"È","Ã‰":"É", "ÃŠ":"Ê", "Ã‹":"Ë", "ÃŒ":"Ì", "ÃŽ":"Î",
    "Ã‘":"Ñ", "Ã’":"Ò", "Ã“":"Ó", "Ã”":"Ô", "Ã•":"Õ","Ã–":"Ö", "Ã—":"×", "Ã˜":"Ø", "Ã™":"Ù", "Ãš":"Ú","Ã›":"Û", 
    "Ãœ":"Ü", "Ãž":"Þ", "ÃŸ":"ß", "Ã¡":"á","Ã¢":"â", "Ã£":"ã", "Ã¤":"ä", "Ã¥":"å", "Ã¦":"æ","Ã§":"ç", "Ã¨":"è",
    "Ã©":"é", "Ãª":"ê", "Ã«":"ë","Ã¬":"ì", "Ã­":"í", "Ã®":"î", "Ã¯":"ï", "Ã°":"ð","Ã±":"ñ", "Ã²":"ò", "Ã³":"ó",
    "Ã´":"ô", "Ãµ":"õ","Ã¶":"ö", "Ã·":"÷", "Ã¸":"ø", "Ã¹":"ù", "Ãº":"ú","Ã»":"û", "Ã¼":"ü", "Ã½":"ý", "Ã¾":"þ", "Ã¿":"ÿ",
    "Ã¢â‚¬Â¦":" ", "Ã°Ã¿â€¡Â¨Ã°Ã¿â€¡Â¦":"", "Ã¢â‚¬â„¢":"’" , "aÃ¢â‚¬Â¦":"","Ã¢â‚¬Â¦":" ", " Ã¢â‚¬Å“":" ", "Ã¢â‚¬â„¢s":"'s",
    "â‚¬":"", "â„¢":"'","Ã¢":"", "Ã¢â‚¬Â¦":"", "Ã°":"", "Ã¿":"", "‘Â\x8f‘Â\x8f‘Â\x8d":"", "˜¡":""
  }


# In[8]:


def remove_special_characters(data, special_characters):
    for k in range(data.shape[0]):
        for l in range(data.shape[1]):
            x = data[k][l]
            #print(x)
    
            if(isinstance(x, str)):
                words = x.split()
                #print(words)
            
                for i in range(len(words)):
                    word = words[i]
                    for char in special_characters:
                        if(char in word):
                            #print(char)
                            word = word.replace(char, special_characters[char])
                        
                    words[i] = word
                new_words = ' '.join([str(elem) for elem in words])
                data[k][l] = new_words
                
    return data

Data = remove_special_characters(Data, special_characters)


# ## Remove Abbreviations

# In[9]:


def create_dictionary():
    data = open("D:/Information Retrieval/Project/abbreviations.txt", "r")
    data = data.readlines()
    
    abbreviations = {}
    for string in data:
    
        words = string.split("=")
        #print(words[0], words[1])
        x = words[1][:-1]
        abbreviations[words[0]] = x
        
    return abbreviations

abbreviations = create_dictionary()
#print(abbreviations)


# In[10]:


def remove_abbreviations(data, abbreviations):
    
    for k in range(data.shape[0]):
        for l in range(data.shape[1]):
            user_string = data[k][l]
            
            if(isinstance(user_string, str)):
                words = user_string.split()
                
                for i in range(len(words)):
                    
                    word = words[i]
                    if(word in abbreviations):
                        word = abbreviations[word]
                    
                    words[i] = word
                new_words = ' '.join([str(elem) for elem in words])
                data[k][l] = new_words
    return data
        
Data = remove_abbreviations(Data, abbreviations)


# In[11]:


whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+-./:;<=>?[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace


# ## Modify Locations

# In[12]:


def modify_locations(Data):
    
    for i in range(data.shape[0]):
        
        new_location = ""
        location = data[i][0]
        if(isinstance(location, str)):
            #print(location)
            for k in location:
                if(k in printable):
                    new_location = new_location + k
        
        data[i][0] = new_location
    
    return data
        
#modify_locations(Data)


# ## Lower Case Conversions

# In[13]:


def convert_lower(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            
            if(isinstance(data[i][j], str)):
                data[i][j] = data[i][j].lower()
        
        if(data[i][0] == ''):
            data[i][0] = 'random'
    #print(data)
    return data

Data = convert_lower(Data)


# ## Hash Tag Removal

# In[14]:


def remove_hashtags(data):
    
    punctuations = '''!()-![]{};:+'"\,<>./?#$%^&*_~'''
    for i in range(data.shape[0]):
        tweet = data[i][3]
        
        new_tweet = ""
        for k in tweet:
            if(punctuation.find(k) == -1):
                new_tweet = new_tweet + k
        data[i][3] = new_tweet
    
    return data
        
Data = remove_hashtags(Data)
#print(Data)


# ## Lemmatization

# In[15]:


def lemmatization(data):
    
    for i in range(data.shape[0]):
        tweet = data[i][3]
        
        x = tweet.split()
        
        new_tweet = ""
        for k in x:
            new_tweet = new_tweet + " " + (lemmatizer.lemmatize(k))
        data[i][3] = new_tweet
    
    return data

data = lemmatization(Data)
#print(Data)


# In[18]:


def return_states(states, data):
    x = []
    for state in states:
        if(state not in data):
            cities = states[state]
            for city in cities:
                if(city in data):
                    x.append(state)
            for city in cities:
                for k in data:
                    new_data = city + "*"
                    if(re.search(new_data, k)):
                        x.append(state)
        else:
            x.append(state)

    for state in states:
        for k in data:
            if(re.search((state + "+"), k)):
                x.append(state)
                
    new_x = []
    for k in x:
        if(k not in new_x):
            new_x.append(k)
    
    return new_x


# In[16]:


print(Data)


# ## Store in Excel

# In[50]:


df = pd.DataFrame(data = Data, columns=["Location", "Retweet Count", "Date", "Tweet", "Label"])


# In[51]:


df.to_excel('D:/Information Retrieval/Project/Final_Data/Test_Data.xlsx')


# ## State-wise Division Of Tweets

# In[20]:


def state_wise_tweets(data):
    states = {'andhra pradesh': ['hyderabad','adilabad','anantapur','chittoor','kakinada','guntur','karimnagar','khammam',
                                 'krishna','kurnool','mahbubnagar','medak','nalgonda','nizamabad','ongole','srikakulam',
                                'nellore','visakhapatnam','vizianagaram','warangal','eluru','kadapa'], 
              
              'arunachal pradesh': ['itangar','anjaw','changlang','east siang','kurung kumey','lohit','lower dibang valley',
                                    'lower subansiri','papum pare','tawang','tirap','dibang valley','upper siang',
                                    'upper subansiri','west kameng' 'west siang'],
              
              'assam': ['dispur','guwahati','baksa','barpeta','bongaigaon','cachar','chirang','darrang','dhemaji',
                        'dima hasao','dhubri','dibrugarh','goalpara','golaghat','hailakandi','jorhat','kamrup',
                        'kamrup metropolitan','karbi anglong','karimganj','kokrajhar','lakhimpur','marigaon','nagaon',
                        'nalbari','sibsagar','sonitpur','tinsukia','udalguri'], 
              
              'bihar': ['patna','gaya','bhagalpur','muzaffarpur','purnia','darbhanga','arrah','begusarai','katihar','munger',
                       'chhapra','danapur','bettiah','saharsa','sasaram','hajipur','dehri','siwan','motihari','nawada',
                       'bagaha','buxar','kishanganj','sitamarhi','jamalpur','jehanabad','aurangabad'], 
              
              'chhattisgarh': ['raipur','bastar','bijapur','bilaspur','dantewada','dhamtari','durg','jashpur','janjgir-champa'
                        'korba','koriya','kanker','kabirdham','mahasamund','narayanpur','raigarh','rajnandgaon','surguja'],
              
              'goa': ['panaji'],
              
              'gujarat': ['gandhinagar','ahmedabad','amreli district','anand','banaskantha','bharuch','bhavnagar','dahod',
                        'the dangs','jamnagar','junagadh','kutch','kheda','mehsana','narmada','navsari','patan','panchmahal',
                        'porbandar','rajkot','sabarkantha','surendranagar','surat','vyara','vadodara','valsad'],
              
              'haryana': ['chandigarh','ambala','bhiwani','faridabad','fatehabad','gurgaon','hissar','jhajjar','jind',
                          'karnal','kaithal','kurukshetra','mahendragarh','mewat','palwal','panchkula','panipat','rewari',
                          'rohtak','sirsa','sonipat','yamuna Nagar'],
              
              'himachal Pradesh':['shimla','bilaspur','chamba','hamirpur','kangra','kinnaur','kullu','lahaul','spiti','mandi',
                                'sirmaur','solan','una'],
              
              'jammu and kashmir': ['srinagar','anantnag','badgam','bandipora','baramulla','doda','ganderbal','jammu','kargil',
                        'kathua','kishtwar','kupwara','kulgam','leh','poonch','pulwama','rajauri','ramban','reasi','samba',
                        'shopian','srinagar','udhampur'],
              
              'jharkhand': ['ranchi','bokaro','chatra','deoghar','dhanbad','dumka','east singhbhum','garhwa','giridih','godda',
                        'gumla','hazaribag','jamtara','khunti','koderma','latehar','lohardaga','pakur','palamu','ramgarh',
                        'ranchi','sahibganj','seraikela','simdega','west-singhbhum'],
              
              'karnataka': ['bangalore','bengaluru','bagalkot','belgaum','bellary','bidar','bijapur','chamarajnagar','chikkamagaluru',
                        'chikkaballapur','chitradurga','davanagere','dharwad','dakshinakannada','gadag','gulbarga','hassan','haveri_district',
                            'kodagu','kolar','koppal','mandya','mysore','raichur','shimoga','tumkur','udupi','ramanagara','yadgir'],
              
              'kerala': ['thiruvananthapuram','alappuzha','ernakulam','idukki','kannur','kasaragod','kollam','kottayam',
                    'kozhikode','malappuram','palakkad','pathanamthitta','thrissur','thiruvananthapuram','Wayanad'],
              
              'madhya pradesh': ['bhopal','alirajpur','anuppur','ashoknagar','balaghat','barwani','betul','bhind','burhanpur',
                    'chhatarpur','chhindwara','damoh','datia','dewas','dhar','dindori','guna','gwalior','harda','hoshangabad',
                    'indore','jabalpur','jhabua','katni','khandwa','khargone','mandla','mandsaur','morena','narsinghpur','neemuch',
                    'panna','rewa','rajgarh','ratlam','raisen','sagar','satna','sehore','seoni','shahdol','shajapur',
                    'sheopur','shivpuri','sidhi','singrauli','tikamgarh','ujjain','umaria','vidisha'],
              
              'maharashtra': ['mumbai','pune','ahmednagar','akola','amravati','aurangabad','bhandara','beed','buldhana','chandrapur','dhule',
                              'gadchiroli','gondia','hingoli','jalgaon','jalna','kolhapur','latur','nandurbar','nanded','nagpur','nashik',
                              'osmanabad','parbhani','raigad','ratnagiri','sindhudurg','sangli','solapur','satara','thane','wardha','Washim','yavatmal'],
              
              'manipur': ['imphal','bishnupur','churachandpur','chandel','senapati','tamenglong','thoubal','ukhrul'],
              
              'meghalaya': ['shillong','east garo hills','east Khasi Hills','Jaintia Hills','Ri Bhoi','South Garo Hills',
                    'West Garo Hills','West Khasi Hills'],
              
              'mizoram': ['aizawi','champhai','kolasib','lawngtlai','lunglei','mamit','saiha','serchhip'],
              
              'nagaland':['kohima','dimapur','mokokchung','mon','phek','tuensang','wokha','zunheboto'],
              
              'orissa':['bhubaneshwar','angul','boudh','bhadrak','balangir','bargarh','baragarh','balasore','cuttack','debagarh',
                    'deogarh','dhenkanal','ganjam','gajapati','jharsuguda','jajpur','jagatsinghpur','khordha','kendujhar', 'keonjhar',
                    'kalahandi','kandhamal','koraput','kendrapara','malkangiri','mayurbhanj','nabarangpur','nuapada','nayagarh',
                    'puri','rayagada','sambalpur','subarnapur','sonepur','sundergarh'],
              
              'punjab':['chandigarh','amritsar','barnala','bathinda','firozpur','faridkot','fatehgarhsahib','fatehgarh','fazilka',
                    'gurdaspur','hoshiarpur','jalandhar','kapurthala','ludhiana','mansa','moga','pathankot','patiala','rupnagar',
                    'ajitgarh','mohali','sangrur','nawanshahr'],
              
              'rajasthan':['jaipur','ajmer','alwar','bikaner','barmer','banswara','bharatpur','baran','bundi','bhilwara','churu',
                    'chittorgarh','dausa','dholpur','dungapur','ganganagar','hanumangarh','jhunjhunu','jalore','jodhpur','jaipur',
                    'jaisalmer','jhalawar','karauli','kota','nagaur','pali','pratapgarh','rajsamand','sikar','sawaimadhopur',
                    'sirohi','tonk','udaipur'],
              
              'sikkim': ['gangtok'],
              
              'tamil Nadu': ['chennai','ariyalur','coimbatore','cuddalore','dharmapuri','dindigul','erode','kanchipuram',
                        'kanyakumari','karur','madurai','nagapattinam','nilgiris','namakkal','perambalur','pudukkottai',
                        'ramanathapuram','salem','sivaganga','tirupur','tiruchirappalli','theni','tirunelveli','thanjavur',
                        'thoothukudi','tiruvallur','tiruvarur','tiruvannamalai','vellore','viluppuram','virudhunagar'],
              
              'telagana': ['hyderabad'],
              
              'tripura':['agartala','dhalai','khowai'],
              
              'uttarakhand': ['dehradun','almora','bageshwar','chamoli','champawat','haridwar','nainital','pauri','garhwal',
                    'pithoragarh','rudraprayag','tehri','Udhamsinghnagar','uttarkashi'],
              
              'delhi':['CP','jammia','karol bagh','Mayur vihar','Preet vihar','shahdara','saket','shaheen bagh','jnu',
                       'seelampur', 'jafrabad', 'maujpur', 'kardampuri', 'babarpur', 'gokulpuri','shivpuri'],
              
              'uttar Pradesh': ['lucknow','muzaffarnagar','Aligarh', 'Mau', 'Azamgarh', 'Kanpur', 'Bareilly', 'Shahjahanpur',
                    'Ghaziabad', 'Bulandshahr','allahabad','agra','ambedkarnagar','auraiya','barabanki','budaun','bagpat',
                    'bahraich','bijnor','ballia','banda','balrampur','basti','chandauli','chitrakoot','deoria','etah','Etawah',
                    'firozabad','farrukhabad','fatehpur','faizabad','gonda','ghazipur','gorakhpur','hamirpur','hardoi','jhansi',
                    'jalaun','jaunpur','kannauj','kanpur','kaushambi','kushinagar','lalitpur','meerut','maharajganj','mahoba',
                    'mirzapur','moradabad','mainpuri','mathura','panchsheel','hapur','pilibhit','shamli','pratapgarh','rampur',
                    'raebareli','saharanpur','sitapur','shahjahanpur','siddharthnagar','sonbhadra','sultanpur','shravasti','unnao','varanasi'],
              
              'west Bengal':['kolkata','birbhum','bankura','bardhaman','darjeeling','dinajpur','hooghly','howrah','jalpaiguri',
                    'coochbehar','maldah','medinipur','murshidabad','nadia','purulia']}
    
    state_tweets = {}
    a = 0
    for i in range(data.shape[0]):
        count = True
        location = data[i][0].split()
        #print(a, location)
        
        for state in states:
            if(state not in location):
                cities = states[state]
                for city in cities:
                    if(city in location):
                        count = False
                        if(state in state_tweets):
                            #print("X")
                            old_data = state_tweets[state]
                            old_data.append(list(data[i,1:]))
                            state_tweets[state] = old_data
                        else:
                            #print("Y")
                            new_data = list(data[i,1:])
                            x = []
                            x.append(new_data)
                            state_tweets[state] = x
                        
            else:
                count = False
                if(state in state_tweets):
                    #print("A")
                    old_data = state_tweets[state]
                    old_data.append(list(data[i,1:]))
                    state_tweets[state] = old_data
                else:
                    #print("B")
                    new_data = list(data[i,1:])
                    x = []
                    x.append(new_data)
                    state_tweets[state] = x
        
        if(count == True):
            tweet_data = data[i][3].split()
            new_states = return_states(states, tweet_data)
            
            #print(new_states)
            if(len(new_states)!= 0):
                count = False
                for k in new_states:
                    if(k in state_tweets):
                        #print("C")
                        old_data = state_tweets[k]
                        old_data.append(list(data[i,1:]))
                        state_tweets[k] = old_data
                    else:
                        #print("D")
                        new_data = list(data[i,1:])
                        x = []
                        x.append(new_data)
                        state_tweets[k] = x
                        
        if(count == True):
            if('random' in state_tweets):
                #print("E")
                old_data = state_tweets['random']
                old_data.append(list(data[i,1:]))
                state_tweets['random'] = old_data
                
            else:
                #print("F")
                new_data = list(data[i,1:])
                x = []
                x.append(new_data)
                state_tweets['random'] = x
        a = a + 1
    
    return state_tweets
        
dict1 = state_wise_tweets(data)


# In[54]:


sum1 = 0
for k in dict1:
    sum1 = sum1 + len(dict1[k])
    print(k, len(dict1[k]))
    
print(sum1)

