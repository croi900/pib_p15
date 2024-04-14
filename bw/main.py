from flask import Flask
import os
import time
app = Flask(__name__)


@app.route('/new_image')
def new_image():
    max_t = 0
    for file in os.listdir("../twda"):
        try:
            t = int(file.split('.')[0])
            max_t = max(t, max_t)
        except:
            pass

    to_htr_path = "../twda/" + str(max_t) + ".jpg"
    bf = open(to_htr_path, "rb")
    image = bf.read()
    out = open("../htr/board.jpeg", "wb")
    out.write(image)
    out.close()
    bf.close()
    os.system(f"cd ../htr && python main.py && mv output.txt ../bw/b_{int(time.time())}.txt")


    return "Success"

@app.route('/new_recording/<to_add>')
def new_recording(to_add):
    sw = open("spoken_words.txt","a")
    sw.write(to_add)

    return "Success"

@app.route('/generate_pdf')
def generate_pdf():
    os.system("cat b_* spoken_words.txt > ../prompt/output.txt")
    os.system("cd ../prompt && python main.py && cp -f outputboss.txt ../mdgen/outputboss.txt")
    os.system("cd ../mdgen && python md.py")
    return "Hello, World!"


if __name__ == '__main__':
    sw = open("spoken_words.txt", "w+")
    sw.write("")
    sw.close()
    app.run(debug=True)