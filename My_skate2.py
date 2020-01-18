import urllib.request
import bs4
import os

class SkateDeluxe:
    """
        Constructeur qui init la connexnion et prend les div ou sont placées les noms,prix ...
        Ainsi que le chemin de l'enregistrement des photos.
    """
    def __init__(self):
        self.Lien_SkateDeluxe=urllib.request.urlopen("https://www.skatedeluxe.com/fr/planches-skate/?page=2")
        self.soup_SkateDeluxe = bs4.BeautifulSoup(self.Lien_SkateDeluxe.read(),'html.parser')
        self.Nom_des_boards_SkateDeluxe=(self.soup_SkateDeluxe.findAll("div",{"class":"listing-product-name"}))
        self.Prix_des_boards_SkateDeluxe=(self.soup_SkateDeluxe.findAll("div",{"class":"listing-product-price"}))
        self.Marque_des_boards_SkateDeluxe=(self.soup_SkateDeluxe.findAll("div",{"class":"listing-product-manufacturer"}))
        self.Image_SkateDeluxe=(self.soup_SkateDeluxe.find_all("div",{"class":"listing-product-image-container"}))
        self.Chemin_SkateDeluxe="C:\Python\Web Scraping\Site\Photo\SkateDeluxe"


    def Join_and_Strip(self,Nom_Liste):
        """
        Prend en paramètre une liste qui par la suite la join (transforme en str) et strip (supprime les espaces au début et fin de phrase).
        """
        Nom_Liste="".join(Nom_Liste)
        Nom_Liste=Nom_Liste.strip()
        #Si on trouve " alors on le remplace par inch (Pouce)
        if '"' in Nom_Liste:
            Nom_Liste=Nom_Liste.replace('"'," inch")
        else:
            pass
        return Nom_Liste

    def SkateDeluxe_Nom(self):
        """
            Cherche le nom des boards skatedeluxe et en retourne la liste.
        """
        Nom_des_boards=self.Nom_des_boards_SkateDeluxe
        List_des_planches=[]
        #Passe chaque élément en str puis prend le debut et la fin pour garder que le milieux
        for i in range(len(Nom_des_boards)):
            Nom_de_la_board=Nom_des_boards[i]
            Nom_de_la_board=str(Nom_de_la_board)
            Debut=Nom_de_la_board.find(">")
            Fin=Nom_de_la_board.find("Planche Skate")
            Nouveau_Nom=[]
            for i in range(Debut+1,Fin):
                Nouveau_Nom.append(Nom_de_la_board[i])
            Nouveau_Nom=self.Join_and_Strip(Nouveau_Nom)
            List_des_planches.append(Nouveau_Nom)
        return List_des_planches

    def SkateDeluxe_Prix(self):
        """
        Cherche les prix  et en retourne 2 liste une prix normal et lautre ancien prix si il y a eu une promotion
        """
        #On peut avoir des promotions !!!
        Prix_des_boards=self.Prix_des_boards_SkateDeluxe
        Liste_des_Prix=[]
        Liste_des_Promotions=[]
        for i in range(len(Prix_des_boards)):
            Le_Prix=Prix_des_boards[i]
            Le_Prix=str(Le_Prix)
            #Si dans le str on trouve "new" alors c'est une promotion
            if "new" in Le_Prix:
                #Prend le premier Prix
                Debut=Le_Prix.find("new")+5
                Fin=Le_Prix.find("EUR")
                Prix_1=(Le_Prix[Debut:Fin])
                Prix_1=self.Join_and_Strip(Prix_1)
                Prix_1=Prix_1.replace(",",".")
                Prix_1=float(Prix_1)
                #Prend le deuxième Prix
                Debut=Le_Prix.find("old")+5
                Fin=Le_Prix.find("EUR",Debut)
                Prix_2=(Le_Prix[Debut:Fin])
                Prix_2=self.Join_and_Strip(Prix_2)
                Prix_2=Prix_2.replace(",",".")
                Prix_2=float(Prix_2)
                #Ajoute au deux liste met la promotions dans Prix normal car moins chère
                Liste_des_Prix.append(Prix_1)
                Liste_des_Promotions.append(Prix_2)
            #Sinon il n'y a pas de promotion alors on prend juste un Prix
            else:
                Debut=Le_Prix.find("regular")+9
                Fin=Le_Prix.find("EUR")
                Prix=(Le_Prix[Debut:Fin])
                Prix=self.Join_and_Strip(Prix)
                Prix=Prix.replace(",",".")
                Prix=float(Prix)
                Liste_des_Prix.append(Prix)
                Liste_des_Promotions.append(0.0)
        #Return deux liste donc deux variable en sortit
        return Liste_des_Prix,Liste_des_Promotions

    def SkateDeluxe_Marque(self):
        """
        Cherche les marques et en retourne une liste
        """
        Marque_des_boards=self.Marque_des_boards_SkateDeluxe
        Liste_des_Marques=[]
        for i in range(len(Marque_des_boards)):
            Marque=Marque_des_boards[i]
            Marque=str(Marque)
            Nouvelle_Marque=[]
            Debut=Marque.find(">")+1
            Fin=Marque.find("<",1)
            for i in range(Debut,Fin):
                Nouvelle_Marque.append(Marque[i])
            Nouvelle_Marque=self.Join_and_Strip(Nouvelle_Marque)
            Liste_des_Marques.append(Nouvelle_Marque)
        return Liste_des_Marques

    def Photo_SkateDeluxe(self):
        """
        Récupère le lien de la photo pour ensuite le téléchager dans un dossier sans qu'il y est de doublons de nom
        """
        Image_SkateDeluxe=self.Image_SkateDeluxe
        Dossier_Photo_SkateDeluxe=os.chdir(self.Chemin_SkateDeluxe)
        Liste_des_Boards_SkateDeluxe=self.SkateDeluxe_Nom()
        #Parcour la liste
        for Position in range(len(Image_SkateDeluxe)):
            #Garde toujours le même début de lien
            Url="https://cdn.skatedeluxe.com/images/product_images/200px2x/"
            #Donne un nom à la photo
            Name="{}.jpg".format(Liste_des_Boards_SkateDeluxe[Position])
            Reference=""
            #Avec bs4 prend la partie qui m'intéresse
            Data_sources=Image_SkateDeluxe[Position].img["data-sources"]
            Compteur=0
            #Prend toute la référence avant la virgule
            while Data_sources[Compteur]!=",":
                Reference+=Data_sources[Compteur]
                Compteur+=1
            #Rajoute à l'url la référence
            Url+="{}".format(Reference)
            #Enregistre l'image avec son ulr,nom,et ou elle va être enregistrer
            urllib.request.urlretrieve(Url,Name,Dossier_Photo_SkateDeluxe)

    def Lien_SkateDeluxe_photo(self):
        """
        Prend les liens des photos et non les images plus rapide
        """
        Image_SkateDeluxe = self.Image_SkateDeluxe
        Liste_Lien=[]
        # Parcour la liste
        for Position in range(len(Image_SkateDeluxe)):
            # Garde toujours le même début de lien
            Url = "https://cdn.skatedeluxe.com/images/product_images/200px2x/"
            Reference = ""
            # Avec bs4 prend la partie qui m'intéresse
            Data_sources = Image_SkateDeluxe[Position].img["data-sources"]
            Compteur = 0
            # Prend toute la référence avant la virgule
            while Data_sources[Compteur] != ",":
                Reference += Data_sources[Compteur]
                Compteur += 1
            # Rajoute à l'url la référence
            Url += "{}".format(Reference)
            Liste_Lien.append(Url)
        return Liste_Lien




    def Avenger_Rassemblement(self,Les_Marques,Les_Boards,Les_Prix,Les_Promotions=[0]):
        """
        Prend plusieurs listes en paramètre et les assembles si il n'y a pas de promotions alors valeur de base égal 0
        """
        Liste_Final=[]
        Verificateur=False
        for i in range(len(Les_Promotions)):
            if Les_Promotions[i]>0.0:
                Verificateur=True
                break
            else:
                pass
        if Verificateur:
            for i in range(len(Les_Marques)):
                Tempo_Marques=Les_Marques[i]
                Tempo_Boards=Les_Boards[i]
                Tempo_Prix=Les_Prix[i]
                Tempo_Promotion=Les_Promotions[i]
                Tuple=(Tempo_Marques,Tempo_Boards,Tempo_Prix,Tempo_Promotion)
                Liste_Final.append(Tuple)
            return Liste_Final
        else:
            for i in range(len(Les_Marques)):
                Tempo_Marques=Les_Marques[i]
                Tempo_Boards=Les_Boards[i]
                Tempo_Prix=Les_Prix[i]
                Tuple=(Tempo_Marques,Tempo_Boards,Tempo_Prix)
                Liste_Final.append(Tuple)
            return Liste_Final

    def Affichage(self):
        """
        Affichage dans l'ide
        """
        Liste_Complete_SkateDeluxe=self.Avenger_Rassemblement(self.SkateDeluxe_Marque(),self.SkateDeluxe_Nom(),self.SkateDeluxe_Prix()[0],self.SkateDeluxe_Prix()[1])
        for i in range(len(Liste_Complete_SkateDeluxe)):
            Tempo=Liste_Complete_SkateDeluxe[i]
            if Tempo[3] == 0.0:
                print("{}, {}\n{} €".format(Tempo[0], Tempo[1], Tempo[2]))
            else:
                print("{}, {}\nEn promotions à {} € au lieu de  {} €".format(Tempo[0], Tempo[1],Tempo[2],Tempo[3]))

    def Complete(self):
        """
        Rassemble toutes les listes en une puis la tri par rapport au prix
        """
        Liste_Complete_SkateDeluxe = self.Avenger_Rassemblement(self.SkateDeluxe_Marque(), self.SkateDeluxe_Nom(),
                                                                self.SkateDeluxe_Prix()[0], self.SkateDeluxe_Prix()[1])
        Liste_Complete_SkateDeluxe=sorted(Liste_Complete_SkateDeluxe,key=lambda colonnes:colonnes[2])
        return  Liste_Complete_SkateDeluxe


    def __del__(self):
        """
        Destructeur vide le fichier photo à la fin
        """
        Chemin=self.Chemin_SkateDeluxe
        for file in os.listdir(os.chdir(Chemin)):
            os.remove(file)


class SkateTitus(SkateDeluxe):
    def __init__(self):

        """
        Constructeur pareil que le premier a l'exception d'un build opener pour pouvoir télécharger les images
        """
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)


        self.Lien_Titus=urllib.request.urlopen("https://www.titus-shop.com/fr/skate-skateboards-planches-de-skate/?p=1")
        self.soup_Titus = bs4.BeautifulSoup(self.Lien_Titus.read(),'html.parser')
        self.Nom_des_boards_Titus=(self.soup_Titus.find_all("div",{"class":"product--content"}))
        self.Prix_des_boards_Titus=(self.soup_Titus.find_all("div",{"class":"product--price"}))
        self.Image_Titus=(self.soup_Titus.find_all("div",{"class":"image-slider--item"}))
        self.Chemin_Titus="C:\Python\Web Scraping\Site\Photo\Titus"



    def Titus_Marque(self):
        """
        Prend les marques des planches et le return dans une liste
        """
        Marque_des_boards=self.Nom_des_boards_Titus
        Liste_Marque=[]
        for i in range(len(Marque_des_boards)):
            Marque_de_la_board=Marque_des_boards[i]
            Liste_Marque.append(Marque_de_la_board.b.string)
        return Liste_Marque

    def Titus_Nom(self):
        """
        Prend le nom des planches et retourne dans une liste
        """
        Nom_des_boards=self.Nom_des_boards_Titus
        Liste_Nom=[]
        for i in range(len(Nom_des_boards)):
            Nom_de_la_board=Nom_des_boards[i]
            #Entre les balise <a> </a>
            Tempo=Nom_de_la_board.a
            #Passe dans une liste et le nom se trouvait à la position 2
            Nom=Tempo.contents[2].string
            Nom=str(Nom)
            #Enlève le mot Planche
            Nom=Nom.replace(", Planche","")
            Nom=Nom.strip()
            Liste_Nom.append(Nom)
        return Liste_Nom

    def Titus_Prix(self):
        """
            Prend le prix des planches et retourne dans une liste
        """
        Prix_des_boards=self.Prix_des_boards_Titus
        Liste_Prix=[]
        for i in range(len(Prix_des_boards)):
            Prix_de_la_board=Prix_des_boards[i]
            Tempo=Prix_de_la_board.a
            Prix=Tempo.contents[0]
            Prix=(Prix[1:6])
            Prix=Prix.replace(",",".")
            Prix=float(Prix)
            Liste_Prix.append(Prix)
        return Liste_Prix

    def Photo_Titus(self):
        """
        Télecharge les images des planches
        """
        Image_Titus=self.Image_Titus
        Liste_des_Nom_Titus=self.Titus_Nom()
        Dossier_Photo_Titus=os.chdir(self.Chemin_Titus)
        Compteur_Doublons=0
        for i in range(len(Liste_des_Nom_Titus)):
            Url=""
            #Prend les informations utile
            Data_sources=Image_Titus[i].picture.source["srcset"]
            Compteur=0
            #Prend tout avant la virgule
            while Data_sources[Compteur]!=",":
                Url+=Data_sources[Compteur]
                Compteur+=1
            #Nom de base
            name="{}.jpg".format(Liste_des_Nom_Titus[i])
            #Commande qui renvoie un booléen si le fichier existe ou pas
            Nom_photo=os.path.exists(name)
            #Tant que le nom existe on rajoute plus 1
            while Nom_photo == True:
                Compteur_Doublons+=1
                name="{}.jpg".format(Liste_des_Nom_Titus[i]+str(Compteur_Doublons))
                Nom_photo=os.path.exists(name)
                if Nom_photo == True:
                    continue
                else:
                    Compteur_Doublons=0
            urllib.request.urlretrieve(Url,name,Dossier_Photo_Titus)

    def Lien_Titus_photo(self):
        """
        Récupère les liens des photos et retourne dans une liste
        """
        Image_Titus = self.Image_Titus
        Liste_des_Nom_Titus = self.Titus_Nom()
        Liste_Url = []
        for i in range(len(Liste_des_Nom_Titus)):
            Url = ""
            # Prend les informations utile
            Data_sources = Image_Titus[i].picture.source["srcset"]
            Compteur = 0
            # Prend tout avant la virgule
            while Data_sources[Compteur] != ",":
                Url += Data_sources[Compteur]
                Compteur += 1
            Liste_Url.append(Url)
        return Liste_Url

    def Affichage(self):
        """
        Affiche dans l'ide
        """
        Liste_Complete_Titus=SkateDeluxe.Avenger_Rassemblement(self.Titus_Marque(),self.Titus_Nom(),self.Titus_Prix())
        for i in range(len(Liste_Complete_Titus)):
            Tempo=Liste_Complete_Titus[i]
            print("{}, {}\n{} €".format(Tempo[0],Tempo[1],Tempo[2]))


    def __del__(self):
        Chemin = self.Chemin_Titus
        for file in os.listdir(os.chdir(Chemin)):
            os.remove(file)



