from flask import Flask , render_template , redirect , url_for , session ,request ,flash
import mysql.connector as database 
import os 


##---------------------------------------------------------------------------------------------------------------------------------------------
## CONNEXION A LA BASE DE DONNEE 
##
#----------------------------------------------------------------

data = database.connect(host= 'localhost', user = 'root' , password = '' , database = 'sania')

app = Flask(__name__)
app.secret_key = "sania"
app.config['UPLOAD_FOLDER'] = "static/pdf"

######---------------------------------------------------------------------------------------------------------------------
#####
###
##
##
# Login AUthentification 
@app.route('/')
@app.route('/login')
def login():
	return render_template('index.html')


##
##-----------------------------------------------------------------------------------------------------------------------
##
@app.route('/login_send', methods = ['POST'])
def login_send():
	if request.method == 'POST':
		username 	= request.form.get('username')
		login 		= request.form.get('login')

		cur = data.cursor()
		cur.execute('SELECT * FROM agents WHERE email_agent = %s AND login_agent = %s' ,(username , login ,))
		data_test = cur.fetchone()

		if data_test:
			session['login'] = True
			session['id_agent'] = data_test[0]
			session['nom_agent'] = data_test[1]
			session['email_agent'] = data_test[2]
			session['phone_agent'] = data_test[3]
			session['fonction_agent'] = data_test[4]
			session['sexe_agent'] = data_test[7]
			session['photo_agent'] = data_test[8]

			if session['fonction_agent'] == 1:
				return redirect(url_for('accueil'))
			elif session['fonction_agent'] == 2:
				return redirect(url_for('message'))	
			elif session['fonction_agent'] == 3:
				return redirect(url_for('recevoir'))
			elif session['fonction_agent'] == 4:
				return redirect(url_for('recevoir'))	
			elif session['fonction_agent'] == 5:
				return redirect(url_for('recevoir'))
			elif session['fonction_agent'] == 6:
				return redirect(url_for('recevoir'))
			elif session['fonction_agent'] == 7:
				return redirect(url_for('recevoir'))	
			elif session['fonction_agent'] == 8:
				return redirect(url_for('recevoir'))				
			else:
				return redirect(url_for('login'))	
		else:
			flash('mot de passe errone'.upper())
			return redirect(url_for('login'))	
#####-----------------------------------------------------------------------------------------------------------------------
####
###
##
##
#
# DECONNEXION DE LA PAGE
@app.route('/deco')
def deco():
	session.clear()
	return redirect(url_for('login'))
###------------------------------------------------------------------------------------------------------------------------
##
##
#
# SUPPRIMER AGENT 
@app.route('/delete/<string:id_agent>', methods = ['GET'])
def delete(id_agent):
	cur = data.cursor()
	cur.execute("DELETE FROM agents WHERE id_agent = %s " , [id_agent])
	return redirect(url_for('accueil'))	

#######------------------------------------------------------------------------------------------------------------
######
#####
####
###
###
##
## MODIFICATION DES AGENTS 
@app.route('/modify/<string:id_agent>', methods = ['POST','GET'])
def modify(id_agent):
	if 'login' in session:
		if request.method == 'POST':
			nom = request.form.get('nom')
			email = request.form.get('email')
			phone = str(request.form.get('phone'))
			sexe  = request.form.get('sexe')

			cur = data.cursor()
			cur.execute("UPDATE agents SET nom_agent = %s , email_agent = %s , phone_agent = %s , sexe_agent = %s WHERE id_agent =%s",(nom,email,phone,sexe,id_agent,))
			data.commit()
			cur.close()

			return redirect(url_for('accueil'))
		cur = data.cursor()
		cur.execute("SELECT * FROM agents WHERE id_agent = %s" ,[id_agent])
		data_cur = cur.fetchone()

		return render_template('modifie.html', a = session['login'], data_aff = data_cur)
	else:
		return redirect(url_for('login'))	


######--------------------------------------------------------------------------------------------------------------------
#####
####
###
##
@app.route('/accueil')
def accueil():
	if 'login' in session:
		###
		##
		#
		#
		#liste generale des agents 

		cur = data.cursor()
		cur.execute("SELECT id_agent , nom_agent,email_agent,phone_agent, libelle_fonction ,date_Enregistrement,sexe_agent FROM agents INNER JOIN fonctions ON agents.fonction = fonctions.id_fonction")
		data_agent = cur.fetchall()

		return render_template('table-datatable-basic.html', a = session['login'], affiche = data_agent)
	else:
		return redirect(url_for('login')) 

#####-----------------------------------------------------------------------------------------------------------------------
####
###
##
##
#
# ENREGISTRE UN AGENT 
@app.route('/add')
def add():
	if 'login' in session:
		###
		###
		###liste de fonction admin 
		cur = data.cursor()
		cur.execute("SELECT * FROM fonctions where id_fonction in (1,2,3,4,5,6,7) ")
		data_fonction = cur.fetchall()

		###
		###
		###liste de fonction dircab
		cur1 = data.cursor()
		cur1.execute("SELECT * FROM fonctions WHERE id_fonction NOT IN (1,2,3,4,5,6,7) ")
		data_fonction1 = cur1.fetchall()

		return render_template('page-register.html',a = session['login'], affiche = data_fonction , affiche1 = data_fonction1 ) 
	else:
		return redirect(url_for('login'))	

###---------------------------------------------------------------------------------------------------------------------
###

@app.route('/add_send',methods =['POST'])
def add_send():
	if request.method == 'POST':
		nom = request.form.get('nom')
		email = request.form.get('email')
		phone = str(request.form.get('phone'))
		sexe  = request.form.get('sexe')
		fonction = request.form.get('fonction')

		####---------------------------------------------------------------------------------------------------------
		###
		###
		##
		##
		#
		#verification si l'admin est deja enregistre 

		adm = data.cursor()
		adm.execute('SELECT * FROM agents WHERE fonction = %s AND fonction = 1' ,(fonction,))
		data_adm = adm.fetchone()

		####----------------------------------------------------------------------------------------------------------
		###
		###
		##
		##
		#
		#verification si le dircab est deja enregistre 

		dircab = data.cursor()
		dircab.execute("SELECT* FROM  agents WHERE fonction = %s AND fonction = 4 ",(fonction,))
		data_dircab = dircab.fetchone()

		####----------------------------------------------------------------------------------------------------------
		###
		###
		##
		##
		#
		#verification si le ministre est deja enregistre 

		ministre = data.cursor()
		ministre.execute("SELECT* FROM agents WHERE fonction = %s AND fonction = 6 ",(fonction,))
		data_ministre = dircab.fetchone()

		####------------------------------------------------------------------------------------------------------------
		###
		###
		##
		##
		#
		#verification du mail

		mail = data.cursor()
		mail.execute("SELECT * FROM agents WHERE email_agent = %s ",(email,))
		data_mail = mail.fetchone()

		####-------------------------------------------------------------------------------------------------------------
		###
		###
		##
		##
		#
		#verification du numero de telephone

		
		if data_adm:
			flash("admin existe deja dans le systeme".upper())
			return redirect(url_for('add'))
		elif data_dircab:
			flash("dircab existe deja dans la systemt".upper())
			return redirect(url_for('add'))
		elif  data_ministre:
			flash('ministre existe deja'.upper())
			return redirect(url_for('add'))
		
		elif  data_mail:
			flash('mail existe deja'.upper())
			return redirect(url_for('add'))	
		else:
			cur = data.cursor()
			cur.execute("INSERT INTO agents(nom_agent,email_agent,phone_agent,fonction,sexe_agent)VALUES(%s,%s,%s,%s,%s)",(nom,email,phone,fonction,sexe,))
			data.commit()
			cur.close()
			flash("enregistrement reussi")
			return redirect(url_for('add'))	 		



######--------------------------------------------------------------------------------------------------------------
#####
####                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
####
###
## MESSAGE
@app.route('/message')
def message():
	if 'login' in session:
		id = session['id_agent']
		###
		###
		##
		##
		#
		#liste de message envoyer 

		msg = data.cursor()
		msg.execute('SELECT * FROM messages WHERE expediteurs = %s order by heures desc ' , (id,))
		data_msg = msg.fetchall()
		return render_template("email-inbox.html", a = session['login'] , aff_msg = data_msg)
	else:
		return redirect(url_for('login'))	
#--------------------------------------------------------------------------------------------------------------------

#######---------------------------------------------------------------------------------------------------------------
######
#####
####
##ENREGISTREMENT DU DOCUMENT 

@app.route('/document')
def document():
	if 'login' in session:
		#liste des agents pour la conversation 

		liste = data.cursor()
		liste.execute('select * from agents where fonction in (3,4,5,6,7,8)')
		data_liste = liste.fetchall()


		return render_template('email-compose.html' , a = session['login'], lst = data_liste)
	else:
		return redirect(url_for('login'))	
#--------------------------------------------------------------------------------------------------------------------

#######---------------------------------------------------------------------------------------------------------------
######
#####
####
##RECEVOIR LES MESSAGES 

@app.route('/recevoir')
def recevoir():
	if 'login' in session:
		ft = session['fonction_agent']
		agt = session['id_agent']
		###
		###
		##
		##
		#
		#liste de message envoyer



		msg = data.cursor()
		msg.execute('SELECT * FROM messages WHERE destinataire = %s or destinataire = %s order by heures desc ' , (ft,agt))
		data_msg = msg.fetchall()



	

		return render_template('recevoir.html' , a = session['login'] , aff_msg = data_msg)
	else:
		return redirect(url_for('login'))



###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
#ENVOIE MESSAGE RECEPTIONS 
@app.route('/reception_send',methods = ['POST'])
def reception_send():
	if request.method == 'POST':
		sujet 		 = request.form['sujet']
		description  = request.form['texte']
		file 		 = request.files['file']
		expediteur   = session['id_agent']
		destinataire = 3 

		agent 		 = session['id_agent']
		fonction 	 = session['fonction_agent']

		if file.filename != '':
			pat = os.path.join(app.config['UPLOAD_FOLDER'] , file.filename)
			file.save(pat) 

			cur = data.cursor()
			cur.execute("INSERT INTO messages(sujet,expediteurs,destinataire,descriptions,pdf,fonction_personne,agent_personne)VALUES(%s,%s,%s,%s,%s,%s,%s)",(sujet,expediteur,destinataire,description ,file.filename,fonction,agent,))
			data.commit()
			cur.close()
			return redirect(url_for('message'))
###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
# READ MESSAGES 
@app.route('/read/<string:id_messages>',methods = ['POST','GET'])
def read(id_messages):
	if 'login' in session:
		cur = data.cursor()
		cur.execute('SELECT id_messages ,sujet,expediteurs,destinataire,descriptions,pdf,heures,jours,libelle_fonction,nom_agent, email_agent ,phone_agent FROM messages inner join fonctions on messages.fonction_personne = fonctions.id_fonction inner join agents on messages.agent_personne = agents.id_agent where id_messages = %s',[id_messages,])
		data_cur = cur.fetchone()

		return render_template('email-read.html',a = session['login'],aff = data_cur)
	else:
		return redirect(url_for('login'))	
	return render_template()

###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
# MESSAGERIE ENTRE AGENT

@app.route('/all_send',methods = ['POST'])
def all_send():
	if request.method == 'POST':
		sujet = request.form['sujet']
		destinataire = request.form['destinataire']
		descriptions = request.form['texte'] 
		expediteur  = session['id_agent']
		file = request.files['file']
		fonction = session['fonction_agent']
		agent  = session['id_agent']

		if file.filename != '':
			p = os.path.join(app.config["UPLOAD_FOLDER"] , file.filename)

			file.save(p)

			cur = data.cursor()
			cur.execute("INSERT INTO messages(sujet,expediteurs,destinataire,descriptions,pdf,fonction_personne,agent_personne)VALUES(%s,%s,%s,%s,%s,%s,%s )",(sujet,expediteur,destinataire,descriptions,file.filename,fonction,agent))
			data.commit()
			cur.close()

			return redirect(url_for('message'))

###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
# PROFILES 			
@app.route('/profile')
def profile():
	if 'login' in session:
		return render_template('profile.html', a = session['login'])
	else:
		return redirect(url_for('login'))


###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
# PHOTOS ADD
@app.route('/photo/<string:id_agent>',methods = ['POST','GET']) 
def photo(id_agent):
    if 'login' in session:
        if request.method == 'POST':
            photo = request.files['photo']

            if photo.filename != '':
                send_photo = os.path.join(app.config['UPLOAD_FOLDER'],photo.filename)
                photo.save(send_photo)
                cur = data.cursor()
                cur.execute('update agents set photo_agent = %s where id_agent = %s ', (photo.filename,id_agent,))
                data.commit()
                cur.close()
                return redirect(url_for('login')) 
               

        cur = data.cursor()
        cur.execute('select * from agents where id_agent = %s',[id_agent,])
        tst_statut = cur.fetchone()
        return render_template('photo.html',photo = tst_statut) 
    else:
        return redirect(url_for('login'))



###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
# MODIFICATIONS DES AGENTS

# MODIFIER AGENT
@app.route('/modify_agent/<string:id_agent>',methods = ['GET','POST'])
def modifier_agent(id_agent):
    if 'login' in session:
        if request.method == 'POST':
            nom         = request.form['nom_agent']
            mail        = request.form['mail_agent']
            phone       = str(request.form['phone_agent'])
            sexe       = request.form['sexe_agent']
            
            # fonction    = request.form['fonction_agent']

            cur = data.cursor()
            cur.execute("update agents set nom_agent = %s , email_agent = %s, phone_agent = %s , sexe_agent = %s  where id_agent = %s",(nom,mail,phone,sexe,id_agent, ))
            data.commit()
            cur.close()
            # flash("modification reussi")

            return redirect(url_for('accueil'))
   
        
       

        fnc = data.cursor()
        fnc.execute("select * from fonctions")
        t = fnc.fetchall()

        cur = data.cursor()
        cur.execute("select * from agents where id_agent = %s" ,[id_agent,])
        test_cur = cur.fetchone()
        return render_template('modify_agent.html',a = session['login'], data = test_cur, dat = t)
    else:
        flash("pas d'autorisation veillez vous connecte ")
        return redirect(url_for('login')) 
###########--------------------------------------------------------------------------------------------------------------------
##########
#########
#######
######
#####
####
###
##
##
#
# MODIFICATIONS DES AGENTS

@app.route('/password_modifier')
def password_modifier():
    if 'login' in session:
      

        return render_template('password_modier.html',a = session['login'])
    else:
        return redirect(url_for('index'))

@app.route('/password_modifier/<string:id_agent>',methods =['POST','GET'])
def update_password(id_agent):
    if request.method == 'POST':
        ancien = request.form['acien']
        mdp   = request.form['mdp']
        conf  = request.form.get('conf')

        call = session['id_agent']  

        #verification 

       

        cur = data.cursor()
        cur.execute('SELECT * FROM agents WHERE  login_agent = %s AND id_agent = %s', (ancien,id_agent))
        test_data = cur.fetchone()

        #verification du mot de passe conforme

        if test_data :
            if mdp != conf:
                flash('le mot de passe doit etre conformer')
         
            else:
                c = data.cursor()
                c.execute("update agents set login_agent = %s where id_agent = %s ", (mdp,id_agent,))  
                data.commit()
                c.close()  
                return redirect(url_for('login'))

            
        else:
            flash('ancien mot de passe incorrecte')  
            

    cur = data.cursor()
    cur.execute('select * from agents where id_agent = %s',[id_agent,])
    t_s = cur.fetchone()

    return render_template('password_modier.html',data = t_s)





if __name__ == '__main__':
	app.run(debug = True)
