#Writing 
with open("notes.txt","w") as f:
    f.write("Hi, my name is Danish and this my my first Text file")

#Reading 
with open("notes.txt","r") as f:
    content=f.read()
    print(content)

#appending 
with open("notes.txt","a") as f:
    f.write("\n and I can Edit this file too")