#----------CONSTANTS----------#
BACKGROUND_COLOR = "#bea0e5"

from tkinter import *
from tkinter.constants import *
import re
import pandas as pd
from PIL import Image,ImageTk
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier,_tree
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.svm import SVC
import csv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
#_________________________________________________________________________________________________________________________________________________---



training = pd.read_csv('Training.csv')
testing= pd.read_csv('Testing.csv')
cols= training.columns
cols= cols[:-1]
x = training[cols]
y = training['prognosis']
y1= y


reduced_data = training.groupby(training['prognosis']).max()

#mapping strings to numbers
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
testx    = testing[cols]
testy    = testing['prognosis']
testy    = le.transform(testy)


clf1  = DecisionTreeClassifier()
clf = clf1.fit(x_train,y_train)
# print(clf.score(x_train,y_train))
# print ("cross result========")
scores = cross_val_score(clf, x_test, y_test, cv=3)
# print (scores)
print (scores.mean())


model=SVC()
model.fit(x_train,y_train)
print("for svm:")
print(model.score(x_test,y_test))

importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

severityDictionary=dict()
description_list = dict()
precautionDictionary=dict()

symptoms_dict = {}

for index, symptom in enumerate(x):
       symptoms_dict[symptom] = index
def calc_condition(exp,days):
    """Used to calculate condition of the patient based on symptoms"""
    sum=0
    for item in exp:
         sum=sum+severityDictionary[item]
    if((sum*days)/(len(exp)+1)>13):
        print("You should take the consultation from doctor. ")
    else:
        print("It might not be that bad but you should take precautions.")

def getDescription():
    """Will get the description from the csv file"""
    global description_list
    with open('symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _description={row[0]:row[1]}
            description_list.update(_description)




def getSeverityDict():
    """Gets severity dict from csv"""
    global severityDictionary
    with open('symptom_severity.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        try:
            for row in csv_reader:
                _diction={row[0]:int(row[1])}
                severityDictionary.update(_diction)
        except:
            pass


def getprecautionDict():
    """Gets precaution from precaution csv"""
    global precautionDictionary
    with open('symptom_precaution.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec={row[0]:[row[1],row[2],row[3],row[4]]}
            precautionDictionary.update(_prec)
#_______________________________________________________________________________________________________________________________________________

def check_pattern(dis_list,inp):
    pred_list=[]
    inp=inp.replace(' ','_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list=[item for item in dis_list if regexp.search(item)]
    if(len(pred_list)>0):
        return 1,pred_list
    else:
        return 0,[]
def sec_predict(symptoms_exp):
    df = pd.read_csv('Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    symptoms_dict = {symptom: index for index, symptom in enumerate(X)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
      input_vector[[symptoms_dict[item]]] = 1

    return rf_clf.predict([input_vector])


def print_disease(node):
    node = node[0]
    val  = node.nonzero()
    disease = le.inverse_transform(val[0])
    return list(map(lambda x:x.strip(),list(disease)))

def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    chk_dis=",".join(feature_names).split(",")
    symptoms_present = []

    while True:
        yield "Enter the symptom you are experiencing"
        print("\nEnter the symptom you are experiencing \n \t\t",end="->")
        #disease_input = input("")
        disease_input=entry.get()
        conf,cnf_dis=check_pattern(chk_dis,disease_input)
        if conf==1:
            print("searches related to input: ")
            yield "searches related to input: "
            for num,it in enumerate(cnf_dis):
                yield ""+str(num)+")"+it
                print(num,")",it)
            if num!=0:
                yield "Select the one you meant (0 - "+num+")"
                print(f"Select the one you meant (0 - {num}):  ", end="")
                #conf_inp = int(input(""))
                conf_inp=entry.get()
            else:
                conf_inp=0

            disease_input=cnf_dis[conf_inp]
            break
            # print("Did you mean: ",cnf_dis,"?(yes/no) :",end="")
            # conf_inp = input("")
            # if(conf_inp=="yes"):
            #     break
        else:
            yield "Enter valid symptom."
            print("Enter valid symptom.")

    while True:
        try:
            yield "Okay. From how many days ? : "
            #num_days=int(input("Okay. From how many days ? : "))
            num_days=int(entry.get())
            break
        except:
            yield "Enter valid input."
            print("Enter valid input.")


    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]

            if name == disease_input:
                val = 1
            else:
                val = 0
            if  val <= threshold:
                recurse(tree_.children_left[node], depth + 1)
            else:
                symptoms_present.append(name)
                recurse(tree_.children_right[node], depth + 1)
        else:
            present_disease = print_disease(tree_.value[node])
            # print( "You may have " +  present_disease )
            red_cols = reduced_data.columns
            symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
            # dis_list=list(symptoms_present)
            # if len(dis_list)!=0:
            #     print("symptoms present  " + str(list(symptoms_present)))
            # print("symptoms given "  +  str(list(symptoms_given)) )
            yield "Are you experiencing any "
            print("Are you experiencing any ")
            symptoms_exp=[]
            for syms in list(symptoms_given):
                inp=""
                yield ""+syms,"? : "
                print(syms,"? : ",end='')
                while True:
                    #inp=input("")
                    inp=entry.get()
                    if(inp=="yes" or inp=="no"):
                        break
                    else:
                        yield "provide proper answers i.e. (yes/no) : "
                        print("provide proper answers i.e. (yes/no) : ",end="")
                if(inp=="yes"):
                    symptoms_exp.append(syms)

            second_prediction=sec_predict(symptoms_exp)
            # print(second_prediction)
            calc_condition(symptoms_exp,num_days)
            if(present_disease[0]==second_prediction[0]):
                yield "You may have ", present_disease[0]
                print("You may have \n", present_disease[0])
                yield description_list[present_disease[0]]
                print(description_list[present_disease[0]])

                # readn(f"You may have {present_disease[0]}")
                # readn(f"{description_list[present_disease[0]]}")

            else:
                yield "You may have "+ present_disease[0]+"or "+ second_prediction[0]
                yield description_list[present_disease[0]]
                yield description_list[second_prediction[0]]
                print("You may have \n", present_disease[0], "or ", second_prediction[0])
                print(description_list[present_disease[0]])
                print(description_list[second_prediction[0]])

            # print(description_list[present_disease[0]])
            precution_list=precautionDictionary[present_disease[0]]
            print("Take following measures :\n ")
            yield "Take following measures : "
            for  i,j in enumerate(precution_list):
                yield i+1+")"+j
                print(i+1+")"+j)

                confidence_level = (1.0*len(symptoms_present))/len(symptoms_given)
                print("confidence level is " + str(confidence_level))

    #recurse(0, 1)

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11



getSeverityDict()
getDescription()
getprecautionDict()

#tree_to_code(clf,cols)



#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
def message_generator():

    global maindisease
    if entry.get().lower() in ("hi", "hi there", "hello"):
        # ask for name
        yield "Hi there, whats your name ?"
        # greeting with name
        name_var = entry.get()
        #yield "Hi " + name_var + " would you like to purchase a ticket?"
        # more conversation, possibly with diverging branches
        #if entry.get() == "yes": ..
        #tree_to_code(clf, cols)
        tree=clf
        feature_names=cols
        tree_ = tree.tree_
        feature_name = [
            feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree_.feature
        ]

        chk_dis = ",".join(feature_names).split(",")
        symptoms_present = []

        while True:
            yield "Hi "+ name_var.upper() +",Enter the symptom you are experiencing"
            print("\nEnter the symptom you are experiencing  \t\t", end="->")
            # disease_input = input("")
            disease_input = entry.get()
            conf, cnf_dis = check_pattern(chk_dis, disease_input)
            if conf == 1:
                print("searches related to input: ")
                bigline="searches related to input:\n "
                for num, it in enumerate(cnf_dis):
                    bigline += str(num) + ")" + str(it)
                    print(num, ")", it)
                if num != 0:
                    bigline+= "\nSelect the one you meant (0 - " + str(num) + ")"
                    print(f"Select the one you meant (0 - {num}):  ", end="")
                    yield bigline
                    # conf_inp = int(input(""))
                    conf_inp = int(entry.get())
                else:
                    #yield bigline
                    conf_inp = 0

                disease_input = cnf_dis[conf_inp]
                break
                # print("Did you mean: ",cnf_dis,"?(yes/no) :",end="")
                # conf_inp = input("")
                # if(conf_inp=="yes"):
                #     break
            else:
                yield "Enter valid symptom."
                print("Enter valid symptom.")

        while True:
            try:
                yield "Okay. From how many days ? : "
                # num_days=int(input("Okay. From how many days ? : "))
                num_days = int(entry.get())
                break
            except:
                yield "Enter valid input."
                print("Enter valid input.")
#4$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44
        q = [(0, 1)]
        while (q):
            tup=q.pop(0)
            node = tup[0]
            depth = tup[1]
            indent = "  " * depth
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]

                if name == disease_input:
                    val = 1
                else:
                    val = 0
                if val <= threshold:
                    q.append((tree_.children_left[node], depth + 1))
                    # recurse(tree_.children_left[node], depth + 1)
                else:
                    symptoms_present.append(name)
                    q.append((tree_.children_right[node], depth + 1))
                    # recurse(tree_.children_right[node], depth + 1)
            else:
                present_disease = print_disease(tree_.value[node])
                # print( "You may have " +  present_disease )
                red_cols = reduced_data.columns
                symptoms_given = red_cols[reduced_data.loc[present_disease].values[0].nonzero()]
                # dis_list=list(symptoms_present)
                # if len(dis_list)!=0:
                #     print("symptoms present  " + str(list(symptoms_present)))
                # print("symptoms given "  +  str(list(symptoms_given)) )
                #yield "Are you experiencing any "
                print("Are you experiencing any ")
                symptoms_exp = []
                for syms in list(symptoms_given):
                    inp = ""
                    yield "Are you experiencing any" + syms+ "? : "
                    print(syms, "? : ", end='')
                    while True:
                        # inp=input("")
                        inp = entry.get()
                        if (inp == "yes" or inp == "no"):
                            break
                        else:
                            yield "provide proper answers i.e. (yes/no) : "
                            print("provide proper answers i.e. (yes/no) : ", end="")
                    if (inp == "yes"):
                        symptoms_exp.append(syms)

                second_prediction = sec_predict(symptoms_exp)
                # print(second_prediction)
                calc_condition(symptoms_exp, num_days)
                if (present_disease[0] == second_prediction[0]):
                    #yield "You may have "+ present_disease[0]
                    print("You may have ", present_disease[0])
                    #yield description_list[present_disease[0]]
                    print(description_list[present_disease[0]])

                    # readn(f"You may have {present_disease[0]}")
                    # readn(f"{description_list[present_disease[0]]}")

                else:
                    maindisease= "You may have " + present_disease[0] + "or " + second_prediction[0]
                    maindisease+= "\n" + description_list[present_disease[0]]
                    maindisease+= description_list[second_prediction[0]]
                    #yield maindiesease
                    print("You may have ", present_disease[0], "or ", second_prediction[0])
                    print(description_list[present_disease[0]])
                    print(description_list[second_prediction[0]])

                # print(description_list[present_disease[0]])
                precution_list = precautionDictionary[present_disease[0]]
                print("Take following measures : ")
                p_list="Take following measures : "
                for i, j in enumerate(precution_list):
                    #yield i + 1 + ")" + j
                    p_list += "\n" + str(i + 1) + ")" + j
                    print(str(i + 1) + ")" + j)
                yield maindisease+ "\n"+p_list

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2
    else:
        yield "Sorry, I have no answer"


def send():
    text.insert(END, "\n" + entry.get()+" <= You",'tag-right')
    text.insert(END, "\nBot => " + next(msg_gen),'bot-chat')
    entry.delete(0, END)


msg_gen = message_generator()

root = Tk()
root.title('CHATBOT')
root.config(padx=50, pady=50,bg=BACKGROUND_COLOR)
title=Label(text = "AAROGYA  MITRA ",font=("Arial",20,"bold"),fg="red",highlightthickness=0,bg=BACKGROUND_COLOR).grid(row=0,column=1)
# root.geometry('1920x1080')
text = Text(root)
text.tag_configure('tag-right', justify='right')
text.tag_configure('bot-chat', foreground="green",background="yellow")
text.grid(row=1,column=1,columnspan=1,padx = 10,pady = 20)
entry = Entry(root, width=107)
entry.focus_set()
entry.grid(row=2, column=1,padx = 20,pady = 20)
#-------Top-LeftImage-----#
imag2=Image.open("1223 (1) (Custom).png")
test2=ImageTk.PhotoImage(imag2)
label2=Label(image=test2)
label2.image=test2
label2.config(highlightthickness=0,background=BACKGROUND_COLOR)
label2.grid(row=0,column=0)
#--------Right image------#
imag1=Image.open("12.jpg")
test=ImageTk.PhotoImage(imag1)
label=Label(image=test)
label.image=test
label.config(highlightthickness=0,background=BACKGROUND_COLOR)
label.grid(row=0,column=3,rowspan=3,columnspan=2)
Button(root, text="Send",highlightthickness=0,command=send,width=3,padx=10).grid(row=2, column=2)
# Button(root,text="Exit",highlightthickness=0,command=exit,width=15,padx=20).grid(row=3,column=2)
root.mainloop()