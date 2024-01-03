# Healthcare-Chatbot
We have created a Chatbot named **AAROGYA-MITHRA** which is  based on **Sklearn** where you can give a symptom and it will ask you questions and will tell you the details and give some advice.In this Project we used Supervised Machine learning,The **Decision-Tree Classifier** Algorithm was used to train the model. The datasets available was in .csv format and _Pandas_ library was used to read the files.The Front-end to this model was added with the help of **Tkinter**.
## Methodology
Decision Tree algorithm belongs to the family of supervised learning algorithms. They can be used to solve both regression and classification problems. Decision trees use the tree representation to solve the problem in which each leaf node corresponds to a class label and attributes are represented on the internal node of the tree. Initially the chatbot ask to enter the name of the user, one major symptom that they are facing and period of facing that symptom. In the next step the chatbot ask the specific symptom the user is facing. for example, type 0 for heavy fever or type 1 for mild fever. Next the bot will ask some series of symptoms, and user have to answer in "yes" or "no" manner. If the value is less than threshold, then go to the left child node. If the value is more than threshold, then go to the right child node. Then as we have got the disease, now we need to append the details of the disease and necessary precautions need to be taken. If user is having that particular symptom for more than 13 days then, chatbot will respond as "You should take the consultation from doctor”. If it is less than 13 days then chat bot will respond as, "It might not be that bad but you should take precautions". After predicting the disease, the bot will give necessary precautions that one must take. After predicting the disease, the bot will give a basic description about the disease, as the user will get an idea of what disease that user might be facing. Unlike alternative libraries, it works offline and is compatible with both Python 2 and 3. The proposed Chatbot system functions based on a Decision Tree algorithm.
# Procedures to run the program
## Run Locally
1.Clone the  github repository into a folder by using the command
```git clone https://github.com/Nitish-G-Hande/Healthcare-Chatbot-using-AI.git```

2.Inside the Project folder Run the command
```python chat_bot_template.py```

3.If the command prompt or gitbash cannot run the above command,then open Visual Studio Code or any other editor and run the program 
```python chat_bot_template.py```

4.This prompts the window  to open a chatbot interface where the user can interact with the chatbot

5.The user can start the conversation by typing "Hello"/"hi" and press the send button to which the bot responds with an appropriate answer

6.After taking various symptoms from the user, the chatbot gives its suggestion/advice regarding the disease and the severity of the disease

## Additional Packages and Libraries to be installed to run the Program

```pip install tkinter```
```pip install pillow```
```pip install scikit-learn```
```pip install pandas```
```pip install numpy```


## Output:

