from flask import Flask,render_template,request
from My_skate2 import *
app = Flask(__name__)
SkateDeluxe=SkateDeluxe()
SkateTitus=SkateTitus()

@app.route('/',methods=['GET', 'POST'])
def index():
    SkateDeluxe_Nom = SkateDeluxe.SkateDeluxe_Nom()
    SkateDeluxe_Marque=SkateDeluxe.SkateDeluxe_Marque()
    SkateDeluxe_Prix=SkateDeluxe.SkateDeluxe_Prix()[0]
    SkateDeluxe_Lien=SkateDeluxe.Lien_SkateDeluxe_photo()

    Titus_Nom=SkateTitus.Titus_Nom()
    Titus_Marque=SkateTitus.Titus_Marque()
    Titus_Prix=SkateTitus.Titus_Prix()
    Titus_Lien=SkateTitus.Lien_Titus_photo()

    if request.method=="POST":
        Place=request.form.get("selection")
        if Place==None:
            Place=0
        else:
            Place=int(Place)
    else:
        Place=0
    return render_template('index.html',SkateDeluxe_Nom=SkateDeluxe_Nom,SkateDeluxe_Marque=SkateDeluxe_Marque,SkateDeluxe_Prix=SkateDeluxe_Prix,SkateDeluxe_Lien=SkateDeluxe_Lien, TailleDeluxe=len(SkateDeluxe_Nom),
                           Titus_Nom=Titus_Nom,Titus_Marque=Titus_Marque,Titus_Prix=Titus_Prix,Titus_Lien=Titus_Lien,TailleTitus=len(Titus_Nom),
                           Place=Place)

if __name__ == "__main__":
    app.run(debug=True)